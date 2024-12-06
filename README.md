# RAGnarock
Building a hella RAG system

## Requirements
 - Python 3.8 or later.

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

 ## Run the server

 ```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
 ```

 ## Postman collection

 Download the POSTMAN collection from [/assets/mini-rag-app.postman_collection.json](/assets/mini-rag-app.postman_collection.json)