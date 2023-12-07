from src import create_app
from flask_migrate import upgrade
from sqlalchemy.exc import ProgrammingError
from src.utils.create_initial_user import create_user_if_not_exists


app = create_app()



if __name__ == "__main__":
    create_user_if_not_exists()
    app.run(host='0.0.0.0', port=5001)
