from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User  # Import từ app.models
from app.models import Ticket
from app import db

admin_bp = Blueprint('admin', __name__)

# Chỉ admin mới được truy cập
def admin_required(func):
    from functools import wraps
    from flask import abort

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)  # HTTP 403 Forbidden
        return func(*args, **kwargs)

    return decorated_view

@admin_bp.route('/manage-users', methods=['GET'])
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@admin_bp.route('/manage-users/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash('You cannot delete an admin user.', 'danger')
        return redirect(url_for('admin.manage_users'))

    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} has been deleted.', 'success')
    return redirect(url_for('admin.manage_users'))



@admin_bp.route('/api/tickets/<status>', methods=['GET'])
@login_required
@admin_required
def get_tickets_by_status(status):
    if status == "total":
        tickets = Ticket.query.all()
    elif status == "open":
        tickets = Ticket.query.filter_by(status='new').all()
    elif status == "in_progress":
        tickets = Ticket.query.filter_by(status='in_progress').all()
    elif status == "closed":
        tickets = Ticket.query.filter_by(status='closed').all()
    else:
        return {"error": "Invalid status"}, 400

    tickets_data = [
        {"id": t.id, "title": t.title, "description": t.description, "status": t.status}
        for t in tickets
    ]
    return {"tickets": tickets_data}, 200
