from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.forms import TicketForm, TicketEditForm, DeleteTicketForm
from app.models import Category, Ticket


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/dashboard")
@login_required
def dashboard():
    tickets = Ticket.query.filter_by(
        user_id=current_user.id
    ).order_by(Ticket.created_at.desc()).all()

    return render_template(
        "dashboard.html",
        tickets=tickets,
        total=len(tickets),
        open_count=sum(t.status == "open" for t in tickets),
        progress_count=sum(t.status == "in_progress" for t in tickets),
        resolved_count=sum(t.status == "resolved" for t in tickets)
    )


@main.route("/tickets")
@login_required
def tickets():
    status_filter = request.args.get("status", "")
    priority_filter = request.args.get("priority", "")

    query = Ticket.query.filter_by(user_id=current_user.id)

    if status_filter:
        query = query.filter_by(status=status_filter)

    if priority_filter:
        query = query.filter_by(priority=priority_filter)

    user_tickets = query.order_by(Ticket.created_at.desc()).all()

    return render_template(
        "tickets.html",
        tickets=user_tickets,
        status_filter=status_filter,
        priority_filter=priority_filter
    )


@main.route("/tickets/new", methods=["GET", "POST"])
@login_required
def create_ticket():
    form = TicketForm()

    categories = Category.query.order_by(Category.name).all()
    form.category_id.choices = [
        (category.id, category.name)
        for category in categories
    ]

    if form.validate_on_submit():
        ticket = Ticket(
            title=form.title.data.strip(),
            description=form.description.data.strip(),
            category_id=form.category_id.data,
            priority=form.priority.data,
            status="open",
            user_id=current_user.id
        )

        db.session.add(ticket)
        db.session.commit()

        flash("Ticket wurde erfolgreich erstellt.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("ticket_form.html", form=form)


@main.route("/tickets/<int:ticket_id>")
@login_required
def ticket_detail(ticket_id):
    ticket = Ticket.query.filter_by(
        id=ticket_id,
        user_id=current_user.id
    ).first_or_404()

    delete_form = DeleteTicketForm()

    return render_template(
        "ticket_detail.html",
        ticket=ticket,
        delete_form=delete_form
    )


@main.route("/tickets/<int:ticket_id>/edit", methods=["GET", "POST"])
@login_required
def edit_ticket(ticket_id):
    ticket = Ticket.query.filter_by(
        id=ticket_id,
        user_id=current_user.id
    ).first_or_404()

    form = TicketEditForm(obj=ticket)

    categories = Category.query.order_by(Category.name).all()
    form.category_id.choices = [
        (category.id, category.name)
        for category in categories
    ]

    if form.validate_on_submit():
        ticket.title = form.title.data.strip()
        ticket.description = form.description.data.strip()
        ticket.category_id = form.category_id.data
        ticket.priority = form.priority.data
        ticket.status = form.status.data

        db.session.commit()

        flash("Ticket wurde aktualisiert.", "success")
        return redirect(
            url_for("main.ticket_detail", ticket_id=ticket.id)
        )

    return render_template(
        "ticket_edit.html",
        form=form,
        ticket=ticket
    )


@main.route("/tickets/<int:ticket_id>/delete", methods=["POST"])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.filter_by(
        id=ticket_id,
        user_id=current_user.id
    ).first_or_404()

    form = DeleteTicketForm()

    if form.validate_on_submit():
        db.session.delete(ticket)
        db.session.commit()

        flash("Ticket wurde gelöscht.", "success")

    return redirect(url_for("main.dashboard"))
