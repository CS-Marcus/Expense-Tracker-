from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from datetime import datetime
from app import db, bcrypt
from app.models import User, Expense


app = Blueprint('app', __name__)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def dashboard():
    expenses = current_user.expenses
    total = sum(expense.amount for expense in expenses)
    return render_template('dashboard.html', expenses=expenses, total=total)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first(): 
            flash('Username is already taken')
            return redirect(url_for('app.register'))

        secret_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=secret_password)

        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('app.dashboard'))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        
        username = request.form.get('username')
        password = request.form.get('password')

        
        user = User.query.filter(User.username == username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('app.dashboard'))
        else:
            flash('Login failed. Check your username or password', 'error')
            return redirect(url_for('app.login'))

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('app.home'))

@app.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'GET':
        return render_template('add_expense.html')
    
    elif request.method == "POST":
        name = request.form.get('name')
        desc = request.form.get('desc')
        date = request.form.get('date')
        amount = float(request.form.get('amount'))
        date = datetime.strptime(date, "%Y-%m-%d")

        new_expense = Expense(name=name, desc=desc, date=date, amount=amount, user_id=current_user.id)

        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added', 'success')
        return redirect(url_for('app.dashboard'))
    

@app.route('/modify_expense/<int:expense_id>', methods=['GET','POST'])
@login_required
def modify_expense(expense_id):

    expense = Expense.query.get(expense_id)

    if not expense or expense.user_id != current_user.id:
        flash('Expense not found or unauthorized', 'error')
        return redirect(url_for('app.dashboard')) 


    if request.method == 'GET':
        return render_template('modify_expense.html', expense=expense)

    elif request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('desc')
        date = request.form.get('date')
        print("Form data received:", request.form)
        amount = float(request.form.get('amount'))
        date = datetime.strptime(date, "%Y-%m-%d")

        expense.name = name 
        expense.desc = desc 
        expense.date = date 
        expense.amount = amount 

        db.session.commit()

        flash('Expense modified', 'success')
        return redirect(url_for('app.dashboard'))

@app.route('/remove_expense/<int:expense_id>', methods=['POST'])
@login_required
def remove_expense(expense_id):

    expense = Expense.query.get_or_404(expense_id)

    if expense.user_id == current_user.id: 
        db.session.delete(expense)
        db.session.commit()

        flash('Expense removed', 'success')

        return redirect(url_for('app.dashboard'))
    
    else:
        flash('Expense not found or unauthorized', 'error')
        return redirect(url_for('app.dashboard')) 