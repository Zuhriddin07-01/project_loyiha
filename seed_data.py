"""Seed script to populate the database with sample doctors, schedules, and admin user."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app
from models import db, Admin, Doctor, Schedule

DOCTORS = [
    {
        'name': 'Dr. Aziz Karimov',
        'specialization': 'Cardiology',
        'experience': 15,
        'rating': 4.9,
        'photo': 'https://ui-avatars.com/api/?name=Aziz+Karimov&background=0077B6&color=fff&size=256&bold=true&format=svg',
        'bio': 'Dr. Aziz Karimov is a highly experienced cardiologist specializing in interventional cardiology and heart failure management. He has performed over 2,000 cardiac procedures.',
        'education': 'Tashkent Medical Academy, Fellowship at Johns Hopkins University',
        'phone': '+998 90 123 4567',
        'email': 'a.karimov@shifomed.uz',
        'consultation_fee': 150000,
        'available_days': 'Monday,Tuesday,Wednesday,Thursday,Friday',
    },
    {
        'name': 'Dr. Nilufar Rahimova',
        'specialization': 'Neurology',
        'experience': 12,
        'rating': 4.8,
        'photo': 'https://ui-avatars.com/api/?name=Nilufar+Rahimova&background=00B4D8&color=fff&size=256&bold=true&format=svg',
        'bio': 'Dr. Nilufar Rahimova is a leading neurologist with expertise in stroke management, epilepsy treatment, and neurodegenerative diseases.',
        'education': 'Samarkand State Medical University, Residency at Charité Berlin',
        'phone': '+998 91 234 5678',
        'email': 'n.rahimova@shifomed.uz',
        'consultation_fee': 140000,
        'available_days': 'Monday,Wednesday,Thursday,Friday',
    },
    {
        'name': 'Dr. Bobur Toshmatov',
        'specialization': 'Orthopedics',
        'experience': 18,
        'rating': 4.7,
        'photo': 'https://ui-avatars.com/api/?name=Bobur+Toshmatov&background=023E8A&color=fff&size=256&bold=true&format=svg',
        'bio': 'Dr. Bobur Toshmatov is a senior orthopedic surgeon specializing in joint replacement, sports injuries, and spinal surgery with minimally invasive techniques.',
        'education': 'Tashkent Pediatric Medical Institute, Fellowship at Mayo Clinic',
        'phone': '+998 93 345 6789',
        'email': 'b.toshmatov@shifomed.uz',
        'consultation_fee': 160000,
        'available_days': 'Monday,Tuesday,Thursday,Saturday',
    },
    {
        'name': 'Dr. Malika Usmanova',
        'specialization': 'Pediatrics',
        'experience': 10,
        'rating': 4.9,
        'photo': 'https://ui-avatars.com/api/?name=Malika+Usmanova&background=10B981&color=fff&size=256&bold=true&format=svg',
        'bio': 'Dr. Malika Usmanova is a dedicated pediatrician specializing in childhood development, infectious diseases in children, and neonatal care.',
        'education': 'Bukhara State Medical Institute, Great Ormond Street Hospital London',
        'phone': '+998 94 456 7890',
        'email': 'm.usmanova@shifomed.uz',
        'consultation_fee': 120000,
        'available_days': 'Monday,Tuesday,Wednesday,Friday,Saturday',
    },
    {
        'name': 'Dr. Jamshid Aliyev',
        'specialization': 'Dentistry',
        'experience': 8,
        'rating': 4.6,
        'photo': 'https://ui-avatars.com/api/?name=Jamshid+Aliyev&background=0096C7&color=fff&size=256&bold=true&format=svg',
        'bio': 'Dr. Jamshid Aliyev is a skilled dentist specializing in cosmetic dentistry, dental implants, and orthodontics using the latest technology.',
        'education': 'Tashkent State Dental Institute, Advanced Training in South Korea',
        'phone': '+998 95 567 8901',
        'email': 'j.aliyev@shifomed.uz',
        'consultation_fee': 100000,
        'available_days': 'Monday,Tuesday,Wednesday,Thursday,Friday,Saturday',
    },
    {
        'name': 'Dr. Dilorom Nazarova',
        'specialization': 'Dermatology',
        'experience': 14,
        'rating': 4.8,
        'photo': 'https://ui-avatars.com/api/?name=Dilorom+Nazarova&background=48CAE4&color=fff&size=256&bold=true&format=svg',
        'bio': 'Dr. Dilorom Nazarova is a renowned dermatologist with expertise in clinical and cosmetic dermatology, treating conditions from acne to skin cancer.',
        'education': 'Andijan State Medical Institute, Fellowship at Seoul National University Hospital',
        'phone': '+998 97 678 9012',
        'email': 'd.nazarova@shifomed.uz',
        'consultation_fee': 130000,
        'available_days': 'Tuesday,Wednesday,Thursday,Friday',
    },
    {
        'name': 'Dr. Rustam Mirzayev',
        'specialization': 'General Surgery',
        'experience': 20,
        'rating': 4.9,
        'photo': 'https://ui-avatars.com/api/?name=Rustam+Mirzayev&background=003459&color=fff&size=256&bold=true&format=svg',
        'bio': 'Dr. Rustam Mirzayev is one of the most experienced general surgeons in the region, specializing in laparoscopic surgery and emergency surgical care.',
        'education': 'First Tashkent State Medical Institute, Training at Cleveland Clinic',
        'phone': '+998 90 789 0123',
        'email': 'r.mirzayev@shifomed.uz',
        'consultation_fee': 180000,
        'available_days': 'Monday,Tuesday,Wednesday,Thursday,Friday',
    },
    {
        'name': 'Dr. Zulfiya Hasanova',
        'specialization': 'Ophthalmology',
        'experience': 11,
        'rating': 4.7,
        'photo': 'https://ui-avatars.com/api/?name=Zulfiya+Hasanova&background=0077B6&color=fff&size=256&bold=true&format=svg',
        'bio': 'Dr. Zulfiya Hasanova is an ophthalmologist specializing in LASIK surgery, cataract treatment, and pediatric eye care.',
        'education': 'Tashkent Medical Academy, Fellowship at Moorfields Eye Hospital London',
        'phone': '+998 91 890 1234',
        'email': 'z.hasanova@shifomed.uz',
        'consultation_fee': 135000,
        'available_days': 'Monday,Wednesday,Friday,Saturday',
    },
    {
        'name': 'Dr. Sardor Yuldashev',
        'specialization': 'Urology',
        'experience': 13,
        'rating': 4.6,
        'photo': 'https://ui-avatars.com/api/?name=Sardor+Yuldashev&background=023E8A&color=fff&size=256&bold=true&format=svg',
        'bio': 'Dr. Sardor Yuldashev is a board-certified urologist specializing in minimally invasive urological surgery and kidney stone management.',
        'education': 'Samarkand State Medical University, Asan Medical Center Seoul',
        'phone': '+998 93 901 2345',
        'email': 's.yuldashev@shifomed.uz',
        'consultation_fee': 145000,
        'available_days': 'Monday,Tuesday,Thursday,Friday',
    },
    {
        'name': 'Dr. Kamola Ibragimova',
        'specialization': 'Gynecology',
        'experience': 16,
        'rating': 4.8,
        'photo': 'https://ui-avatars.com/api/?name=Kamola+Ibragimova&background=00B4D8&color=fff&size=256&bold=true&format=svg',
        'bio': 'Dr. Kamola Ibragimova is a leading gynecologist with extensive experience in prenatal care, high-risk pregnancies, and minimally invasive surgeries.',
        'education': 'Tashkent Pediatric Medical Institute, Fellowship at Imperial College London',
        'phone': '+998 94 012 3456',
        'email': 'k.ibragimova@shifomed.uz',
        'consultation_fee': 140000,
        'available_days': 'Monday,Tuesday,Wednesday,Thursday,Friday',
    },
]

DAY_MAP = {
    'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
    'Friday': 4, 'Saturday': 5, 'Sunday': 6
}


def seed():
    with app.app_context():
        print('Clearing existing data...')
        Appointment = __import__('models', fromlist=['Appointment']).Appointment
        db.session.query(Appointment).delete()
        db.session.query(Schedule).delete()
        db.session.query(Doctor).delete()
        db.session.query(Admin).delete()
        db.session.commit()

        # Create admin
        admin = Admin(username='admin', email='admin@shifomed.uz')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print(f'Admin created: admin / admin123')

        # Create doctors and schedules
        for doc_data in DOCTORS:
            doctor = Doctor(**doc_data)
            db.session.add(doctor)
            db.session.commit()

            for day_name in doctor.get_available_days_list():
                if day_name in DAY_MAP:
                    schedule = Schedule(
                        doctor_id=doctor.id,
                        day_of_week=DAY_MAP[day_name],
                        start_time='09:00',
                        end_time='17:00',
                        slot_duration=30,
                        is_active=True
                    )
                    db.session.add(schedule)

            db.session.commit()
            print(f'Created: {doctor.name} ({doctor.specialization})')

        print(f'\n✅ Database seeded successfully!')
        print(f'─────────────────────────────────')
        print(f'Admin Login: admin / admin123')
        print(f'Doctors: {len(DOCTORS)} created')
        print(f'─────────────────────────────────')


if __name__ == '__main__':
    seed()
