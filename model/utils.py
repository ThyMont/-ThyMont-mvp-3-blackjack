def evaluate_hand(card_list):
    total = 0
    aces = 0

    for card in card_list:
        valor = card['value']
        if valor in ['KING', 'QUEEN', 'JACK']:
            total += 10
        elif valor == 'ACE':
            total += 11
            aces += 1
        else:
            total += int(valor)

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total


def evaluate_blackjack_natural(mao):
    if len(mao) == 2:
        values = [card['value'] for card in mao]
        return 'ACE' in values and any(valor in ['10', 'KING', 'QUEEN', 'JACK'] for valor in values)
    return False
