from App.models import Position, Employer, Student, Application
#from  App.controllers.shortlist import get_eligible_students
from App.database import db

# responsible for just creating positions , automatic mathcing is handled when an application is created. The studnets auto-applies are all the psoitions they qualify for 
def open_position(user_id, title, number_of_positions=1, gpa_requirement=None):
    employer = Employer.query.get(user_id)
    if not employer:
        return None
    
    new_position = Position(title=title, employer_id=employer.id, number_of_positions=number_of_positions, gpa_requirement=gpa_requirement)
    db.session.add(new_position)
    try:
        db.session.commit()
        print(f"Position {new_position.id} created successfully!")
        #get_eligible_students(new_position)
        return new_position
    except Exception as e:
        db.session.rollback()
        return None

          

def get_position(position_id):  # needed for testing 
    return Position.query.get(position_id)

def get_position_by_title(title):
    return Position.query.filter_by(title=title).first() # needed for testing 

def get_positions_by_employer(user_id):
    employer = Employer.query.get(user_id)
    return Position.query.filter_by(employer_id=employer.id).all()

def get_all_positions_json():
    positions = Position.query.all()
    if positions:
        return [position.toJSON() for position in positions]
    return []

def get_positions_by_employer_json(user_id):
    employer = Employer.query.filter_by(id=user_id).first()
    positions = db.session.query(Position).filter_by(employer_id=employer.id).all()
    if positions:
        return [position.toJSON() for position in positions]
    return []
