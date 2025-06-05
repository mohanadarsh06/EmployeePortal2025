from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Employee(UserMixin, db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # Employee Details
    designation = db.Column(db.String(100))
    department = db.Column(db.String(100))
    location = db.Column(db.String(100))
    team = db.Column(db.String(50))  # UFS/RG
    skills = db.Column(db.Text)  # JSON string of skills
    
    # Employment Details
    employment_type = db.Column(db.String(20))  # Permanent/Contract
    billable_status = db.Column(db.String(20))  # Billable/Non-billable
    join_date = db.Column(db.Date)
    experience_years = db.Column(db.Float)
    
    # Hierarchy
    manager_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    is_manager = db.Column(db.Boolean, default=False)
    
    # Relationships
    manager = db.relationship('Employee', remote_side=[id], backref='direct_reports')
    feedback_given = db.relationship('Feedback', foreign_keys='Feedback.manager_id', backref='given_by')
    feedback_received = db.relationship('Feedback', foreign_keys='Feedback.employee_id', backref='received_by')
    billing_records = db.relationship('BillingDetail', backref='employee')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_all_subordinates(self):
        """Get all employees under this manager's hierarchy"""
        subordinates = []
        direct_reports = self.direct_reports
        for report in direct_reports:
            subordinates.append(report)
            subordinates.extend(report.get_all_subordinates())
        return subordinates
    
    def can_manage(self, employee):
        """Check if this employee can manage another employee"""
        if not self.is_manager:
            return False
        subordinates = self.get_all_subordinates()
        return employee in subordinates
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'name': self.name,
            'email': self.email,
            'designation': self.designation,
            'department': self.department,
            'location': self.location,
            'team': self.team,
            'skills': self.skills,
            'employment_type': self.employment_type,
            'billable_status': self.billable_status,
            'join_date': self.join_date.isoformat() if self.join_date else None,
            'experience_years': self.experience_years,
            'manager_id': self.manager_id,
            'manager_name': self.manager.name if self.manager else None,
            'is_manager': self.is_manager
        }

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    
    # Feedback Period
    feedback_type = db.Column(db.String(20), nullable=False)  # Monthly/Quarterly
    period_year = db.Column(db.Integer, nullable=False)
    period_month = db.Column(db.Integer)  # For monthly feedback
    period_quarter = db.Column(db.Integer)  # For quarterly feedback
    
    # Feedback Content
    performance_rating = db.Column(db.Integer)  # 1-5 scale
    goals_achieved = db.Column(db.Text)
    areas_of_improvement = db.Column(db.Text)
    strengths = db.Column(db.Text)
    comments = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_name': self.received_by.name,
            'manager_name': self.given_by.name,
            'feedback_type': self.feedback_type,
            'period_year': self.period_year,
            'period_month': self.period_month,
            'period_quarter': self.period_quarter,
            'performance_rating': self.performance_rating,
            'goals_achieved': self.goals_achieved,
            'areas_of_improvement': self.areas_of_improvement,
            'strengths': self.strengths,
            'comments': self.comments,
            'created_at': self.created_at.isoformat()
        }

class BillingDetail(db.Model):
    __tablename__ = 'billing_details'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    
    # Billing Information
    billing_rate = db.Column(db.Float)
    currency = db.Column(db.String(10), default='USD')
    project_name = db.Column(db.String(200))
    client_name = db.Column(db.String(200))
    
    # Time Period
    billing_month = db.Column(db.Integer, nullable=False)
    billing_year = db.Column(db.Integer, nullable=False)
    
    # Hours and Amount
    billable_hours = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    
    # Status
    billing_status = db.Column(db.String(20), default='Draft')  # Draft/Submitted/Approved/Paid
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_name': self.employee.name,
            'billing_rate': self.billing_rate,
            'currency': self.currency,
            'project_name': self.project_name,
            'client_name': self.client_name,
            'billing_month': self.billing_month,
            'billing_year': self.billing_year,
            'billable_hours': self.billable_hours,
            'total_amount': self.total_amount,
            'billing_status': self.billing_status
        }
