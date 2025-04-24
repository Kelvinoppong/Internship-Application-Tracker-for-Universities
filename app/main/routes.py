from flask import render_template, redirect, url_for, flash, request, send_file
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.models import Application, User
from app.main.forms import ApplicationForm
from functools import wraps
import pandas as pd
from io import BytesIO
from datetime import datetime

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You need to be an admin to access this page.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@bp.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('main/index.html', title='Home')

@bp.route('/dashboard')
@login_required
def dashboard():
    # Get all applications for the current user
    applications = Application.query.filter_by(user_id=current_user.id)\
        .order_by(Application.date_applied.desc()).all()
    
    # Calculate statistics
    total_applications = len(applications)
    pending = sum(1 for app in applications if app.status == 'Pending')
    interviews = sum(1 for app in applications if app.status == 'Interview')
    offers = sum(1 for app in applications if app.status == 'Offer')
    
    stats = {
        'total': total_applications,
        'pending': pending,
        'interviews': interviews,
        'offers': offers
    }
    
    return render_template('main/dashboard.html', 
                         title='Dashboard',
                         applications=applications,
                         stats=stats)

@bp.route('/application/add', methods=['GET', 'POST'])
@login_required
def add_application():
    form = ApplicationForm()
    if form.validate_on_submit():
        application = Application(
            company_name=form.company_name.data,
            position=form.position.data,
            status=form.status.data,
            deadline=form.deadline.data,
            notes=form.notes.data,
            user_id=current_user.id
        )
        db.session.add(application)
        db.session.commit()
        flash('Application added successfully!')
        return redirect(url_for('main.dashboard'))
    return render_template('main/application_form.html',
                         title='Add Application',
                         form=form)

@bp.route('/application/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_application(id):
    application = Application.query.get_or_404(id)
    if application.user_id != current_user.id and not current_user.is_admin():
        flash('You cannot edit this application.')
        return redirect(url_for('main.dashboard'))
    
    form = ApplicationForm()
    if form.validate_on_submit():
        application.company_name = form.company_name.data
        application.position = form.position.data
        application.status = form.status.data
        application.deadline = form.deadline.data
        application.notes = form.notes.data
        db.session.commit()
        flash('Application updated successfully!')
        return redirect(url_for('main.dashboard'))
    elif request.method == 'GET':
        form.company_name.data = application.company_name
        form.position.data = application.position
        form.status.data = application.status
        form.deadline.data = application.deadline
        form.notes.data = application.notes
    return render_template('main/application_form.html',
                         title='Edit Application',
                         form=form)

@bp.route('/application/<int:id>/delete', methods=['POST'])
@login_required
def delete_application(id):
    application = Application.query.get_or_404(id)
    if application.user_id != current_user.id and not current_user.is_admin():
        flash('You cannot delete this application.')
        return redirect(url_for('main.dashboard'))
    
    db.session.delete(application)
    db.session.commit()
    flash('Application deleted successfully!')
    return redirect(url_for('main.dashboard'))

@bp.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    # Get filter parameters
    student_id = request.args.get('student_id', type=int)
    company = request.args.get('company', '')
    status = request.args.get('status', '')
    
    # Base query
    query = Application.query.join(User)
    
    # Apply filters
    if student_id:
        query = query.filter(Application.user_id == student_id)
    if company:
        query = query.filter(Application.company_name.ilike(f'%{company}%'))
    if status:
        query = query.filter(Application.status == status)
    
    # Get all applications
    applications = query.order_by(Application.date_applied.desc()).all()
    
    # Get all students and statuses for filter dropdowns
    students = User.query.filter_by(role='student').all()
    statuses = ['Pending', 'Applied', 'Interview', 'Offer', 'Rejected']
    
    # Calculate statistics
    total_students = User.query.filter_by(role='student').count()
    total_applications = len(applications)
    total_companies = len(set(app.company_name for app in applications))
    success_rate = len([app for app in applications if app.status == 'Offer']) / total_applications if total_applications > 0 else 0
    
    stats = {
        'total_students': total_students,
        'total_applications': total_applications,
        'total_companies': total_companies,
        'success_rate': f"{success_rate:.1%}"
    }
    
    return render_template('main/admin_dashboard.html',
                         title='Admin Dashboard',
                         applications=applications,
                         students=students,
                         statuses=statuses,
                         stats=stats,
                         selected_student=student_id,
                         selected_company=company,
                         selected_status=status)

@bp.route('/admin/export')
@login_required
@admin_required
def export_data():
    # Get all applications with user information
    applications = db.session.query(
        Application,
        User.email.label('student_email')
    ).join(User).all()
    
    # Create DataFrame
    data = []
    for app, email in applications:
        data.append({
            'Student Email': email,
            'Company': app.company_name,
            'Position': app.position,
            'Status': app.status,
            'Date Applied': app.date_applied.strftime('%Y-%m-%d'),
            'Deadline': app.deadline.strftime('%Y-%m-%d') if app.deadline else '',
            'Notes': app.notes
        })
    
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = BytesIO()
    df.to_excel(output, index=False, sheet_name='Applications')
    output.seek(0)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'internship_applications_{timestamp}.xlsx'
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    ) 