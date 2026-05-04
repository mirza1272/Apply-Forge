# ApplyForge - Job Board Platform

A Django-based job board connecting employers with job seekers.

## 🛠️ Installation (Local Development)

### Prerequisites
- Python 3.10+
- PostgreSQL (or SQLite for testing)
- Git (optional)

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/mirza1272/Apply-Forge.git
   cd Apply-Forge

## Create virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

## Install dependencies

pip install -r requirements.txt

## Configure environment

Create .env file:
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3  # For PostgreSQL: postgres://user:pass@localhost:5432/dbname

## Run migrations
python manage.py migrate
## Create superuser
python manage.py createsuperuser
## Run development server
python manage.py runserver
Access at: http://localhost:8000

Apply-Forge/
├── applyforge/          # Main project folder
├── jobs/                # Job listings app
├── accounts/            # User accounts app
├── static/              # CSS, JS, images
├── templates/           # HTML templates
├── requirements.txt     # Python dependencies
└── manage.py            # Django management script
