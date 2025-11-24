
class Context:
    def __init__(self, initial_state):  # first state the content would be assigned to. we can switch form this state to others
        self.state = initial_state  # i dont need to pre-declare the state attribute in python
        self.state.setContext(self)   

    def setState(self, state):
        self.state = state
        self.state.setContext(self)

    def next(self):
        return self.state.next()

    def previous(self):
        return self.state.previous()

    def withdraw(self):
        return self.state.withdraw()

    def getStateName(self):
        return self.state.getStateName()
    
    def getMatchedCompanies(self):
        return self.state.getMatchedCompanies()