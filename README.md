# Mood Tracker

## config

Configs are in config.py.

You can also use a .env file

For tests, use tests/test_config.py


## setup

Assumptions: 
- a container named moody_pg_container is running, as defined in in the `docker-compose.yml` file.

config.py goes in the same folder as this README.md 

create the database you plan to use ..
e.g. `docker exec moody_pg_container psql -c "CREATE DATABASE moody"`
or `postgres=# CREATE DATABASE moody;`

## .env

you can use a .env, which `flask db` commands can find. 
Or, just use what's in the config.py defaults
the `.env_example` can be updated, and then remove the `_example` from the name.



## migrations

If you run 
`flask db migrate`
`flask db upgrade`

it should create three tables in the database, asside from the alembic_version table

to check you can run 
`$ docker exec moody_pg_container psql -d moody -c '\dt'`

The output should look similar to below:

    $ docker exec moody_pg_container psql -d moody -c '\dt'
                List of relations
    Schema |       Name        | Type  |  Owner
    --------+-------------------+-------+----------
    public | alembic_version   | table | postgres
    public | moods             | table | postgres
    public | users             | table | postgres
    public | users_moods       | table | postgres
    (4 rows)


## running the app for the first time

the command...

    $ python wsgi.py 
    
should start the app, but the more common way would be to use...
    
    $ python -m flask run

for debugging tools you may also want to try, but only when running in a safe server for testing:

    $ python -m flask run --reload --debugger

If using Visual Studio Code, you may want to try to run it using the debugger provided as well. 

the provided .vscode\launch.json settings might help, at least get you started with this. 


At this point, the urls `http://127.0.0.1:5000/moods` and `http://127.0.0.1:5000/users`
should return a 200 if used, in your browser, assuming you didn't already add any data. 

To add some data using the API, use a POST request to `http://127.0.0.1:5000/moods`
To do this with a tool like "Insomnia" add the body as json:

    {
	    "description":"happy"
    }



    
