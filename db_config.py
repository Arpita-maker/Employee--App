import pyodbc

def get_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=EmployeeCompDB;'
        'Trusted_Connection=yes;'
    )
