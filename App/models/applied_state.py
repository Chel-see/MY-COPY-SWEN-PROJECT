from App.models.application_state import ApplicationState



class AppliedState(ApplicationState):
    def __init__(self):
        super().__init__("applied")

    def next(self, app):
        # Applied -> Shortlisted
        from App.models.shortlisted_state import ShortListedState
        app.set_state(ShortListedState())

    def previous(self, app):
        return None  # no previous
    
    def reject(self, app):
            from App.models.rejected_state import RejectedState
            app.set_state(RejectedState())

    def withdraw(self, app):
        from App.models.rejected_state import RejectedState
        app.set_state(RejectedState())
















# from App.models.application_state import ApplicationState


# class AppliedState(ApplicationState):

#     def __init__(self):
#         super().__init__("applied")

  
#     # Applied → Shortlisted
#     def next(self):
#         if self.context:
#             from App.models.shortlisted_state import ShortListedState
#             self.context.setState(ShortListedState())

#     # Applied has no previous state
#     def previous(self):
#         return None

#     # withdraw() always means rejection
#     def withdraw(self):
#         if self.context:
#             from App.models.rejected_state import RejectedState
#             self.context.setState(RejectedState())

#     # No special accept/reject behavior here
#     def accept(self):
#         return None

#     def reject(self):
#         if self.context:
#             from App.models.rejected_state import RejectedState
#             self.context.setState(RejectedState())

  
#     def getMatchedCompanies(self):
#         return []
