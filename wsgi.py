from src import create_app
from flask_migrate import upgrade
from sqlalchemy.exc import ProgrammingError
from src.utils import create_initial_user


app = create_app()
with app.app_context():
    try:
        create_initial_user.create_user_if_not_exists()
    except:
        pass



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
