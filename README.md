# Introduction
TODO

## Installation

```
  $ git clone https://github.com/avuletica/calendario.git && cd calendario
  $ docker-compose up
```
For first time setup we must run migrations:

```
  $ docker exec -it calendario sh
  $ alembic upgrade head
```

downgrade last revision
```
$ alembic downgrade -1
```