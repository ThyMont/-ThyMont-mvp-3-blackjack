from pydantic import BaseModel, Field
from typing import List


class GamePath(BaseModel):
    """
    Recupera o ID do Game
    """
    game_id: str = Field('l2jp2wau5s2e', description='ID do Game')


class CardSchema(BaseModel):
    """
    Define o objeto Card
    """
    image: str = "https://deckofcardsapi.com/static/img/KH.png"
    value: str = "KING"
    suit: str = "HEARTS"
    code: str = "KH"


class HandSchema(BaseModel):
    """
    Define a mão de um jogador
    """
    cards: List[CardSchema]
    score: int


class MatchSchema(BaseModel):
    """
    Resposta da partida
    """
    deck_id: str
    dealer: HandSchema
    player: HandSchema
    remaining: int
    game_over: bool = False
    winner: str = ""
    is_natural_blackjack: bool = False
