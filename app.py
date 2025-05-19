import streamlit as st
import pandas as pd
import plotly.express as px
import pyodbc

# Database connection
def get_connection():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=EmployeeCompDB;'
        'Trusted_Connection=yes;'
    )
    return conn

# Fetch data
def load_data(include_inactive=True):
    conn = get_connection()
    query = """
        SELECT Name, Role, Location, ExperienceYears, Compensation, Status
        FROM Employees
    """
    df = pd.read_sql(query, conn)
    if not include_inactive:
        df = df[df['Status'].str.lower() == 'active']
    return df

# Streamlit UI
st.title("Employee Compensation Dashboard")

# Load full dataset (with toggle for inactive)
include_inactive = st.checkbox("Include Inactive Employees", value=True)
df = load_data(include_inactive)

# Role filter
roles = df['Role'].dropna().unique()
selected_role = st.selectbox("Filter by Role", options=["All"] + list(roles))
if selected_role != "All":
    df = df[df['Role'] == selected_role]

# Location filter
locations = df['Location'].dropna().unique()
selected_location = st.selectbox("Select Location", options=locations)

# Show average compensation for selected location
location_df = df[df['Location'] == selected_location]
avg_comp = location_df['Compensation'].mean()
st.metric(label=f"Average Compensation in {selected_location}", value=f"INR {avg_comp:,.2f}")

# Bar chart for compensation by location
bar_data = df.groupby('Location')['Compensation'].mean().reset_index()
fig = px.bar(bar_data, x='Location', y='Compensation', title="Average Compensation by Location")
st.plotly_chart(fig)

# Display data table
st.subheader("Employee Details")
st.dataframe(df[['Name', 'Role', 'Location', 'Compensation']])


# Additional Section for Filtered Download (User Story 4)

st.markdown("---")
st.header("🎯 Filtered Data for Export")

# Additional filters (optional - you can extend this)
filtered_roles = st.multiselect("Select Roles to Export", options=df['Role'].unique(), default=list(df['Role'].unique()))
filtered_locations = st.multiselect("Select Locations to Export", options=df['Location'].unique(), default=list(df['Location'].unique()))

# Apply these extra filters on already filtered df
export_df = df[
    df['Role'].isin(filtered_roles) &
    df['Location'].isin(filtered_locations)
]

# Show filtered table
st.dataframe(export_df[['Name', 'Role', 'Location', 'ExperienceYears', 'Compensation', 'Status']])

# Convert to CSV
@st.cache_data
def convert_df_to_csv(dataframe):
    return dataframe.to_csv(index=False).encode('utf-8')

csv = convert_df_to_csv(export_df)

# Download button
st.download_button(
    label="📥 Download Filtered CSV",
    data=csv,
    file_name='filtered_employees.csv',
    mime='text/csv'
)

# ==========================
# User Story 2: Experience Grouping
# ==========================
st.markdown("---")
st.header("👥 Group Employees by Years of Experience")

# Create bins for experience
bins = [0, 1, 2, 5, 10, 20, float('inf')]
labels = ["0-1", "1-2", "2-5", "5-10", "10-20", "20+"]

df['ExperienceRange'] = pd.cut(df['ExperienceYears'], bins=bins, right=False, labels=labels)

# Group by experience range
group_by_option = st.radio("Group breakdown by:", options=["None", "Location", "Role"])

if group_by_option == "None":
    grouped = df.groupby('ExperienceRange').size().reset_index(name='Count')
    fig_exp = px.bar(grouped, x='ExperienceRange', y='Count', title="Employee Count by Experience Range")
else:
    grouped = df.groupby(['ExperienceRange', group_by_option]).size().reset_index(name='Count')
    fig_exp = px.bar(
        grouped,
        x='ExperienceRange',
        y='Count',
        color=group_by_option,
        barmode='group',
        title=f"Employee Count by Experience Range and {group_by_option}"
    )

st.plotly_chart(fig_exp)


