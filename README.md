# Introduction
Purpose to create example of FastAPI architecture with:
 - JWT authorization
 - Alembic integration
 - building images with docker
 - utilisation of docker-compose for handling multiple docker services
 - testing (pytest)
 
Task: parse, store .ics files and make an algorithm to calculate optimal cleaning time.

## Installation

```
  $ git clone https://github.com/avuletica/calendario.git && cd calendario
  $ docker-compose up
```
For first time setup we must run migrations (we can also add initial data for testing):

```
  $ docker exec -it calendario_be sh
  $ alembic upgrade head
  $ python init_data.py
```
BE: http://localhost:8080/docs

FE (work in progress): http://localhost:4200/login
### Cleaning algorithm

Cleaning time is scheduled from 11:00 AM to 15:00 PM

x = date ranges when apartment is unoccupied

|apartment|date_range_1|date_range_2|date_range_3|date_range_4|
|:----:|:---:|:---:|:---:|:---:|
| A1   | x   | x   | x   |     |
| A2   | x   | x   |     |     |
| A3   | x   | x   | x   |     |
| A4   | x   | x   | x   | x   |

For given datetime range

1) Find intervals when the apartment is unoccupied
    - This is done by combining apartment first end_datetime (end of stay) with apartments
    next start_time (next guest coming) and generating datetime range
2) If there is a booking on the same day the guest leaves, that day will be optimal cleaning time.
3) If we find common intervals where apartments are unoccupied => result in group cleaning
    - this is done by checking if there is an intersection in the available days of each apartment.
        - If there is an intersection => find availability_range with the most number of intersections,
            this will result in most apartment cleaning per day.
        - All availability_ranges that fall under the previous category will be removed for the next iteration
        - Repeat the process as long as there are common intervals.
4) If there are no common interval where apartments are unoccupied suggest the first available cleaning is:
    - same day if the guest leaves at or before 11 AM
    - next day if the guest leaves after 3 PM

### Testing

Running all test cases with pytest:

```
    $ docker exec -it calendario_be sh
    $ pytest
```

To get fresh docker container (no volume data)
```
    $ docker rm -f -v calendario_pg_db
```


### Database diagram
<img src="https://github.com/avuletica/calendario/blob/master/backend/app/static/calendario_db_diagram.png" width="1000" height="300">

#### Helpful alembic commands
generate a new revision
```
$ alembic revision --autogenerate -m "revision message"`
```
downgrade last revision
```
$ alembic downgrade -1
```
