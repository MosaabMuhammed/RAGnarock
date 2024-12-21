# RAGnarock
Building a hella RAG system

## Requirements
 - Python 3.8 or later.

 #### Install deps
 ```bash
 sudo apt update
 sudo apt install libpq-dev gcc python3-dev
 ```

 ### Install Python using Miniconda
 1. Download and install Miniconda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
 2. Createt a new environment using the following command:
 ```bash
 $ conda create -n mini-rag python=3.8
 ```
 3. Activate the environment:
 ```bash
 $ conda activate mini-rag
 ```

 ## Installation
 ### Install the required packages
 ```bash
 $ pip install -r requirements.txt
 ```

 ### Setup the environment variables
 ```bash
 $ cp .env.example .env
 ```

 Then you will need to set your environment variables in `.env` file.

 ### Run the docker server
 ```bash
$ cd docker
$ cp .env.example .env
$ sudo docker compose up -d
 ```

 ## Run the server

 ```bash
$ cd src
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
 ```

 ## Postman collection

 Download the POSTMAN collection from [/assets/mini-rag-app.postman_collection.json](/assets/mini-rag-app.postman_collection.json)


### Docker helpful commands
```bash
// stop any working containers.
$ sudo docker stop $(sudo docker ps -aq)

// remove any stopped containers.
$ sudo docker rm $(sudo docker ps -aq)

// remove any downloaded images.
$ sudo docker rmi $(sudo docker images -q)

// remove any dockers volumes.
$ sudo docker volume rm $(sudo docker volume ls -q)

// Clean anything left after removing and stopping everything.\
$ sudo docker system prune --all
```

### Run DB migration
```bash
$ cd .\models\db_schemas\ragnarok_db\
$ alembic init alembic
```
These commands will create a new folder called `alembic` and another file called `alembic.ini`.

Next, we will need to create a copy for the `alembic.ini` file as `alembic.ini.example` to be as an example for any new developer.

Next, change the `sqlalchemy.url` in `alembic.ini` to your database url.

Now, we need to guide alembic to the logic of our database's tables. We can do this by going to `env.py` in `alembic` folder, and add the following:
```python
from schemas import SQLAlchemyBase

target_metadata = SQLAlchemyBase.metadata
```

while we are still in the database folder `ragnarok_db`, we write the following commands to create the tables:
```bash
$ alembic revision --autogenerate -m "Initial Commit"
$ alembic upgrade head
```

for any future updates, just run the previous two commands with new commit message, and the changes will be reflected.

NOTE: your changes is backward comptabile.
