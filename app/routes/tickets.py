from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.ticket import Ticket
from app.models.users import User
from app.forms import TicketForm
from app import db

tickets_bp = Blueprint('tickets', __name__)

# View All Tickets
@tickets_bp.route('/', methods=['GET'])
@login_required
def list_tickets():
    tickets = Ticket.query.all()
    return render_template('tickets/list.html', tickets=tickets)

# Create Ticket
@tickets_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_ticket():
    form = TicketForm()
    # Lấy danh sách người dùng từ database
    form.assigned_to.choices = [(user.id, user.username) for user in User.query.all()]
    if form.validate_on_submit():
        ticket = Ticket(
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            created_by=current_user.id,
            assigned_to=form.assigned_to.data if form.assigned_to.data else None
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket created successfully!', 'success')
        return redirect(url_for('tickets.list_tickets'))
    return render_template('tickets/create.html', form=form)

@tickets_bp.route('/<int:ticket_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.created_by != current_user.id:
        flash('You are not authorized to edit this ticket.', 'danger')
        return redirect(url_for('tickets.list_tickets'))

    form = TicketForm(obj=ticket)
    # Lấy danh sách người dùng từ database
    form.assigned_to.choices = [(user.id, user.username) for user in User.query.all()]
    if form.validate_on_submit():
        ticket.title = form.title.data
        ticket.description = form.description.data
        ticket.status = form.status.data
        ticket.assigned_to = form.assigned_to.data if form.assigned_to.data else None
        db.session.commit()
        flash('Ticket updated successfully!', 'success')
        return redirect(url_for('tickets.list_tickets'))
    return render_template('tickets/edit.html', form=form, ticket=ticket)


# Delete Ticket
@tickets_bp.route('/<int:ticket_id>/delete', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.created_by != current_user.id:
        flash('You are not authorized to delete this ticket.', 'danger')
        return redirect(url_for('tickets.list_tickets'))

    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket deleted successfully!', 'success')
    return redirect(url_for('tickets.list_tickets'))