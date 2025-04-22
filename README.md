# Internship Application Tracker for Universities

A Flask-based web application that helps university students track their internship applications while providing administrators with valuable insights into application statistics.

## Features

### For Students
- Track internship applications
- Manage application deadlines
- Add notes and status updates
- Access interview tips and resources
- Dashboard with application overview

### For Administrators
- View application statistics
- Export student application data
- Track popular companies and success rates
- Monitor student engagement

## Tech Stack

- **Backend**: Flask 3.0.2
- **Database**: SQLAlchemy with SQLite
- **Frontend**: Bootstrap 3.3.7
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Additional**: Flask-Migrate, email-validator

## Project Structure

```
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models
│   ├── auth/                # Authentication blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   └── main/               # Main application blueprint
│       ├── __init__.py
│       └── routes.py
├── config.py               # Configuration settings
├── requirements.txt        # Project dependencies
└── run.py                 # Application entry point
```

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Internship-Application-Tracker-for-Universities.git
cd Internship-Application-Tracker-for-Universities
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. Run the application:
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Environment Variables

Create a `.env` file in the root directory with the following variables:
```
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///app.db
```

## Database Models

### User Model
- Username
- Email
- Password (hashed)
- Admin status
- Relationship with applications

### Application Model
- Company name
- Position
- Application deadline
- Status
- Notes
- Date applied
- Relationship with user

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Future Enhancements

- Email notifications for deadlines
- Document upload functionality
- Interview scheduling
- Integration with job boards
- Mobile application
- Analytics dashboard improvements 

##Author Contact
- Name: Kelvin Oppong Acheampong