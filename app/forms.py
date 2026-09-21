from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    SelectField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    username = StringField(
        "Benutzername",
        validators=[DataRequired(), Length(min=3, max=80)]
    )
    email = StringField(
        "E-Mail",
        validators=[DataRequired(), Email(), Length(max=120)]
    )
    password = PasswordField(
        "Passwort",
        validators=[DataRequired(), Length(min=6)]
    )
    password_confirm = PasswordField(
        "Passwort bestätigen",
        validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Registrieren")


class LoginForm(FlaskForm):
    username = StringField(
        "Benutzername",
        validators=[DataRequired()]
    )
    password = PasswordField(
        "Passwort",
        validators=[DataRequired()]
    )
    submit = SubmitField("Anmelden")


class TicketForm(FlaskForm):
    title = StringField(
        "Titel",
        validators=[DataRequired(), Length(min=3, max=150)]
    )
    description = TextAreaField(
        "Beschreibung",
        validators=[DataRequired(), Length(min=5)]
    )
    category_id = SelectField(
        "Kategorie",
        coerce=int,
        validators=[DataRequired()]
    )
    priority = SelectField(
        "Priorität",
        choices=[
            ("low", "Niedrig"),
            ("medium", "Mittel"),
            ("high", "Hoch"),
            ("critical", "Kritisch")
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField("Ticket erstellen")


class TicketEditForm(FlaskForm):
    title = StringField(
        "Titel",
        validators=[DataRequired(), Length(min=3, max=150)]
    )
    description = TextAreaField(
        "Beschreibung",
        validators=[DataRequired(), Length(min=5)]
    )
    category_id = SelectField(
        "Kategorie",
        coerce=int,
        validators=[DataRequired()]
    )
    priority = SelectField(
        "Priorität",
        choices=[
            ("low", "Niedrig"),
            ("medium", "Mittel"),
            ("high", "Hoch"),
            ("critical", "Kritisch")
        ]
    )
    status = SelectField(
        "Status",
        choices=[
            ("open", "Offen"),
            ("in_progress", "In Bearbeitung"),
            ("resolved", "Gelöst"),
            ("closed", "Geschlossen")
        ]
    )
    submit = SubmitField("Änderungen speichern")


class DeleteTicketForm(FlaskForm):
    submit = SubmitField("Ticket löschen")
