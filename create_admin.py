from app import app, db, Admin
from werkzeug.security import generate_password_hash

with app.app_context():

    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    admin = Admin(
        username=username,
        password=generate_password_hash(password)
    )

    db.session.add(admin)
    db.session.commit()

    print("Admin created successfully!")