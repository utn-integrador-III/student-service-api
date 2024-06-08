from db import db

class LostObject(db.Model):
    __tablename__ = 'lost_objects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    date_found = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'date_found': self.date_found.isoformat(),
            'location': self.location
        }
