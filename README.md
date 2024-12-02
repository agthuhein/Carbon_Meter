# Carbon Meter

The project aims to calculate carbon emissions for a company based on three key areas: energy usage, waste, and business travel. The calculations will be done monthly for each company. Additionally, an admin dashboard will display the results using pie charts, bar charts, and tables, showing the historical data for the past month, three months, and six months. This tool will help companies track and manage their carbon emissions over time.


## Key Functions
- Carbon Emission Calculation: Calculates carbon emissions based on three main sectors — energy usage, waste, and business travel on a monthly basis for each company.
- Admin Dashboard: Provides an overview of carbon emissions with visualizations such as pie charts and bar charts.
- Historical Data Display: Shows historical carbon emission data for the past month, past three months, and past six months.
- Data Tables: Displays detailed data in table format for easy tracking and comparison.
- Monthly Tracking: Provides the ability to track emissions month by month to identify trends over time.


## Prerequisites

- HTML
- CSS
- Javascript
- Python 3.12.7
- Flask 3.0.3
- SQLAlchemy 2.0.36
- SQLite

## Installing

Clone the repository

    git clone https://github.com/agthuhein/Carbon_Meter.git
    
## Install dependencies

    cd my_assignment
    pip install -r requirements.txt

## Running the application

    python app.py

# Let's get started
## Views
### Login page inputs

- Email Address
- Password

### Register page inputs

- Name
- Email Address
- Password

### Dashboard page inputs

- Select (Last month, Last 3 months, Last 6 months)
- Select (All Companies or Individual Company)
- Export Button (Generate report in PDF format)
- Pie Chart
- Bar Chart
- List of data in table format

### Calculate \ Energy Usage calculation page

- Select month
- Select year
- Select company (Add new link - To add a new company to calculate.)
- Avg. monthly electricity bill (€)
- Avg. monthly gas bill (€)
- Avg. monthly fuel bill (€)
