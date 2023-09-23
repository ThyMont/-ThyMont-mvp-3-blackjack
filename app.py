from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import *
# from logger import logger
from schemas.game_schema import GamePath, MatchSchema
from schemas.error import ErrorSchema
from service import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")


@app.get('/', tags=[home_tag])
@app.get('/home', tags=[home_tag])
@app.get('/index', tags=[home_tag])
def home():
    """
    Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.get('/newgame', responses={"200": MatchSchema, "503": ErrorSchema})
def teste():
    """
    Inicia uma nova partida
    """
    service = GameService()
    return service.start()


@app.get("/restart/<string:game_id>", responses={"200": MatchSchema, "503": ErrorSchema})
def restart(path: GamePath):
    """
    Reinicia uma partida utilizando um deck anterior
    """
    service = GameService()
    return service.restart(path.game_id)


@app.get("/hit/<string:game_id>", responses={"200": MatchSchema, "503": ErrorSchema})
def hit(path: GamePath):
    """
    Player compra uma carta
    """
    service = GameService()
    return service.hit(path.game_id)


@app.get("/stand/<string:game_id>", responses={"200": MatchSchema, "503": ErrorSchema})
def stand(path: GamePath):
    """
    Player mantém sua mão e partida é finalizada
    """
    service = GameService()
    return service.stand(path.game_id)


@app.get("/double/<string:game_id>", responses={"200": MatchSchema, "503": ErrorSchema})
def double(path: GamePath):
    """
    Player dobra a aposta, compra uma nova carta e partida é finalizada
    """
    service = GameService()
    return service.double(path.game_id)
