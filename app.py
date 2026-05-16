from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import flash

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import UserMixin

from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from flask_mail import Mail
from flask_mail import Message

from config import Config

from datetime import datetime

import pytz
import os
import secrets
import logging
import traceback

# =========================================================
# APP INIT
# =========================================================

app = Flask(__name__)
app.config.from_object(Config)
logging.basicConfig(level=logging.DEBUG)

# =========================================================
# FILE STORAGE
# =========================================================

UPLOAD_FOLDER = "static/uploads"
REPLY_FOLDER = "static/replies"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPLY_FOLDER"] = REPLY_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPLY_FOLDER, exist_ok=True)

# =========================================================
# DB + MAIL
# =========================================================

db = SQLAlchemy(app)
mail = Mail(app)

with app.app_context():
    db.create_all()

# =========================================================
# TIMEZONE
# =========================================================

india_timezone = pytz.timezone("Asia/Kolkata")

# =========================================================
# LOGIN
# =========================================================

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# =========================================================
# MODELS
# =========================================================

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    ticket_id = db.Column(db.String(30), unique=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    subject = db.Column(db.String(200), nullable=False)
    issue = db.Column(db.Text, nullable=False)

    status = db.Column(db.String(50), default="Open")
    priority = db.Column(db.String(50), default="Medium")
    category = db.Column(db.String(100), default="General")

    filename = db.Column(db.String(255))

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(india_timezone)
    )

    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(india_timezone),
        onupdate=lambda: datetime.now(india_timezone)
    )

# =========================================================
# USER LOADER
# =========================================================

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# =========================================================
# TICKET ID (NO PREFIX - AS YOU REQUESTED)
# =========================================================

def generate_ticket_id():
    while True:
        ticket_id = secrets.token_hex(4).upper()
        if not Ticket.query.filter_by(ticket_id=ticket_id).first():
            return ticket_id

# =========================================================
# EMAIL SENDER (FULL POWER VERSION)
# =========================================================

def send_email(to, subject, body, attachment_path=None):

    try:
        msg = Message(
            subject=subject,
            sender=app.config.get("MAIL_DEFAULT_SENDER"),
            recipients=[to]
        )

        msg.body = body

        if attachment_path:
            with open(attachment_path, "rb") as f:
                msg.attach(
                    filename=os.path.basename(attachment_path),
                    content_type="application/octet-stream",
                    data=f.read()
                )

        mail.send(msg)

        print("EMAIL SENT SUCCESSFULLY")

        return True

    except Exception as e:
        
        print("===== EMAIL ERROR =====")
        print(str(e))
        traceback.print_exc()
        
        return False

# =========================================================
# HOME
# =========================================================

@app.route("/")
def index():
    return render_template("index.html")

# =========================================================
# CREATE TICKET
# =========================================================

@app.route("/create-ticket", methods=["GET", "POST"])
def create_ticket():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        issue = request.form["issue"]

        file = request.files.get("file")
        filename = None

        if file and file.filename:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(path)

        ticket_id = generate_ticket_id()

        ticket = Ticket(
            ticket_id=ticket_id,
            name=name,
            email=email,
            subject=subject,
            issue=issue,
            filename=filename
        )

        db.session.add(ticket)
        db.session.commit()

        # =========================
        # FULL EMAIL (RESTORED)
        # =========================

        send_email(
            email,
            "Fixora Support Ticket Created",
            f"""
Hello {name},

Your support ticket has been successfully created.

----------------------------------
Ticket ID: {ticket_id}
Subject: {subject}
Status: Open
----------------------------------

Please keep this Ticket ID for future tracking.

We will update you shortly.

Regards,
Fixora Support Team
"""
        )

        flash(
            f"Ticket created successfully! Your Ticket ID is {ticket_id}. Email sent to your registered email.",
            "success"
        )

        return redirect(url_for("track_ticket"))

    return render_template("create_ticket.html")

# =========================================================
# TRACK TICKET
# =========================================================

@app.route("/track-ticket", methods=["GET", "POST"])
def track_ticket():

    ticket = None

    if request.method == "POST":

        ticket_id = request.form["ticket_id"]

        ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()

        if not ticket:
            flash("Ticket not found!", "danger")

    return render_template("track_ticket.html", ticket=ticket)

# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):
            login_user(admin)
            return redirect(url_for("dashboard"))

        flash("Invalid credentials", "danger")

    return render_template("login.html")

# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
@login_required
def dashboard():

    tickets = Ticket.query.order_by(Ticket.updated_at.desc()).all()

    return render_template(
        "dashboard.html",
        tickets=tickets,
        total=Ticket.query.count(),
        open_tickets=Ticket.query.filter_by(status="Open").count(),
        resolved=Ticket.query.filter_by(status="Resolved").count(),
        critical_tickets=Ticket.query.filter_by(priority="Critical").count()
    )

# =========================================================
# TICKET DETAILS (EMAIL + UPDATE FIXED)
# =========================================================

@app.route("/ticket/<int:id>", methods=["GET", "POST"])
@login_required
def ticket_details(id):

    ticket = Ticket.query.get_or_404(id)

    if request.method == "POST":

        action = request.form.get("action")

        ticket.status = request.form["status"]
        ticket.priority = request.form["priority"]
        ticket.category = request.form["category"]

        reply_message = request.form.get("reply_message", "").strip()
        reply_file = request.files.get("reply_file")

        attachment_path = None

        if reply_file and reply_file.filename:
            filename = secure_filename(reply_file.filename)
            attachment_path = os.path.join(app.config["REPLY_FOLDER"], filename)
            reply_file.save(attachment_path)

        db.session.commit()

        # =========================
        # UPDATE ONLY
        # =========================

        if action == "update":
            flash("Ticket updated successfully!", "success")

        # =========================
        # SEND EMAIL
        # =========================

        elif action == "send_email":

            if not reply_message:
                flash("Reply message cannot be empty!", "danger")
                return redirect(url_for("ticket_details", id=id))

            email_status = send_email(
                ticket.email,
                f"Ticket Update - {ticket.ticket_id}",
                f"""
Hello {ticket.name},

Your ticket has been updated.

----------------------------------
Ticket ID: {ticket.ticket_id}
Status: {ticket.status}
Priority: {ticket.priority}
Category: {ticket.category}
----------------------------------

Message from support:
{reply_message}

Last Updated: {ticket.updated_at}

Regards,
Fixora Support Team
""",
                attachment_path
            )

            if email_status:
                flash("Email sent successfully!", "success")
            else:
                flash("Failed to send email!", "danger")

        return redirect(url_for("ticket_details", id=id))

    return render_template("ticket_details.html", ticket=ticket)

# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.errorhandler(Exception)
def handle_exception(e):

    print("===== ERROR =====")
    print(str(e))

    return f"""
    <h1>Internal Server Error</h1>
    <pre>{str(e)}</pre>
    """, 500

# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )