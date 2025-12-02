from App.database import db


class Application(db.Model):
    __tablename__ = "application"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    status = db.Column(db.String(15), nullable=False)

    # runtime-only state object (not stored in DB)
    state = None  

    def __init__(self, student_id, position_id):
        self.student_id = student_id
        self.position_id = position_id

        # initial state
        from App.models.applied_state import AppliedState
        self.set_state(AppliedState())

    # ---------- Delegate to State ----------
    def next(self, decision=None):
        """Move to next state."""
        return self.state.next(self, decision)

    def previous(self):
        return self.state.previous(self)

    def withdraw(self):
        return self.state.withdraw(self)

    # ---------- State setter ----------
    def set_state(self, new_state):
        self.state = new_state
        self.status = new_state.name  # Update DB string
        db.session.add(self)
        db.session.commit()

    def getStatus(self):
        return self.status

    def __repr__(self):
        return f"<Application {self.id} - Status: {self.status}>"































# from App.database import db
# from App.models.context import Context
# from App.models.applied_state import AppliedState
# from App.models.shortlisted_state import ShortListedState
# from App.models.rejected_state import RejectedState

# class Application(db.Model):
#     __tablename__ = "application"

#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
#     position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
#     status = db.Column(db.String(15), default="applied", nullable=False)
#     type = db.Column(db.String(50))

#     def __init__(self, student_id, position_id):
#         self.student_id = student_id
#         self.position_id = position_id
#         self.context = Context(AppliedState())
#         self.status = self.context.state.name #applied

#     def getStatus(self):
#         return self.status

#     def setStatus(self, newStatus:str): # transition to shortlisted / accepted / rejected states
#         if isinstance(self.context.state, AppliedState) and newStatus=="shortlisted": #Applied -> Shortlisted
#             self.context.setState(ShortListedState())
#         elif isinstance(self.context.state, ShortListedState): #Shortlisted -> Accepted / Rejected
#             self.context.state.next_decision(newStatus)
#         elif isinstance(self.context.state, ShortListedState()) and newStatus=="applied":
#             self.context.state.previous()
#         elif isinstance(self.context.state, RejectedState()) and newStatus=="shortlisted":
#             self.context.state.previous()
#         elif newStatus == "withdrawn": #Student withdraws from position
#             self.context.setState(RejectedState())
#         self.status = self.context.state.name
#         db.session.commit()

#     def __repr__(self):
#         return f'<Application id: {self.id} - Student ID: {self.student_id} - Position ID: {self.position_id} - Status: {self.status}>'

