# Introduction
TODO

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