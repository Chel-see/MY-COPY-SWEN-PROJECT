from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=True)
    type = db.Column(db.String(50))

    
    def __init__(self, username, password, email, phone_number=None):
        self.username = username
        self.set_password(password)
        self.email = email
        self.phone_number = phone_number

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'type': self.type,
            'email': self.email,
            'phone_number': self.phone_number
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
        
    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on':type
    }