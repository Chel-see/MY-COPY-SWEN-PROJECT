from App.database import db
from App.models.user import User

from App.models.context import Context


class Shortlist(db.Model):  # because an application can exit and be a shortlisted application
    __tablename__ = 'shortlist'
    id = db.Column(db.Integer, primary_key=True)
    application_id=db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False,unique=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    isWithdrawn = db.Column(db.Boolean, default=False)

    application=db.relationship('Application', backref=('shortlist'), lazy=True)
    staff = db.relationship('Staff', backref=('shortlist'), lazy=True)
    


    def __init__(self,application_id,staff_id):  # an application will be created first with a position and by a student
        self.application_id=application_id
        self.staff_id = staff_id
        

    
    def checkWithdrawn(self):
        return self.isWithdrawn

    # @classmethod
    # def student_shortlist(cls, student_id):  # gets all the short list for a particular student
    #     return cls.query.filter_by(student_id=student_id).all()

    # @classmethod 
    # def position_shortlist(cls, position_id): # gets all the short list for a particular position
    #     return cls.query.filter_by(position_id=position_id).all()
        
    def toJSON(self):
        return{
            "id": self.id,
            "application_id": self.application_id,
            "staff_id": self.staff_id,
            "isWithdrawn": self.isWithdrawn
        }
    def __repr__(self):
        return f'<Shortlist id: {self.id} - Application ID: {self.application_id} - Staff ID: {self.staff_id} - isWithdrawn: {self.isWithdrawn}>'
      
    


