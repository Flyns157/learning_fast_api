# My first project with FastApi

*Mise en place d'une API pour Pokemons*

## Screenshots

![image](https://drive.google.com/uc?export=view&id=1nbcsVC8JANUrOaOO42k_3PDsgiFgM6wu)

## Tools

Réalisé avec

- Python (3.12)
- Fast API
- Uvicorn
- Pydantic
- Docker

## Usage

### With Docker :

* To deploy :
* ```
  docker compose up -d deploy --build
  ```
* To debug :
* ```
  docker compose up debug --build 
  ```

### Without Docker :

* To deploy:
* ```
  fastapi run app
  ```
* To debug:
* ```
  fastapi dev app
  ```
