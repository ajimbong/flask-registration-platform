from blueprints import main
from config import db, app

app.register_blueprint(main.bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
