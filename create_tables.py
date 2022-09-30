from app.config import config
from app.server import create_app
from app.setup.db import db

if __name__ == '__main__':
    with create_app(config).app_context():
        db.create_all()
