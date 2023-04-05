from flask import Blueprint, request, render_template, redirect, url_for, flash
from db import mysql

employees = Blueprint('employees', __name__, template_folder='src/templates')


@employees.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM employees')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', employees=data)

@employees.route('/edit/<id>', methods=['POST', 'GET'])
def get_employee(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM employees WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('manageEmployees.html', employee=data[0])


@employees.route('/add_employee', methods=['POST'])
def add_employee():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO employees (fullname, phone, email) VALUES (%s,%s,%s)", (fullname, phone, email))
            mysql.connection.commit()
            flash('Employee Added successfully')
            return redirect(url_for('employees.Index'))
        except Exception as e:
            flash(e.args[1])
            return redirect(url_for('employees.Index'))


@employees.route('/update/<id>', methods=['POST'])
def update_employee(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE employees
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (fullname, email, phone, id))
        flash('Employee Updated Successfully!')
        mysql.connection.commit()
        return redirect(url_for('employees.Index'))


@employees.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_employee(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM employees WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Employee Removed Successfully!')
    return redirect(url_for('employees.Index'))
