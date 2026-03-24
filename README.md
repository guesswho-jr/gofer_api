# 🛒 Gofer API

A backend REST API for a shopping application, built with Django/Django rest framework.

## 📋 What It Does

- Handles shopping application backend logic
- Manages user accounts and authentication
- Provides dashboard data and analytics
- Processes and logs application activity

## 🛠️ Tech Stack

- **Language:** Python
- **Framework:** Django
- **Type:** REST API

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip
- Virtualenv (recommended)

### Installation

1. Clone the repository
   git clone git@github.com:guesswho-jr/gofer_api.git

2. Navigate into the project
   cd gofer_api

3. Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate

4. Install dependencies
   pip install -r requirements.txt


6. Run migrations
   python manage.py migrate

7. Start the server
   python manage.py runserver

## 📁 Project Structure

├── Gofer_main/       # Main Django project settings
├── accounts/         # User accounts & authentication
├── dashboard/        # Dashboard endpoints
├── middleware/       # Custom middleware
├── story/            # Story/feed related logic
├── utils/            # Utility functions
├── scripts/          # Helper scripts
├── Logs/             # Application logs
├── manage.py         # Django management entry point
└── .gitignore

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Debug mode toggle |
| `DATABASE_URL` | Database connection string |
| `ALLOWED_HOSTS` | Allowed hostnames |

