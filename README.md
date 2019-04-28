# Run project in windows

## Run virtualenv 'env'

    /env/Scripts/activate


## Run Database

    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade

# Setting up application

This application uses sqlite3 database for an easy startup.
running this application with Docker environment uses postgres database.

## Running without docker

### Using virtualenv

Activate virtual environment
```
    source <env_name>/bin/activate
```

Install project dependencies
```
    pip install -r requirements.txt
```

Run localhost development server
```
    python app.py
```

## Running with Docker
requires Docker installed locally.
To run this project with docker change ```DOCKER=True``` in ```app.py```
and the command to build the containers:
```
    docker-compose up -d 
```

