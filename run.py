import os
from app import create_app, db
from flask_migrate import Migrate
#from app.models.user import User
#from app.models.models import Quiz, Question, Answer, PageScan

#app = create_app()
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
from flask_migrate import Migrate
#
# @app.cli.command("init-db")
# def init_db():
#     db.create_all()
#     print("Database tables created.")

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    #app.run()
    app.run(port=8080, host='0.0.0.0', debug=True)
