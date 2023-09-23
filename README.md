# mvp-3-blackjack

# Criar venv

```
$ py -m venv venv
```

# Iniciar venv

```
$ .\venv\Scripts\activate
```

# Encerrar venv

```
$ deactivate
```

# Instalar dependências

```
(env)$ pip install -r requirements.txt
```

# Para executar a API:

```
(env)$ flask run --host 0.0.0.0 --port 5001
```

# Criar imagem no Docker

```
docker build -t blackjack-backend .
```

# Iniciar imagem no Docker

```
docker run -p 5001:5001 blackjack-backend
```
