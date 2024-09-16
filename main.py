from app import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates database tables
    app.run(debug=True)