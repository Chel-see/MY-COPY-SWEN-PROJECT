from App.models import Position, Employer, Student, Application
from App.database import db

def open_position(user_id, title, number_of_positions=1, gpa_requirement=None):
    employer = Employer.query.filter_by(id=user_id).first()
    if not employer:
        return None
    
    new_position = Position(title=title, employer_id=employer.id, number_of_positions=number_of_positions, gpa_requirement=gpa_requirement)
    db.session.add(new_position)
    try:
        db.session.commit()
        getEligibleStudents(new_position)
        return new_position
    except Exception as e:
        db.session.rollback()
        return None

def getEligibleStudents(position):
    students = db.session.query(Student).all()
    eligible_students=[]
    for student in students:
        if student.gpa >= position.gpa_requirement or position.gpa_requirement is None:
            application = Application(student_id=student.id, position_id=position.id)
            db.session.add(application)
            eligible_students.append(student)
    db.session.commit()
    return eligible_students            

def get_positions_by_employer(user_id):
    employer = Employer.query.filter_by(id=user_id).first()
    return db.session.query(Position).filter_by(employer_id=employer.id).all()

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
