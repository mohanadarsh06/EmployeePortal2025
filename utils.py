# utils.py
import pandas as pd
import json
from datetime import datetime
import re

ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_excel_file(file, manager_id):
    """Process uploaded Excel file and create employee records"""
    from app import db
    from models import Employee
    
    result = {
        'success': False,
        'count': 0,
        'skipped': 0,
        'errors': [],
        'error': None
    }
    
    try:
        # Read Excel file with multiple sheet support
        try:
            df = pd.read_excel(file, sheet_name=0)  # Read first sheet
        except Exception as e:
            result['error'] = f"Failed to read Excel file: {str(e)}"
            return result

        if df.empty:
            result['error'] = "Excel file is empty"
            return result

        # Normalize column names (remove extra spaces, handle case variations)
        df.columns = df.columns.str.strip()
        
        # Expected columns with flexible matching
        required_columns = ['Employee ID', 'Name', 'Email']
        optional_columns = {
            'Designation': ['designation', 'job_title', 'position'],
            'Department': ['department', 'dept'],
            'Location': ['location', 'office', 'city'],
            'Team': ['team', 'group'],
            'Skills': ['skills', 'skill_set', 'technologies'],
            'Employment Type': ['employment_type', 'emp_type', 'type'],
            'Billable Status': ['billable_status', 'billable'],
            'Join Date': ['join_date', 'joining_date', 'start_date'],
            'Experience Years': ['experience_years', 'exp_years', 'experience'],
            'Manager ID': ['manager_id', 'manager_employee_id', 'reporting_manager'],
            'Is Manager': ['is_manager', 'manager_flag', 'manager']
        }

        # Check for required columns
        missing_required = []
        for col in required_columns:
            if col not in df.columns:
                # Try to find alternative column names
                found = False
                for df_col in df.columns:
                    if col.lower().replace(' ', '_') in df_col.lower().replace(' ', '_'):
                        df = df.rename(columns={df_col: col})
                        found = True
                        break
                if not found:
                    missing_required.append(col)

        if missing_required:
            result['error'] = f"Missing required columns: {', '.join(missing_required)}"
            return result

        # Store employees temporarily to handle manager relationships
        temp_employees = []
        manager_relationships = {}

        # First pass: Create all employees without manager relationships
        for index, row in df.iterrows():
            try:
                # Skip rows with missing critical data
                if pd.isna(row.get('Employee ID')) or pd.isna(row.get('Name')) or pd.isna(row.get('Email')):
                    result['errors'].append(f"Row {index + 2}: Missing critical data (Employee ID, Name, or Email)")
                    continue

                employee_id = str(row.get('Employee ID', '')).strip()
                email = str(row.get('Email', '')).strip().lower()
                
                # Check if employee already exists
                existing_employee = Employee.query.filter(
                    (Employee.employee_id == employee_id) | (Employee.email == email)
                ).first()

                if existing_employee:
                    result['skipped'] += 1
                    result['errors'].append(f"Row {index + 2}: Employee {employee_id} already exists")
                    continue

                # Validate email format
                if '@' not in email:
                    result['errors'].append(f"Row {index + 2}: Invalid email format: {email}")
                    continue

                # Create new employee
                employee_data = {
                    'employee_id': employee_id,
                    'name': str(row.get('Name', '')).strip(),
                    'email': email,
                    'designation': str(row.get('Designation', '') or '').strip(),
                    'department': str(row.get('Department', '') or '').strip(),
                    'location': str(row.get('Location', '') or '').strip(),
                    'team': str(row.get('Team', '') or '').strip(),
                    'skills': str(row.get('Skills', '') or '').strip(),
                    'employment_type': str(row.get('Employment Type', '') or '').strip(),
                    'billable_status': str(row.get('Billable Status', '') or '').strip(),
                    'manager_employee_id': str(row.get('Manager ID', '') or '').strip(),
                    'is_manager_flag': str(row.get('Is Manager', '') or '').strip().lower()
                }

                # Handle dates
                if pd.notna(row.get('Join Date')):
                    try:
                        if isinstance(row['Join Date'], str):
                            # Try multiple date formats
                            for date_format in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y']:
                                try:
                                    employee_data['join_date'] = datetime.strptime(row['Join Date'], date_format).date()
                                    break
                                except ValueError:
                                    continue
                        else:
                            employee_data['join_date'] = row['Join Date'].date()
                    except Exception as e:
                        result['errors'].append(f"Row {index + 2}: Invalid date format for Join Date")

                # Handle experience years
                if pd.notna(row.get('Experience Years')):
                    try:
                        employee_data['experience_years'] = float(row['Experience Years'])
                    except (ValueError, TypeError):
                        result['errors'].append(f"Row {index + 2}: Invalid experience years value")

                temp_employees.append(employee_data)

                # Store manager relationship for later processing
                if employee_data['manager_employee_id']:
                    manager_relationships[employee_id] = employee_data['manager_employee_id']

            except Exception as e:
                result['errors'].append(f"Row {index + 2}: Error processing row - {str(e)}")
                continue

        # Second pass: Create employees in database
        created_employees = {}
        
        for emp_data in temp_employees:
            try:
                employee = Employee()
                employee.employee_id = emp_data['employee_id']
                employee.name = emp_data['name']
                employee.email = emp_data['email']
                employee.designation = emp_data['designation'] or None
                employee.department = emp_data['department'] or None
                employee.location = emp_data['location'] or None
                employee.team = emp_data['team'] or None
                employee.skills = emp_data['skills'] or None
                employee.employment_type = emp_data['employment_type'] or None
                employee.billable_status = emp_data['billable_status'] or None
                
                if 'join_date' in emp_data:
                    employee.join_date = emp_data['join_date']
                
                if 'experience_years' in emp_data:
                    employee.experience_years = emp_data['experience_years']

                # Set manager flag
                employee.is_manager = emp_data['is_manager_flag'] in ['yes', 'true', '1', 'y']
                
                # Set default manager to importing user for now
                employee.manager_id = manager_id

                # Set default password
                employee.set_password('password123')

                db.session.add(employee)
                db.session.flush()  # Get ID without committing
                
                created_employees[emp_data['employee_id']] = employee
                result['count'] += 1

            except Exception as e:
                result['errors'].append(f"Failed to create employee {emp_data['employee_id']}: {str(e)}")
                continue

        # Third pass: Update manager relationships
        for emp_id, manager_emp_id in manager_relationships.items():
            if emp_id in created_employees and manager_emp_id in created_employees:
                try:
                    created_employees[emp_id].manager_id = created_employees[manager_emp_id].id
                except Exception as e:
                    result['errors'].append(f"Failed to set manager for {emp_id}: {str(e)}")

        db.session.commit()
        result['success'] = True

    except Exception as e:
        db.session.rollback()
        result['error'] = f"Unexpected error: {str(e)}"

    return result

def get_dashboard_analytics(employees):
    """Generate analytics data for dashboard charts"""
    if not employees:
        return {
            'skills': {},
            'employment_type': {},
            'billable_status': {},
            'location': {},
            'team': {},
            'total_employees': 0
        }

    analytics = {
        'skills': {},
        'employment_type': {},
        'billable_status': {},
        'location': {},
        'team': {},
        'total_employees': len(employees)
    }

    for employee in employees:
        # Employment type analytics
        emp_type = employee.employment_type or 'Unknown'
        analytics['employment_type'][emp_type] = analytics['employment_type'].get(emp_type, 0) + 1

        # Billable status analytics
        billable = employee.billable_status or 'Unknown'
        analytics['billable_status'][billable] = analytics['billable_status'].get(billable, 0) + 1

        # Location analytics
        location = employee.location or 'Unknown'
        analytics['location'][location] = analytics['location'].get(location, 0) + 1

        # Team analytics
        team = employee.team or 'Unknown'
        analytics['team'][team] = analytics['team'].get(team, 0) + 1

        # Skills analytics (assuming skills are comma-separated)
        if employee.skills:
            skills_list = [skill.strip() for skill in employee.skills.split(',')]
            for skill in skills_list:
                if skill:
                    analytics['skills'][skill] = analytics['skills'].get(skill, 0) + 1

    return analytics

def create_sample_data():
    """Create sample data for testing - only use if no data exists"""
    # Import here to avoid circular imports
    from app import db
    from models import Employee

    if Employee.query.first():
        return  # Data already exists

    # Create top-level manager
    top_manager = Employee(
        employee_id='EMP001',
        name='Sooraj Kumar',
        email='sooraj@company.com',
        designation='VP Engineering',
        department='Engineering',
        location='Bangalore',
        team='UFS',
        employment_type='Permanent',
        billable_status='Non-billable',
        is_manager=True,
        manager_id=None
    )
    top_manager.set_password('password123')
    db.session.add(top_manager)
    db.session.commit()

    # Create line managers
    managers = [
        {
            'employee_id': 'EMP002',
            'name': 'Anuja Sharma',
            'email': 'anuja@company.com',
            'designation': 'Engineering Manager',
            'team': 'UFS'
        },
        {
            'employee_id': 'EMP003',
            'name': 'Asha Patel',
            'email': 'asha@company.com',
            'designation': 'Tech Lead',
            'team': 'RG'
        },
        {
            'employee_id': 'EMP004',
            'name': 'Vinod Singh',
            'email': 'vinod@company.com',
            'designation': 'Senior Manager',
            'team': 'UFS'
        }
    ]

    for mgr_data in managers:
        manager = Employee(
            employee_id=mgr_data['employee_id'],
            name=mgr_data['name'],
            email=mgr_data['email'],
            designation=mgr_data['designation'],
            department='Engineering',
            location='Bangalore',
            team=mgr_data['team'],
            employment_type='Permanent',
            billable_status='Billable',
            is_manager=True,
            manager_id=top_manager.id
        )
        manager.set_password('password123')
        db.session.add(manager)

    db.session.commit()