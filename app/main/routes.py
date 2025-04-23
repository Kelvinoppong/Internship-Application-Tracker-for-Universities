from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.models import Application

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