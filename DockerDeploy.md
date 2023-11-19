# requirements

- `docker compose` or equivalent

# docker


### files needed
1. docker-compose.yml
2. .env
3. container_entrypoint/entrypoint.sh
    - this runs flask db upgrade and starts the flask app

# steps
1. `git clone https://github.com/beaukinstler/flask-based-mood-tracker.git`
1. `cd flask-based-mood-tracker`
1. `cp .env_example .env`
1. docker compose pull
2. docker volume create moodsy_pg_data
3. docker compose up -d

