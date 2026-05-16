from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class Admin(UserMixin, db.Model):
    """Admin user model for managing the system."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Admin {self.username}>'


class Doctor(db.Model):
    """Doctor model with profile information."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=4.5)
    photo = db.Column(db.String(300), default='')
    bio = db.Column(db.Text, default='')
    education = db.Column(db.String(300), default='')
    phone = db.Column(db.String(20), default='')
    email = db.Column(db.String(120), default='')
    consultation_fee = db.Column(db.Integer, default=0)
    available_days = db.Column(db.String(200), default='')  # comma-separated days
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    schedules = db.relationship('Schedule', backref='doctor', lazy=True, cascade='all, delete-orphan')
    appointments = db.relationship('Appointment', backref='doctor', lazy=True, cascade='all, delete-orphan')

    def get_available_days_list(self):
        if self.available_days:
            return [d.strip() for d in self.available_days.split(',')]
        return []

    def __repr__(self):
        return f'<Doctor {self.name}>'


class Schedule(db.Model):
    """Weekly schedule for each doctor."""
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = db.Column(db.String(5), nullable=False)  # "09:00"
    end_time = db.Column(db.String(5), nullable=False)    # "17:00"
    slot_duration = db.Column(db.Integer, default=30)      # minutes
    is_active = db.Column(db.Boolean, default=True)

    DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    def get_day_name(self):
        return self.DAY_NAMES[self.day_of_week] if 0 <= self.day_of_week <= 6 else ''

    def generate_time_slots(self):
        """Generate available time slots based on start/end time and duration."""
        slots = []
        start_h, start_m = map(int, self.start_time.split(':'))
        end_h, end_m = map(int, self.end_time.split(':'))
        current = start_h * 60 + start_m
        end = end_h * 60 + end_m
        while current + self.slot_duration <= end:
            h, m = divmod(current, 60)
            slots.append(f'{h:02d}:{m:02d}')
            current += self.slot_duration
        return slots

    def __repr__(self):
        return f'<Schedule Doctor:{self.doctor_id} Day:{self.day_of_week}>'


class Appointment(db.Model):
    """Patient appointment booking."""
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)      # "2024-12-25"
    time_slot = db.Column(db.String(5), nullable=False)   # "09:00"
    patient_name = db.Column(db.String(100), nullable=False)
    patient_phone = db.Column(db.String(20), nullable=False)
    patient_age = db.Column(db.Integer, nullable=False)
    patient_gender = db.Column(db.String(10), nullable=False)
    notes = db.Column(db.Text, default='')
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Unique constraint to prevent double booking
    __table_args__ = (
        db.UniqueConstraint('doctor_id', 'date', 'time_slot', name='unique_booking'),
    )

    def __repr__(self):
        return f'<Appointment {self.patient_name} - {self.date} {self.time_slot}>'
