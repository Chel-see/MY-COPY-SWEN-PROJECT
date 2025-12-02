from App.models.application_state import ApplicationState

class RejectedState(ApplicationState):
    def __init__(self, reason="Not specified"):
        super().__init__("Rejected")
        self.reason = reason

    def next(self, app):
        return None  # No next state from Rejected

    def previous(self, app):
        
            from App.models.shortlisted_state import ShortListedState
            app.set_state(ShortListedState())
        
    def viewReason(self):
        return self.reason

    def withdraw(self, app):
        return None  # Cannot withdraw a rejected application

    def getMatchedCompanies(self):
        return []  # No matched companies for rejected applications