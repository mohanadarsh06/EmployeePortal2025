#!/usr/bin/env python3
from werkzeug.security import generate_password_hash
from app import app, db
from models import Employee

def create_sample_users():
    with app.app_context():
        # Check if users already exist
        if Employee.query.first():
            print("Users already exist in database")
            return
        
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
        print(f"Created top manager: {top_manager.name}")
        
        # Create line managers
        managers_data = [
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
        
        for mgr_data in managers_data:
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
            print(f"Created manager: {manager.name}")
        
        db.session.commit()
        print("Sample users created successfully!")

if __name__ == '__main__':
    create_sample_users()