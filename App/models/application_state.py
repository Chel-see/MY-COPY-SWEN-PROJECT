
from abc import ABC, abstractmethod

class ApplicationState(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def next(self,application):
        pass

    @abstractmethod
    def previous(self,application):
        pass

    @abstractmethod
    def withdraw(self,application):
        pass















# from abc import ABC, abstractmethod

# class ApplicationState(ABC):
#     def __init__(self, name: str):
#         self.name = name
#         self.context = None

#     def set_context(self, context):
#         self.context = context

#     @abstractmethod
#     def next(self):
#         pass

#     @abstractmethod
#     def previous(self):
#         pass

#     def getStateName(self):
#         return self.name

#     @abstractmethod
#     def withdraw(self):
#         pass

#     @abstractmethod
#     def getMatchedCompanies(self):
#         pass