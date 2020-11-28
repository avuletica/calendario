# Introduction
Purpose to create example of FastAPI architecture with:
 - JWT authorization
 - Alembic integration
 - building images with docker
 - utilisation of docker-compose for handling multiple docker services
 - celery worker for handling intensive background tasks
 - testing
 
This was done with a task to parse, store .ics files and .. todo...


## Installation

```
  $ git clone https://github.com/avuletica/calendario.git && cd calendario
  $ docker-compose up
```
For first time setup we must run migrations (we can also add initial data for testing):

```
  $ docker exec -it calendario sh
  $ alembic upgrade head
  $ python init_data.py
```

#### Helpful alembic commands
generate a new revision
```
$ alembic revision --autogenerate -m "revision message"`
```
downgrade last revision
```
$ alembic downgrade -1
```

### Testing

To get fresh docker container (no volume data)
```
    $ docker rm -f -v calendario_pg_db
```