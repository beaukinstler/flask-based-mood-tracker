# Example Flask App

## model

I'm creating this based on my 
example app, which I built to recap of the basics learned in a recent training session.

The model in the example was a Teacher/Student database, with a linking table
for the relationships, including a grade in the linking table.

I'm leaving this README change to document that the base of the app was built on that 
small project. 

## config

instead of defining details in the __init__.py of the src, I'm also 
creating a config.py that could read from env variables. 

From past experience, it's best to get in the habit of keeping 
those details dynamic, and not in the source code. 


## setup

Assumptions: 
- a container named pg_container is running, as defined in in the `docker-compose.yml` file by nucamp.

config.py goes in the same folder as this README.md 

create the database you plan to use ..
e.g. `docker exec pg_container psql -c "CREATE DATABASE example"`
or `postgres=# CREATE DATABASE example;`

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
`$ docker exec pg_container psql -d example -c '\dt'`

The output should look similar to below:

    $ docker exec pg_container psql -d example -c '\dt'
                List of relations
    Schema |       Name        | Type  |  Owner
    --------+-------------------+-------+----------
    public | alembic_version   | table | postgres
    public | students          | table | postgres
    public | teachers          | table | postgres
    public | teachers_students | table | postgres
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


At this point, the urls `http://127.0.0.1:5000/students` and `http://127.0.0.1:5000/teachers`
should return a 404 if used, in your browser, assuming you didn't already add any data. 

To add some data using the API, use a POST request.
To do this with a tool like "Insomnia" add the body as json:

    {
	    "name":"Dr. Lovlace"
    }


## After initial test



1. use `flask db downgrade`, to drop the test tables.

2. remove all the migrations from .\migrations\versions

3. remove the blueprints from (or comment out to save for examples)

    - currently these are at line 37

        from .api import teachers, students
        app.register_blueprint(teachers.bp)
        app.register_blueprint(students.bp)

4. Remove the `student.py` and `teacher.py`

5. remove the models from the src\models.py

    - everything after the `db = SQLAlchemy()`

6. Reverse all these steps, to add your new api code

    1. Add your classes to the models 
    2. Add routes in the `api` directory
    3. import and register the blueprints defined in the route files
    4. run `pipenv run flask db migrate`
    5. run `pipenv run flask db upgrade`
    6. run `pipenv flask run --reload --debugger`
    
