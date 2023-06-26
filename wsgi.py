from src import create_app
from flask_migrate import upgrade


app = create_app()

with app.app_context():
    upgrade()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
