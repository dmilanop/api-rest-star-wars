from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(60), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    favorites = db.relationship("Favorite", backref="user", uselist=True)

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

#     # people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
#     # planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
#     # vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))

    def serialize(self):
        return {
            "name": self.name,
            "id": self.id,
        }


# class People(db.Model):
#     name = db.Column(db.String(80), nullable=False)
#     id = db.Column(db.Integer, primary_key=True)
#     age = db.Column(db.Integer, unique=True)
#     favorites = db.relationship("Favorites")

#     def serialize(self):
#         return {
#             "name": self.name,
#             "id": self.id,
#             "age": self.age
#         }


# class Planet(db.Model):
#     name = db.Column(db.String(80), nullable=False)
#     id = db.Column(db.Integer, primary_key=True)
#     population = db.Column(db.Integer, nullable=False)
#     favorites = db.relationship("Favorites")

#     def serialize(self):
#         return {
#             "name": self.name,
#             "id": self.id,
#             "population": self.population
#         }


# class Vehicle(db.Model):
#     name = db.Column(db.String(80), nullable=False )
#     id = db.Column(db.Integer, primary_key=True)
#     speed = db.Column(db.Integer, nullable=False)
#     favorites = db.relationship("Favorites")

#     def serialize(self):
#         return {
#             "name": self.name,
#             "id": self.id,
#             "speed": self.speed
#         }