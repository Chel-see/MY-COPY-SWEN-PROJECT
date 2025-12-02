from App.models.application_state import ApplicationState  # App added new change


class AcceptedState(ApplicationState):
    def __init__(self):
        super().__init__("Accepted")

    def next(self,app):
        return None  # No direct next state from Accepted

    def previous(self,app):
       
            from models.shortlisted_state import ShortListedState
            app.set_state(ShortListedState())  # No previous state from Accepted

    def acceptOffer(self):
        self.name="Confirmed"

    def withdraw(self,app):
        
            from models.rejected_state import RejectedState
            app.set_tate(RejectedState())
            
    def getMatchedCompanies(self):
        return []  # No matched companies for accepted applications
