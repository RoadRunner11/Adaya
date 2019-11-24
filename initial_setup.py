from app import create_app
from app.helper.app_context import AppContext as AC
from app.models import User,Role

db = AC().db

if __name__ == "__main__":
    app = create_app("config.dev")  # start app with config
    with app.app_context():
        db.drop_all()
        db.create_all()
        member = Role("member")
        admin = Role("admin")
        user = User("abc@gmail.com", "1q2w3e4r")
        user2 = User("abcd@gmail.com", "1q2w3e4r")
        user.role = admin
        db.session.add(member)
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()
