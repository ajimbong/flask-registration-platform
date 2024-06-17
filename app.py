from blueprints import main, admin
from config import db, app

app.register_blueprint(main.bp)
app.register_blueprint(admin.admin_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
