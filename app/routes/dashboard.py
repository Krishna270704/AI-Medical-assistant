from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.models import ChatSession, MedicalReport, Appointment, MedicationReminder, db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    # Fetch user's data
    recent_chats = ChatSession.query.filter_by(user_id=current_user.id).order_by(ChatSession.created_at.desc()).limit(5).all()
    reports = MedicalReport.query.filter_by(user_id=current_user.id).order_by(MedicalReport.uploaded_at.desc()).limit(5).all()
    appointments = Appointment.query.filter_by(user_id=current_user.id, status='upcoming').order_by(Appointment.appointment_date.asc()).limit(5).all()
    reminders = MedicationReminder.query.filter_by(user_id=current_user.id, status='active').all()
    
    return render_template('dashboard/index.html', 
                           chats=recent_chats, 
                           reports=reports, 
                           appointments=appointments, 
                           reminders=reminders)

@dashboard_bp.route('/chat/new')
@login_required
def new_chat():
    # Create a new chat session
    new_session = ChatSession(user_id=current_user.id, title="New Consultation")
    db.session.add(new_session)
    db.session.commit()
    return redirect(url_for('main.chat_view', session_id=new_session.id))

@dashboard_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.preferred_language = request.form.get('language')
        db.session.commit()
        from flask import flash
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('dashboard.profile'))
    return render_template('dashboard/profile.html')

@dashboard_bp.route('/dashboard/appointments/add', methods=['POST'])
@login_required
def add_appointment():
    from datetime import datetime
    doctor = request.form.get('doctor_name')
    specialty = request.form.get('specialty')
    date_str = request.form.get('appointment_date')
    if doctor and date_str:
        dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        apt = Appointment(user_id=current_user.id, doctor_name=doctor, specialty=specialty, appointment_date=dt)
        db.session.add(apt)
        db.session.commit()
    return redirect(url_for('dashboard.index'))

@dashboard_bp.route('/dashboard/reminders/add', methods=['POST'])
@login_required
def add_reminder():
    medication = request.form.get('medication_name')
    dosage = request.form.get('dosage')
    freq = request.form.get('frequency')
    time = request.form.get('time')
    if medication:
        rem = MedicationReminder(user_id=current_user.id, medicine_name=medication, dosage=dosage, frequency=freq, time=time)
        db.session.add(rem)
        db.session.commit()
    return redirect(url_for('dashboard.index'))
