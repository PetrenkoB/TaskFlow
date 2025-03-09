Simple REST-api using Flask and Flask-restful

Make shure you have .env file with enviroment variables:  

FLASK_DEBUG  
DATABASE_URL  
DATABASE_USER  
DATABASE_PASSWORD  
DATABASE_HOST  
DATABASE_PORT  
DATABASE_NAME  
JWT_SECRET_KEY

Database in question - PostgreSQL

Launching locally:  
You need to have db with corresponding to DATABASE_NAME name in your PostgreSQL instance  

```shell
python3 -m venv .venv
source .venv/bin/activate #see https://docs.python.org/3/library/venv.html#creating-virtual-environments  if you have platform issues
pip install -r requirements.txt
python3 app.py # dev only
```

Launching with Docker compose:  

```shell
docker compose up --build
```