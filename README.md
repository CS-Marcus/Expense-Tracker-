# Expensely (Expense Tracker)


A simple Flask-based web application to track personal expenses.


## Features
- User registration and login (secure with bcrypt)
- Add, edit, and delete expenses
- Expense list with total calculation
- Flash messages and basic styling


## Technologies Used
- Flask
- Flask-Login
- Flask-Bcrypt
- SQLite
- HTML/CSS


## How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/expense-tracker.git

## Create a Virtual Environment (Optional but Recommended)
python -m venv venv
venv\Scripts\activate # On mac: source venv/bin/activate 

## Install dependencies
pip install -r requirements.txt

## Run the app 
flask run 

## Project Structure 
expense-tracker/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── templates/
│       ├── layout.html
│       ├── register.html
│       ├── login.html
│       ├── dashboard.html
│       ├── add_expense.html
│       └── modify_expense.html
│
├── requirements.txt
├── README.md
└── run.py








