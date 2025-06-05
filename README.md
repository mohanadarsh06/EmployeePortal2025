# Employee Feedback Portal

A comprehensive web application built with Flask for managing employee information, feedback, billing details, and organizational hierarchy. This portal provides managers and employees with tools to track performance, manage billing, and visualize organizational structure.

## Features

### 🏢 **Dashboard & Analytics**
- **Real-time Charts**: Interactive visualizations showing employee distribution by:
  - Employment Type (Permanent/Contract)
  - Billable Status (Billable/Non-billable)
  - Team Distribution (UFS/RG)
  - Location Distribution
  - Skills Distribution
- **Key Metrics**: Quick overview cards displaying total employees, managers, and department statistics
- **Role-based Access**: Different dashboard views for managers and employees

### 👥 **Employee Management**
- **Complete Employee Profiles**: Manage comprehensive employee information including:
  - Personal details (Name, Email, Employee ID)
  - Professional information (Designation, Department, Location)
  - Team assignment (UFS/RG)
  - Employment details (Type, Billable Status, Join Date)
  - Skills tracking and experience years
  - Manager-employee relationships
- **CRUD Operations**: Add, edit, view, and delete employee records
- **Hierarchical Structure**: Manager-subordinate relationships with multi-level hierarchy support
- **Search & Filter**: Advanced filtering options for employee lists

### 📊 **Feedback Management System**
- **Performance Reviews**: Structured feedback system with:
  - Monthly and Quarterly feedback cycles
  - Performance ratings (1-5 scale)
  - Goals achievement tracking
  - Areas of improvement documentation
  - Strengths identification
  - Detailed comments and observations
- **Manager Tools**: Managers can provide feedback to their direct reports and subordinates
- **Historical Tracking**: Complete feedback history for performance trend analysis
- **Automated Periods**: System automatically manages feedback periods by year, month, and quarter

### 💰 **Billing & Financial Management**
- **Detailed Billing Records**: Track financial information including:
  - Billing rates per employee
  - Project and client assignments
  - Monthly billing hours
  - Total billing amounts
  - Currency management
  - Billing status tracking (Draft/Submitted/Approved/Paid)
- **Financial Reports**: Generate billing summaries and financial analytics
- **Multi-project Support**: Employees can be assigned to multiple projects with different rates

### 🏗️ **Organization Hierarchy**
- **Visual Organization Chart**: Interactive hierarchy visualization showing:
  - Manager-employee relationships
  - Department structure
  - Team distributions
  - Reporting lines
- **Multi-level Management**: Support for complex organizational structures
- **Role Identification**: Clear distinction between managers and employees

### 📤 **Data Import/Export**
- **Excel Import**: Bulk employee data import via Excel files
- **Template Download**: Pre-formatted Excel templates for data import
- **Data Validation**: Comprehensive validation during import process
- **Import Results**: Detailed feedback on import success/failures

### 🔐 **Authentication & Security**
- **Secure Login System**: Email and password-based authentication
- **Role-based Access Control**: Different permissions for managers and employees
- **Session Management**: Secure session handling with Flask-Login
- **Password Security**: Hashed password storage using Werkzeug security

### 📱 **User Interface & Experience**
- **Responsive Design**: Mobile-friendly interface that works on all devices
- **Modern UI**: Clean, professional design with Bootstrap 5
- **Interactive Charts**: Chart.js powered visualizations
- **Flash Messages**: User feedback for all operations
- **Intuitive Navigation**: Role-based sidebar navigation

## Technology Stack

- **Backend**: Python Flask
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Charts**: Chart.js for data visualization
- **Icons**: Font Awesome
- **Authentication**: Flask-Login
- **File Handling**: openpyxl for Excel operations
- **Data Processing**: Pandas for data manipulation

## Setup Instructions for Visual Studio Code

### Prerequisites

1. **Python 3.11 or higher**
   ```bash
   python --version
   ```

2. **Git** (for version control)
   ```bash
   git --version
   ```

3. **Visual Studio Code** with Python extension

### Step 1: Clone or Download the Project

```bash
# If using Git
git clone <repository-url>
cd employee-feedback-portal

# Or download and extract the project files
```

### Step 2: Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:
```bash
pip install flask flask-sqlalchemy flask-login psycopg2-binary gunicorn pandas openpyxl email-validator werkzeug sqlalchemy
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/employee_feedback

# Session Security
SESSION_SECRET=your-secret-key-here

# Development Settings
FLASK_ENV=development
FLASK_DEBUG=True
```

### Step 5: Database Setup

#### Option A: PostgreSQL (Recommended for Production)

1. **Install PostgreSQL**:
   - Download from [postgresql.org](https://www.postgresql.org/download/)
   - Install and start the service

2. **Create Database**:
   ```sql
   CREATE DATABASE employee_feedback;
   CREATE USER your_username WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE employee_feedback TO your_username;
   ```

3. **Update DATABASE_URL** in `.env` file with your credentials

#### Option B: SQLite (for Development)

```env
DATABASE_URL=sqlite:///employee_feedback.db
```

### Step 6: Initialize the Application

```bash
# Create database tables and sample data
python create_users.py

# Or run the main application (it will auto-create tables)
python main.py
```

### Step 7: Run the Application

```bash
# Development server
python main.py

# Or using Flask CLI
flask run

# Or using Gunicorn (production-like)
gunicorn --bind 0.0.0.0:5000 --reload main:app
```

### Step 8: Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

### Default Login Credentials

**Top Manager (Full Access)**:
- Email: `sooraj@company.com`
- Password: `password123`

**Line Managers**:
- Email: `anuja@company.com` / Password: `password123`
- Email: `asha@company.com` / Password: `password123`
- Email: `vinod@company.com` / Password: `password123`

## Visual Studio Code Configuration

### Recommended Extensions

1. **Python** - Microsoft
2. **Python Debugger** - Microsoft
3. **Flask** - wholroyd
4. **SQLite Viewer** - qwtel
5. **Auto Rename Tag** - Jun Han
6. **Bracket Pair Colorizer** - CoenraadS

### Launch Configuration

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "env": {
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "1"
            },
            "args": [],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```

### Workspace Settings

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "files.associations": {
        "*.html": "html"
    },
    "emmet.includeLanguages": {
        "jinja2": "html"
    }
}
```

## Project Structure

```
employee-feedback-portal/
├── app.py                 # Flask application factory
├── main.py               # Application entry point
├── models.py             # Database models
├── routes.py             # URL routes and view functions
├── utils.py              # Utility functions
├── create_users.py       # Sample data creation
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── charts.js     # Chart configurations
├── templates/
│   ├── base.html         # Base template
│   ├── login.html        # Login page
│   ├── dashboard.html    # Dashboard
│   ├── employees.html    # Employee list
│   ├── employee_form.html # Employee add/edit form
│   ├── feedback.html     # Feedback list
│   ├── feedback_form.html # Feedback form
│   ├── billing.html      # Billing records
│   ├── hierarchy.html    # Organization chart
│   ├── import_excel.html # Excel import
│   ├── 404.html          # Error pages
│   └── 500.html
└── uploads/              # File upload directory
```

## Development Workflow

### 1. Database Migrations

When making model changes:

```python
# In Python console or script
from app import app, db
with app.app_context():
    db.create_all()
```

### 2. Adding New Features

1. **Models**: Update `models.py` for new database fields
2. **Routes**: Add new endpoints in `routes.py`
3. **Templates**: Create/modify HTML templates
4. **Static Files**: Add CSS/JS as needed

### 3. Debugging

- Use VS Code debugger with the provided launch configuration
- Check Flask debug logs in the terminal
- Use browser developer tools for frontend debugging
- Database queries can be debugged with logging:

```python
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

## Deployment

### Production Setup

1. **Environment Variables**:
   ```env
   FLASK_ENV=production
   DATABASE_URL=postgresql://prod_user:prod_pass@prod_host:5432/prod_db
   SESSION_SECRET=super-secure-secret-key
   ```

2. **Gunicorn Configuration**:
   ```bash
   gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
   ```

3. **Database Backup**:
   ```bash
   pg_dump employee_feedback > backup.sql
   ```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   - Check DATABASE_URL in `.env`
   - Ensure PostgreSQL service is running
   - Verify database credentials

2. **Import Errors**:
   - Activate virtual environment
   - Install missing packages: `pip install -r requirements.txt`

3. **Template Errors**:
   - Check file paths in templates folder
   - Verify Jinja2 syntax

4. **Port Already in Use**:
   ```bash
   # Find and kill process
   lsof -ti:5000 | xargs kill -9
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test thoroughly
4. Submit a pull request with detailed description

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the Flask documentation
3. Create an issue in the repository
4. Contact the development team

---

**Happy Coding!** 🚀