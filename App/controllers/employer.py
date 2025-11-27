from App.models.employer import Employer
from App.database import db
from App.models import Student, Shortlist, Position
from App.controllers.user import *
from App.models.application import Application

def create_employer(username, password, email, company, phone_number):
  newEmployer = Employer(username, password, email, company, phone_number)
  db.session.add(newEmployer)
  db.session.commit()
  return newEmployer

def decide_shortlist(student_id, position_id, decision):
  student = db.session.query(Student).filter_by(user_id=student_id).first()
  shortlist = db.session.query(Shortlist).filter_by(student_id=student.id, position_id=position_id, status ="pending").first()
  position = db.session.query(Position).filter(Position.id==position_id, Position.number_of_positions > 0).first()
  
  application = db.session.query(Application).filter_by(student_id=student.id, position_id=position.id).first()
  
  if shortlist and position and application:
    shortlist.update_status(decision)
    if decision=="accept":
      position.update_number_of_positions(position.number_of_positions - 1)
    application.setStatus(decision)
    db.session.commit()
    return shortlist
  return False
