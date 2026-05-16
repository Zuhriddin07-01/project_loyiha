# 🏥 ShifoMed - Hospital Appointment Booking Platform

ShifoMed is a modern hospital appointment booking platform built with Flask. Patients can browse doctors, view their profiles, and book appointments online. Administrators can manage doctors, schedules, and appointments through a dedicated admin panel.

## ✨ Features

- **Patient Booking**: Browse doctors by specialization, view profiles, and book appointments
- **Doctor Management**: Add, edit, and remove doctors with detailed profiles
- **Schedule System**: Flexible weekly schedules with configurable time slots
- **Admin Panel**: Dashboard with statistics, appointment management, and doctor CRUD
- **Responsive Design**: Modern UI with Bootstrap 5 and custom CSS
- **Real-time Slots**: Dynamic time slot availability checking via API

## 🛠 Tech Stack

- **Backend**: Python, Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Auth**: Flask-Login for admin authentication
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Icons**: Bootstrap Icons

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/project_loyiha.git
cd project_loyiha
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Seed the database (optional)
```bash
python seed_data.py
```

### 5. Run the application
```bash
python app.py
```

The app will be available at `http://localhost:5000`

## 👤 Admin Access

After running `seed_data.py`:
- **URL**: `/admin/login`
- **Username**: `admin`
- **Password**: `admin123`

## 📁 Project Structure

```
project_loyiha/
├── app.py              # Main Flask application with routes
├── models.py           # SQLAlchemy database models
├── config.py           # Application configuration
├── seed_data.py        # Database seeding script
├── requirements.txt    # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css   # Custom styles
│   └── js/
│       └── main.js     # Client-side JavaScript
└── templates/
    ├── base.html           # Base template with navbar & footer
    ├── index.html          # Home page
    ├── doctors.html        # Doctors listing page
    ├── doctor_detail.html  # Doctor profile page
    ├── booking.html        # Appointment booking page
    ├── booking_success.html# Booking confirmation
    └── admin/
        ├── base_admin.html  # Admin layout
        ├── login.html       # Admin login
        ├── dashboard.html   # Admin dashboard
        ├── doctors.html     # Manage doctors
        ├── doctor_form.html # Add/Edit doctor form
        └── appointments.html# Manage appointments
```

## 📝 License

This project is open source and available under the [MIT License](LICENSE).
