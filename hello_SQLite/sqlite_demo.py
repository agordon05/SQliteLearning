import sqlite3
from employee import Employee

conn = sqlite3.connect('employee.db')

# Good for testing
# conn = sqlite3.connect(':memory:')

c = conn.cursor()


# c.execute("INSERT INTO employees VALUES ('corey', 'Schafer', 50000)")
# conn.commit()
# conn.close()

# create table
def create_table():
    with conn:
        c.execute(
            """CREATE TABLE IF NOT EXISTS employees (
                first TEXT,
                last TEXT,
                pay INTEGER
                )""")
    # conn.commit()


def add_data(employee: Employee):
    with conn:
        # c.execute("INSERT INTO employees VALUES ('corey', 'Schafer', 50000)")
        c.execute("INSERT INTO employees VALUES (?, ?, ?)", (employee.first, employee.last, employee.pay))

        # SECONDARY WAY OF INSERTING DATA
        # emp_dict = {
        #     'first': employee.first,
        #     'last': employee.last,
        #     'pay': employee.pay
        # }
        # c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", emp_dict)


def get_from_last_name(name) -> []:
    employee_list = []

    with conn:
        c.execute("SELECT * FROM employees WHERE last=:last", {'last': name})
        data = c.fetchall()
        print(data)
        for emp in data:
            employee = Employee(emp[0], emp[1], emp[2])
            employee_list.append(employee)
    return employee_list
    # conn.commit()


def get_employees() -> []:
    employee_list = []

    with conn:
        c.execute("SELECT * FROM employees")
        data = c.fetchall()
        print(data)
        for emp in data:
            employee = Employee(emp[0], emp[1], emp[2])
            employee_list.append(employee)
    return employee_list


def update_pay(employee: Employee, pay):
    with conn:
        emp_dict = employee.get_dict()
        emp_dict['pay'] = pay
        c.execute(
            """
            UPDATE employees 
            SET pay = :pay 
            WHERE first = :first AND last = :last
            """, emp_dict)


def remove_employee(emp: Employee):
    with conn:
        emp_dict = emp.get_dict()
        c.execute("DELETE from employees WHERE first = :first AND last = :last", emp_dict)


def close():
    conn.close()



