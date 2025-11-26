from App import db
from App.models.context import Context
from App.models.applied_state import AppliedState
from App.models.shortlisted_state import ShortListedState

class Application(db.Model):
    __tablename__ = "application"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    status = db.Column(db.String(15), default="applied", nullable=False)
    type = db.Column(db.String(50))

    def __init__(self, student_id, position_id):
        self.student_id = student_id
        self.position_id = position_id
        self.context = Context(AppliedState())
        self.status = self.context.state.name #applied

    def getStatus(self):
        return self.status

    def setStatus(self, newStatus:str): # transition to shortlisted / accepted / rejected states
        if isinstance(self.context.state, AppliedState) and newStatus=="shortlisted": #Applied -> Shortlisted
            self.context.setState(ShortListedState())
        elif isinstance(self.context.state, ShortListedState): #Shortlisted -> Accepted / Rejected
            self.context.state.next_decision(newStatus)
        self.status = self.context.state.name
        db.session.commit()

    def __repr__(self):
        return f'<Application id: {self.id} - Student ID: {self.student_id} - Position ID: {self.position_id} - Status: {self.status}>'

    __mapper_args__={'polymorphic_identity':'application',
                     'polymorphic_on':type}
