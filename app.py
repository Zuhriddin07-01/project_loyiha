from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, Admin, Doctor, Schedule, Appointment
from datetime import datetime, date

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


# ─── PUBLIC ROUTES ───────────────────────────────────────────

@app.route('/')
def home():
    """Home page with featured doctors and services."""
    featured_doctors = Doctor.query.filter_by(is_active=True).order_by(Doctor.rating.desc()).limit(4).all()
    total_doctors = Doctor.query.filter_by(is_active=True).count()
    total_appointments = Appointment.query.count()
    specializations = db.session.query(Doctor.specialization).filter_by(is_active=True).distinct().all()
    return render_template('index.html',
                           featured_doctors=featured_doctors,
                           total_doctors=total_doctors,
                           total_appointments=total_appointments,
                           total_specializations=len(specializations))


@app.route('/doctors')
def doctors():
    """Doctors listing page with filtering."""
    spec_filter = request.args.get('specialization', 'all')
    search = request.args.get('search', '')

    query = Doctor.query.filter_by(is_active=True)

    if spec_filter and spec_filter != 'all':
        query = query.filter_by(specialization=spec_filter)

    if search:
        query = query.filter(
            db.or_(
                Doctor.name.ilike(f'%{search}%'),
                Doctor.specialization.ilike(f'%{search}%')
            )
        )

    doctors_list = query.order_by(Doctor.rating.desc()).all()
    specializations = db.session.query(Doctor.specialization).filter_by(is_active=True).distinct().all()
    specs = [s[0] for s in specializations]

    return render_template('doctors.html',
                           doctors=doctors_list,
                           specializations=specs,
                           current_filter=spec_filter,
                           search=search)


@app.route('/doctor/<int:doctor_id>')
def doctor_detail(doctor_id):
    """Doctor detail page with schedule and booking option."""
    doctor = Doctor.query.get_or_404(doctor_id)
    schedules = Schedule.query.filter_by(doctor_id=doctor_id, is_active=True).order_by(Schedule.day_of_week).all()
    return render_template('doctor_detail.html', doctor=doctor, schedules=schedules)


@app.route('/booking/<int:doctor_id>', methods=['GET', 'POST'])
def booking(doctor_id):
    """Booking page - select date/time and fill patient info."""
    doctor = Doctor.query.get_or_404(doctor_id)
    schedules = Schedule.query.filter_by(doctor_id=doctor_id, is_active=True).order_by(Schedule.day_of_week).all()

    if request.method == 'POST':
        try:
            appt_date = request.form.get('date')
            time_slot = request.form.get('time_slot')
            patient_name = request.form.get('patient_name', '').strip()
            patient_phone = request.form.get('patient_phone', '').strip()
            patient_age = request.form.get('patient_age')
            patient_gender = request.form.get('patient_gender')
            notes = request.form.get('notes', '').strip()

            # Validation
            if not all([appt_date, time_slot, patient_name, patient_phone, patient_age, patient_gender]):
                flash('Please fill in all required fields.', 'danger')
                return redirect(url_for('booking', doctor_id=doctor_id))

            # Check for double booking
            existing = Appointment.query.filter_by(
                doctor_id=doctor_id,
                date=appt_date,
                time_slot=time_slot
            ).filter(Appointment.status != 'cancelled').first()

            if existing:
                flash('This time slot is already booked. Please choose another time.', 'danger')
                return redirect(url_for('booking', doctor_id=doctor_id))

            appointment = Appointment(
                doctor_id=doctor_id,
                date=appt_date,
                time_slot=time_slot,
                patient_name=patient_name,
                patient_phone=patient_phone,
                patient_age=int(patient_age),
                patient_gender=patient_gender,
                notes=notes
            )
            db.session.add(appointment)
            db.session.commit()

            flash('Appointment booked successfully! We will contact you shortly.', 'success')
            return redirect(url_for('booking_success', appointment_id=appointment.id))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('booking', doctor_id=doctor_id))

    return render_template('booking.html', doctor=doctor, schedules=schedules, today=date.today().isoformat())


@app.route('/booking/success/<int:appointment_id>')
def booking_success(appointment_id):
    """Booking confirmation page."""
    appointment = Appointment.query.get_or_404(appointment_id)
    doctor = Doctor.query.get(appointment.doctor_id)
    return render_template('booking_success.html', appointment=appointment, doctor=doctor)


@app.route('/api/available-slots/<int:doctor_id>/<string:selected_date>')
def get_available_slots(doctor_id, selected_date):
    """API endpoint: returns available time slots for a given doctor and date."""
    try:
        dt = datetime.strptime(selected_date, '%Y-%m-%d')
        day_of_week = dt.weekday()  # 0=Monday

        schedule = Schedule.query.filter_by(
            doctor_id=doctor_id,
            day_of_week=day_of_week,
            is_active=True
        ).first()

        if not schedule:
            return jsonify({'slots': [], 'message': 'Doctor is not available on this day'})

        all_slots = schedule.generate_time_slots()

        # Get booked slots (excluding cancelled)
        booked = Appointment.query.filter_by(
            doctor_id=doctor_id,
            date=selected_date
        ).filter(Appointment.status != 'cancelled').all()
        booked_times = [a.time_slot for a in booked]

        slots = [{'time': s, 'available': s not in booked_times} for s in all_slots]

        return jsonify({'slots': slots})
    except Exception as e:
        return jsonify({'slots': [], 'error': str(e)})


# ─── ADMIN ROUTES ────────────────────────────────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page."""
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.check_password(password):
            login_user(admin)
            flash('Welcome back, Admin!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('admin/login.html')


@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))


@app.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard with statistics."""
    total_doctors = Doctor.query.count()
    total_appointments = Appointment.query.count()
    pending_appointments = Appointment.query.filter_by(status='pending').count()
    confirmed_appointments = Appointment.query.filter_by(status='confirmed').count()
    recent_appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(10).all()

    return render_template('admin/dashboard.html',
                           total_doctors=total_doctors,
                           total_appointments=total_appointments,
                           pending_appointments=pending_appointments,
                           confirmed_appointments=confirmed_appointments,
                           recent_appointments=recent_appointments)


@app.route('/admin/doctors')
@login_required
def admin_doctors():
    """Admin - manage doctors list."""
    doctors_list = Doctor.query.order_by(Doctor.name).all()
    return render_template('admin/doctors.html', doctors=doctors_list)


@app.route('/admin/doctor/add', methods=['GET', 'POST'])
@login_required
def admin_add_doctor():
    """Admin - add a new doctor."""
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            specialization = request.form.get('specialization', '').strip()
            experience = int(request.form.get('experience', 0))
            rating = float(request.form.get('rating', 4.5))
            bio = request.form.get('bio', '').strip()
            education = request.form.get('education', '').strip()
            phone = request.form.get('phone', '').strip()
            email = request.form.get('email', '').strip()
            consultation_fee = int(request.form.get('consultation_fee', 0))
            available_days = ','.join(request.form.getlist('available_days'))

            # Generate avatar URL
            photo = f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=0077B6&color=fff&size=256&bold=true"

            doctor = Doctor(
                name=name, specialization=specialization, experience=experience,
                rating=rating, photo=photo, bio=bio, education=education,
                phone=phone, email=email, consultation_fee=consultation_fee,
                available_days=available_days
            )
            db.session.add(doctor)
            db.session.commit()

            # Create default schedules for available days
            day_map = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
                       'Friday': 4, 'Saturday': 5, 'Sunday': 6}
            for day in doctor.get_available_days_list():
                if day in day_map:
                    schedule = Schedule(
                        doctor_id=doctor.id, day_of_week=day_map[day],
                        start_time='09:00', end_time='17:00', slot_duration=30
                    )
                    db.session.add(schedule)
            db.session.commit()

            flash(f'Doctor {name} added successfully!', 'success')
            return redirect(url_for('admin_doctors'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding doctor: {str(e)}', 'danger')

    return render_template('admin/doctor_form.html', doctor=None, action='Add')


@app.route('/admin/doctor/edit/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_doctor(doctor_id):
    """Admin - edit existing doctor."""
    doctor = Doctor.query.get_or_404(doctor_id)

    if request.method == 'POST':
        try:
            doctor.name = request.form.get('name', '').strip()
            doctor.specialization = request.form.get('specialization', '').strip()
            doctor.experience = int(request.form.get('experience', 0))
            doctor.rating = float(request.form.get('rating', 4.5))
            doctor.bio = request.form.get('bio', '').strip()
            doctor.education = request.form.get('education', '').strip()
            doctor.phone = request.form.get('phone', '').strip()
            doctor.email = request.form.get('email', '').strip()
            doctor.consultation_fee = int(request.form.get('consultation_fee', 0))
            doctor.available_days = ','.join(request.form.getlist('available_days'))
            doctor.photo = f"https://ui-avatars.com/api/?name={doctor.name.replace(' ', '+')}&background=0077B6&color=fff&size=256&bold=true"

            db.session.commit()
            flash(f'Doctor {doctor.name} updated successfully!', 'success')
            return redirect(url_for('admin_doctors'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating doctor: {str(e)}', 'danger')

    return render_template('admin/doctor_form.html', doctor=doctor, action='Edit')


@app.route('/admin/doctor/delete/<int:doctor_id>', methods=['POST'])
@login_required
def admin_delete_doctor(doctor_id):
    """Admin - delete a doctor."""
    doctor = Doctor.query.get_or_404(doctor_id)
    name = doctor.name
    db.session.delete(doctor)
    db.session.commit()
    flash(f'Doctor {name} deleted successfully.', 'info')
    return redirect(url_for('admin_doctors'))


@app.route('/admin/appointments')
@login_required
def admin_appointments():
    """Admin - view all appointments."""
    status_filter = request.args.get('status', 'all')
    query = Appointment.query

    if status_filter and status_filter != 'all':
        query = query.filter_by(status=status_filter)

    appointments = query.order_by(Appointment.created_at.desc()).all()
    return render_template('admin/appointments.html',
                           appointments=appointments,
                           current_filter=status_filter)


@app.route('/admin/appointment/<int:appt_id>/status', methods=['POST'])
@login_required
def admin_update_status(appt_id):
    """Admin - update appointment status."""
    appointment = Appointment.query.get_or_404(appt_id)
    new_status = request.form.get('status')
    if new_status in ['pending', 'confirmed', 'cancelled', 'completed']:
        appointment.status = new_status
        db.session.commit()
        flash(f'Appointment status updated to {new_status}.', 'success')
    return redirect(url_for('admin_appointments'))


# ─── INITIALIZE DATABASE ─────────────────────────────────────

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
