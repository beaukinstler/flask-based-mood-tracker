from src.models import User
from src import db
from sqlalchemy.exc import ProgrammingError
import os

def create_user_if_not_exists():
    """
    Query for an existing user, and if none exists, create one.
    If the database has not been created yet, run `flask db upgrade`.
    """
    try:
        user = User.query.first()
        if not user:
            admin_user = os.environ.get('ADMIN_USERNAME')
            admin_password = os.environ.get('ADMIN_PASSWORD')
            if not admin_user or not admin_password:
                raise EnvironmentError("ADMIN_USERNAME and ADMIN_PASSWORD must be set as environment variables")
            user = User(admin_user, admin_password)
            user.is_admin = True
            db.session.add(user)
            db.session.commit()
    except ProgrammingError as e:
        print(e)
        print("ProgrammingError. This is likely because the database has not been created yet. Run `flask db upgrade`")
    except Exception as e:
        print(e)
        pass

    if os.environ.get('TESTING') == "1":
        creat_test_users()


def creat_test_users():
    try:
        if User.query.count() > 1:
            return
        for i in range(1, 21):
            user = User(f"test_user{i}", "123123")
            db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        raise
        
    pass