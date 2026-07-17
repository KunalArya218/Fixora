# Fixora - Smart Helpdesk & Ticket Management System

Fixora is a full-stack Flask-based helpdesk and ticket management system designed to simplify issue reporting, tracking, and resolution with automated email notifications and an admin control panel.

---

## 🚀 Overview

Fixora allows users to raise support tickets with details and attachments, while admins can manage, update, and respond to tickets efficiently. The system also sends automated email notifications for ticket creation and updates.

---

## ✨ Features

* 📝 Create support tickets with unique ID
* 📧 Email notifications for ticket creation and updates
* 📂 File upload support for issue attachments
* 🧑‍💼 Admin dashboard for ticket management
* 🔄 Update ticket status, priority, and category
* 💬 Reply system with optional attachments
* 🔐 Secure login system for admin
* ⏱️ Timezone support (Asia/Kolkata)
* 📊 Dashboard analytics (total, open, resolved, critical tickets)

---

## 🛠️ Tech Stack

* Python (Flask)
* Flask-SQLAlchemy (Database ORM)
* Flask-Login (Authentication)
* Flask-Mail (SMTP Email system)
* PostgreSQL / SQLite
* HTML, CSS, JavaScript
* Jinja2 Templates

---

## 📁 Project Structure

```
Fixora/
│
├── app.py
├── config.py
├── requirements.txt
├── .gitignore
├── LICENSE
│
├── templates/
│   ├── index.html
│   ├── create_ticket.html
│   ├── dashboard.html
│   ├── login.html
│   ├── track_ticket.html
│   └── ticket_details.html
│
├── static/
│   ├── style.css
│   ├── uploads/
│   └── replies/
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Kunalarya218/fixora.git
cd fixora
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup environment variables

Create a `.env` file:

```
SECRET_KEY=your_secret_key

DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432
DB_NAME=your_db_name

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

### 5. Run the application

```bash
python app.py
```

---

## 📧 Email System

Fixora uses SMTP (Gmail recommended) to send:

* Ticket creation confirmation
* Ticket update notifications
* Admin replies with optional attachments

⚠️ Use Gmail App Password (not normal password).

---

## 🔐 Admin Access

* Login required for dashboard access
* Admin can manage all tickets
* Update status, priority, category
* Send replies via email

---

## 📊 Dashboard Features

* Total tickets count
* Open tickets
* Resolved tickets
* Critical tickets
* Full ticket management table

---

## 🚀 Deployment

Recommended platforms:

* Render (Flask hosting)
* Neon (PostgreSQL database)

Use Gunicorn for production:

```bash
gunicorn app:app
```

---

## ⚠️ Important Notes

* Do NOT upload `.env` file to GitHub
* Do NOT expose email passwords
* Ensure file upload directories exist

---

## 👨‍💻 Author

**Kunal Arya**

---

## 📜 License

This project is licensed under the MIT License - feel free to use and modify it.

---

## 💡 Future Improvements

* AI-powered ticket auto-response
* Real-time chat support
* WhatsApp notifications
* Advanced analytics dashboard
* Role-based admin system

---

🔥 Built with Flask | Designed for real-world helpdesk use
