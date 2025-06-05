#!/bin/bash

# Employee Feedback Portal - GitHub Commit Script
# Repository: https://github.com/anuja-sonaji/Bmp_Aus_emp_feedback_portal1.git

echo "🚀 Preparing to commit Employee Feedback Portal to GitHub..."

# Configure git user (update with your details)
git config user.name "Anuja Sonaji"
git config user.email "anuja.sonaji@example.com"

# Add remote repository if not already added
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/anuja-sonaji/Bmp_Aus_emp_feedback_portal1.git

# Add all files to staging
echo "📁 Adding files to git..."
git add .

# Create commit with descriptive message
echo "💾 Creating commit..."
git commit -m "Initial commit: Complete Employee Feedback Portal

Features implemented:
- User authentication system with role-based access
- Dashboard with interactive charts and analytics
- Employee management (CRUD operations)
- Feedback management system (monthly/quarterly reviews)
- Billing and financial tracking
- Organization hierarchy visualization
- Excel import/export functionality
- Responsive web design with Bootstrap 5
- PostgreSQL database integration
- Comprehensive documentation and setup guide

Tech Stack:
- Backend: Python Flask, SQLAlchemy, Flask-Login
- Frontend: HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js
- Database: PostgreSQL with psycopg2
- File Processing: pandas, openpyxl
- Server: Gunicorn WSGI server"

# Push to GitHub
echo "🌐 Pushing to GitHub repository..."
git branch -M main
git push -u origin main

echo "✅ Successfully committed Employee Feedback Portal to GitHub!"
echo "📍 Repository URL: https://github.com/anuja-sonaji/Bmp_Aus_emp_feedback_portal1.git"
echo ""
echo "🔗 You can now view your project at:"
echo "   https://github.com/anuja-sonaji/Bmp_Aus_emp_feedback_portal1"