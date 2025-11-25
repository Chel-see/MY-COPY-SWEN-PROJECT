from App.models import Shortlist, Position, Staff, Student, Application
from App.database import db

# 1. GET ELIGIBLE STUDENTS FOR A POSITION
def get_eligible_students(position_id):

    position = Position.query.filter_by(id=position_id).first()
    if not position:
        return {"error": "Position not found"}, 404

    gpa_required = position.gpa_requirement

    # Get all applications for the position
    applications = Application.query.filter_by(position_id=position_id).all()

    eligible = []
    for app in applications:
        student = Student.query.filter_by(id=app.student_id).first()
        if not student:
            continue

        # Check GPA requirement
        if gpa_required is None or student.gpa >= gpa_required:
            eligible.append({
                "student_id": student.id,
                "name": student.name,
                "gpa": student.gpa,
                "resume": student.resume,
                "status": app.status
            })

    return eligible, 200


# 2.STAFF SHORTLISTS A STUDENT (ONLY IF ELIGIBLE)
def shortlist_student(staff_id, student_id, position_id):

    staff = Staff.query.filter_by(id=staff_id).first()
    student = Student.query.filter_by(id=student_id).first()
    position = Position.query.filter_by(id=position_id).first()

    if not staff or not student or not position:
        return {"error": "Staff, student, or position not found"}, 404

    #Check if student applied for the position
    app = Application.query.filter_by(
        student_id=student_id,
        position_id=position_id
    ).first()

    if not app:
        return {"error": "Student has not applied for this position"}, 400

    # Check eligibility before shortlisting
    eligible_list, _ = get_eligible_students(position_id)
    eligible_ids = [s["student_id"] for s in eligible_list]

    if student_id not in eligible_ids:
        return {"error": "Student does not meet GPA requirement"}, 400

    #Prevent duplicate shortlisting
    existing = Shortlist.query.filter_by(
        student_id=student_id,
        position_id=position_id
    ).first()

    if existing:
        return {"error": "Student is already shortlisted"}, 400

    #Create shortlist entry
    shortlist = Shortlist(
        student_id=student_id,
        position_id=position_id,
        staff_id=staff_id,
        status="shortlisted"
    )

    db.session.add(shortlist)

    #Update application status to shortlisted
    app.setStatus("shortlisted")

    db.session.commit()
    return shortlist.toJSON(), 201


# 3. GET SHORTLISTS FOR A STUDENT
def get_shortlist_by_student(student_id):
    entries = Shortlist.query.filter_by(student_id=student_id).all()
    return [e.toJSON() for e in entries], 200


# 4. GET SHORTLISTS FOR A POSITION
def get_shortlist_by_position(position_id):
    entries = Shortlist.query.filter_by(position_id=position_id).all()
    return [e.toJSON() for e in entries], 200

