import pandas as pd
import pyodbc
from datetime import datetime

# Read Excel
file_path = 'Employee.xlsx'  # Ensure it's in the same folder as this script
df = pd.read_excel(file_path)

# Clean column names
df.columns = df.columns.str.strip()

# Rename columns to match DB schema
df.rename(columns={
    'Name': 'Name',
    'Role': 'Role',
    'Location': 'Location',
    'Years of Experience': 'ExperienceYears',
    'Active?': 'Status',
    'Current Comp (INR)': 'Compensation',
    'Last Working Day': 'LastWorkingDay'
}, inplace=True)

# Fix ExperienceYears (convert ranges like '0-1' to mid-value float)
def convert_experience(val):
    try:
        if isinstance(val, str) and '-' in val:
            start, end = map(float, val.split('-'))
            return round((start + end) / 2, 1)
        elif pd.isna(val):
            return None
        else:
            return float(val)
    except:
        return None

df['ExperienceYears'] = df['ExperienceYears'].apply(convert_experience)

# Clean Compensation (remove commas)
df['Compensation'] = df['Compensation'].astype(str).str.replace(',', '', regex=False)
df['Compensation'] = pd.to_numeric(df['Compensation'], errors='coerce')

# Fix Status column (Y/N -> Active/Inactive)
df['Status'] = df['Status'].apply(lambda x: 'Active' if str(x).strip().upper() in ['Y', 'YES', 'ACTIVE'] else 'Inactive')

# Parse LastWorkingDay to proper date format or None
def parse_date(val):
    if pd.isna(val):
        return None
    try:
        return pd.to_datetime(val).date()
    except:
        return None

df['LastWorkingDay'] = df['LastWorkingDay'].apply(parse_date)

# Optional: Fix common typos
df['Role'] = df['Role'].replace({'Senir Associate': 'Senior Associate'})

# DB connection
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=localhost\\SQLEXPRESS;'
    'DATABASE=EmployeeCompDB;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Insert rows
success = 0
failed = 0

for index, row in df.iterrows():
    name = row['Name']
    role = row['Role']
    location = row['Location']
    exp = row['ExperienceYears']
    comp = row['Compensation']
    status = row['Status']
    lwd = row['LastWorkingDay']

    print(f"Inserting: {name}, {role}, {location}, {exp}, {comp}, {status}, {lwd}")

    try:
        cursor.execute("""
            INSERT INTO Employees (Name, Role, Location, ExperienceYears, Compensation, Status, LastWorkingDay)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, name, role, location, exp, comp, status, lwd)
        conn.commit()
        success += 1
    except Exception as e:
        print(f"❌ Error inserting row {index}: {e}")
        failed += 1

print(f"\n✅ Successfully inserted: {success} rows")
print(f"❌ Failed to insert: {failed} rows")
