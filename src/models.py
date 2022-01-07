from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(60), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    favorites = db.relationship("Favorite", backref="user", uselist=True)

    @classmethod
    def create(cls, new_user):
        new_user = cls(**new_user)
        db.session.add(new_user)
        try:
            db.session.commit()
            return new_user
        except Exception as error:
            db.session.rollback()
            print(error.args)
            return None


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    url = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint(
        "user_id",
        "url",
        name = "unique_favorite_user"
    ),)

    def serialize(self):
        return {
            "name": self.name,
            "id": self.id,
        }

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except Exception as error: 
            db.session.rollback()
            return False


