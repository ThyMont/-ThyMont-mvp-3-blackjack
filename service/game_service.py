import requests
from model.utils import evaluate_hand, evaluate_blackjack_natural


class GameService:

    msg_erro_api = "Erro API Cards"

    def start(self):
        # Embaralha as
        request = requests.get(
            "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
        json = request.json()
        deck_id = json["deck_id"]
        return self.draw_cards(deck_id)

    def restart(self, deck_id):
        request = requests.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/shuffle/")
        json = request.json()
        deck_id = json["deck_id"]
        return self.draw_cards(deck_id)

    def draw_cards(self, deck_id):
        # Retirar 4 cartas, sendo 2 para o dealer e 2 para o player
        request = requests.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=4")
        json = request.json()
        if not json["success"]:
            return {'message': self.msg_erro_api}, 503

        dealer_card_list = json["cards"][0:2]
        dealer_cards = []
        for card in dealer_card_list:
            del (card["images"])
            dealer_cards.append(card["code"])
        requests.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/dealer/add/?cards={','.join(map(str, dealer_cards))}")

        player_card_list = json["cards"][2::]
        player_cards = []
        for card in player_card_list:
            del (card["images"])
            player_cards.append(card["code"])
        requests.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/player/add/?cards={','.join(map(str, player_cards))}")

        return {'deck_id': json["deck_id"],
                'dealer': {'cards': [dealer_card_list[0], {'code': 'back', 'image': "https://deckofcardsapi.com/static/img/back.png"}],
                           'score': evaluate_hand([dealer_card_list[0]])},
                'player': {'cards': player_card_list,
                           'score': evaluate_hand(player_card_list)},
                'remaining': json["remaining"]}, 200

    def stand(self, deck_id):

        self.dealer_play(deck_id)

        request = requests.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/player/list/"
        )
        json = request.json()
        if not json["success"]:
            return {'message': self.msg_erro_api}, 503
        piles = json["piles"]
        player = piles["player"]
        player_card_list = player["cards"]
        player_score = evaluate_hand(player_card_list)
        for card in player_card_list:
            del (card["images"])

        request = requests.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/dealer/list/"
        )
        json = request.json()
        if not json["success"]:
            return {'message': self.msg_erro_api}, 503
        piles = json["piles"]
        dealer = piles["dealer"]
        dealer_card_list = dealer["cards"]
        for card in dealer_card_list:
            del (card["images"])

        winner = self.define_winner(player_card_list, dealer_card_list)

        return {'deck_id': json["deck_id"],
                'game_over': True,
                'winner': winner,
                'is_natural_blackjack': evaluate_blackjack_natural(player_card_list) if winner == 'player' else False,
                'dealer': {'cards': dealer_card_list,
                           'score': evaluate_hand(dealer_card_list)},
                'player': {'cards': player_card_list,
                           'score': player_score},
                'remaining': json["remaining"]}, 200

    def double(self, deck_id):

        request = requests.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1")
        json = request.json()
        if not json["success"]:
            return {'message': self.msg_erro_api}, 503
        player_card_list = json["cards"]
        player_cards = []
        for card in player_card_list:
            del (card["images"])
            player_cards.append(card["code"])
        requests.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/player/add/?cards={','.join(map(str, player_cards))}")

        request = requests.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/player/list/"
        )
        json = request.json()
        if not json["success"]:
            return {'message': self.msg_erro_api}, 503
        piles = json["piles"]
        player = piles["player"]
        player_card_list = player["cards"]
        player_score = evaluate_hand(player_card_list)
        for card in player_card_list:
            del (card["images"])

        bust = player_score > 21

        request = requests.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/dealer/list/"
        )
        json = request.json()
        if not json["success"]:
            return {'message': self.msg_erro_api}, 503
        piles = json["piles"]
        dealer = piles["dealer"]
        dealer_card_list = dealer["cards"]
        for card in dealer_card_list:
            del (card["images"])

        if bust:
            return {'deck_id': json["deck_id"],
                    'game_over': True,
                    'winner': "dealer",
                    'is_natural_blackjack': False,
                    'dealer': {'cards': dealer_card_list,
                               'score': evaluate_hand(dealer_card_list)},
                    'player': {'cards': player_card_list,
                               'score': player_score},
                    'remaining': json["remaining"]}, 200

        self.dealer_play(deck_id)

        request = requests.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/player/list/"
        )
        json = request.json()
        if not json["success"]:
            return {'message': self.msg_erro_api}, 503
        piles = json["piles"]
        player = piles["player"]
        player_card_list = player["cards"]
        player_score = evaluate_hand(player_card_list)
        for card in player_card_list:
            del (card["images"])

        request = requests.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/dealer/list/"
        )
        json = request.json()
        if not json["success"]:
            return {'message': self.msg_erro_api}, 503
        piles = json["piles"]
        dealer = piles["dealer"]
        dealer_card_list = dealer["cards"]
        for card in dealer_card_list:
            del (card["images"])

        winner = self.define_winner(player_card_list, dealer_card_list)

        return {'deck_id': json["deck_id"],
                'game_over': True,
                'winner': winner,
                'is_natural_blackjack': evaluate_blackjack_natural(player_card_list) if winner == 'player' else False,
                'dealer': {'cards': dealer_card_list,
                           'score': evaluate_hand(dealer_card_list)},
                'player': {'cards': player_card_list,
                           'score': player_score},
                'remaining': json["remaining"]}, 200

    def hit(self, deck_id):
        request = requests.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1")
        json = request.json()
        if not json["success"]:
            return {'message': self.msg_erro_api}, 503
        player_card_list = json["cards"]
        player_cards = []
        for card in player_card_list:
            del (card["images"])
            player_cards.append(card["code"])
        requests.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/player/add/?cards={','.join(map(str, player_cards))}")

        request = requests.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/player/list/"
        )
        json = request.json()
        if not json["success"]:
            return {'message': self.msg_erro_api}, 503
        piles = json["piles"]
        player = piles["player"]
        player_card_list = player["cards"]
        player_score = evaluate_hand(player_card_list)
        for card in player_card_list:
            del (card["images"])

        bust = player_score > 21

        request = requests.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/dealer/list/"
        )
        json = request.json()
        if not json["success"]:
            return {'message': self.msg_erro_api}, 503
        piles = json["piles"]
        dealer = piles["dealer"]
        dealer_card_list = dealer["cards"]
        for card in dealer_card_list:
            del (card["images"])

        if bust:
            return {'deck_id': json["deck_id"],
                    'game_over': True,
                    'winner': "dealer",
                    'is_natural_blackjack': False,
                    'dealer': {'cards': dealer_card_list,
                               'score': evaluate_hand(dealer_card_list)},
                    'player': {'cards': player_card_list,
                               'score': player_score},
                    'remaining': json["remaining"]}, 200

        return {'deck_id': json["deck_id"],
                'dealer': {'cards': [dealer_card_list[0], {'code': 'back', 'image': "https://deckofcardsapi.com/static/img/back.png"}],
                           'score': evaluate_hand([dealer_card_list[0]])},
                'player': {'cards': player_card_list,
                           'score': player_score},
                'remaining': json["remaining"]}, 200

    def dealer_play(self, deck_id):
        request = requests.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/dealer/list/"
        )
        json = request.json()
        if not json["success"]:
            return {'message': self.msg_erro_api}, 503
        piles = json["piles"]
        dealer = piles["dealer"]
        dealer_card_list = dealer["cards"]

        score = evaluate_hand(dealer_card_list)

        while score < 17:
            request = requests.get(
                f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1")
            json = request.json()
            if not json["success"]:
                return {'message': self.msg_erro_api}, 503
            dealer_card_list = json["cards"]
            dealer_cards = []
            for card in dealer_card_list:
                del (card["images"])
                dealer_cards.append(card["code"])
            requests.get(
                f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/dealer/add/?cards={','.join(map(str, dealer_cards))}")
            request = requests.get(
                f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/dealer/list/"
            )
            json = request.json()
            if not json["success"]:
                return {'message': self.msg_erro_api}, 503
            piles = json["piles"]
            dealer = piles["dealer"]
            dealer_card_list = dealer["cards"]
            score = evaluate_hand(dealer_card_list)

    def define_winner(_, player_card_list, dealer_card_list):
        if evaluate_blackjack_natural(player_card_list):
            # Verificar se o dealer também tem um blackjack natural
            if evaluate_blackjack_natural(dealer_card_list):
                return "push"
            else:
                return "player"

        # Verificar se o dealer tem um blackjack natural
        if evaluate_blackjack_natural(dealer_card_list):
            return "dealer"

        player_score = evaluate_hand(player_card_list)
        dealer_score = evaluate_hand(dealer_card_list)

        if player_score > 21:
            return "dealer"
        elif dealer_score > 21:
            return "player"
        elif player_score > dealer_score:
            return "player"
        elif player_score < dealer_score:
            return "dealer"
        else:
            return "push"
