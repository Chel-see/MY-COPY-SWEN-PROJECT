from models.application_state import ApplicationState
from models.rejected_state import RejectedState
from models.shortlisted_state import ShortlistedState


class AcceptedState(ApplicationState):
    def __init__(self):
        super().__init__("Accepted")

    def next(self):
        return None  # No direct next state from Accepted

    def previous(self):
        if self.context:
            self.context.setState(ShortlistedState())  # No previous state from Accepted

    def acceptOffer(self):
        self.name="Confirmed"

    def withdraw(self):
        if self.context: # check if there is a valid context
            self.context.setState(RejectedState())
            
    def getMatchedCompanies(self):
        return []  # No matched companies for accepted applications
