from App.database import db
from App.models.user import User

class Employer(User):
    __tablename__ = 'employer'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    positions = db.relationship("Position", back_populates="employer")

    __mapper_args__={"polymorphic_identity" : "employer"}

    def __init__(self, username, password, email, company, phone_number=None):
        super().__init__(username, password, email, phone_number)
        self.company = company
        self.type = "employer"

    def __repr__(self):
        return f'<Employer ID: {self.id} - Username: {self.username} - Company: {self.company}>'
