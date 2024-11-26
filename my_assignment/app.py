from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify, json
from model import db, app, User, Company, Energy, Waste, BusinessTravel, Usage
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random


###Views###
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        with app.app_context():
            user = User.query.filter_by(email=email).first()
        
            if user and user.check_password(password):
                session['name'] = user.name
                session['email'] = user.email
                session['password'] = user.password

                return redirect(url_for('dashboard'))
            else:
                return render_template('index.html', error='Please check your email and password.')

    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        with app.app_context():
            new_user = User(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('name', None)
    session.pop('password', None)
    session.pop('result', None)
    return redirect(url_for('index'))

###route company page
@app.route('/company_list')
def company_list():
    if session['name']:
        with app.app_context():
            user = User.query.filter_by(email = session['email']).first()
        
        with app.app_context():
            companies = Company.query.all()
            print(companies)
    
        return render_template('company_list.html', user=user, companies=companies)

###route energy usage calculation page
@app.route('/cal_energyusage', methods=['GET','POST'])
def cal_energyusage():

    if session['name']:
        with app.app_context():
            user = User.query.filter_by(email = session['email']).first()
            companies = Company.query.all()
    
    if request.method == 'POST':
        month = int(request.form['month'])
        year = int(request.form['year'])
        company_id = int(request.form['company'])
        e_bill = float(request.form['e_bill'])
        g_bill = float(request.form['g_bill'])
        f_bill = float(request.form['f_bill'])
        energyUsage_result = float(request.form['resultFootPrint'])
        print(month)
        print(year)
        print(company_id)
        print(e_bill)
        print(g_bill)
        print(f_bill)
        print(energyUsage_result)
        with app.app_context():
            usage_ID = 0
            energyUsage_ID = 0
            queryUsage = Usage.query.filter_by(company_id=company_id, month=month, year=year)
            recordUsage = queryUsage.all()

            queryEnergyUsage = Energy.query.filter_by(company_id=company_id, month=month, year=year)
            recordEnergyUsage = queryEnergyUsage.all()

            for r in recordUsage:
                usage_ID = r.id
            
            for e in recordEnergyUsage:
                energyUsage_ID = e.id
            
            #usage table add and update
            if usage_ID == 0:
                new_Usage = Usage(energy = energyUsage_result, waste=0.0, fuel= 0.0, month=month, year=year, company_id=company_id)
                db.session.add(new_Usage)

                db.session.commit()
            else:
                usage = Usage.query.get(usage_ID)
                usage.energy = energyUsage_result
                db.session.add(usage)

                db.session.commit()
            
            #Energy Usage table add and update
            if(energyUsage_ID == 0):
                new_energyUsage = Energy(month = month, year = year, e_bill = e_bill, g_bill = g_bill, f_bill = f_bill, company_id=company_id)
                db.session.add(new_energyUsage)

                db.session.commit()
            else:
                energyUsage = Energy.query.get(energyUsage_ID)
                energyUsage.e_bill = e_bill
                energyUsage.g_bill = g_bill
                energyUsage.f_bill = f_bill
                db.session.add(energyUsage)

                db.session.commit()
            flash('Your calculated result has been saved successfully.', 'success')

        return redirect(url_for('cal_energyusage'))
    return render_template('cal_energyusage.html', user=user, companies=companies)

###route waste calculation page
@app.route('/cal_waste', methods=['GET','POST'])
def cal_waste():

    if session['name']:
        with app.app_context():
            user = User.query.filter_by(email = session['email']).first()
            companies = Company.query.all()
    
    if request.method == 'POST':
        month = int(request.form['month'])
        year = int(request.form['year'])
        company_id = int(request.form['company'])
        g_waste = float(request.form['gen_waste'])
        r_waste = float(request.form['rec_waste'])
        waste_result = float(request.form['resultFootPrint'])
        print(month)
        print(year)
        print(company_id)
        print(f'This is gen waste {g_waste}')
        print(r_waste)
        print(waste_result)

        with app.app_context():
            usage_ID = 0
            waste_ID = 0

            queryUsage = Usage.query.filter_by(company_id=company_id, month=month, year=year)
            recordUsage = queryUsage.all()

            waste = Waste.query.filter_by(company_id=company_id, month=month, year=year)
            recordWaste = waste.all()

            for r in recordUsage:
                usage_ID = r.id
            
            for e in recordWaste:
                waste_ID = e.id

            #usage table add and update
            if usage_ID == 0:
                new_Usage = Usage(waste = waste_result, energy=0.0, fuel= 0.0, month=month, year=year, company_id=company_id)
                db.session.add(new_Usage)

                db.session.commit()
            else:
                usage = Usage.query.get(usage_ID)
                usage.waste = waste_result
                db.session.add(usage)

                db.session.commit()
            
            #Energy Usage table add and update
            if(waste_ID == 0):
                new_Waste = Waste(month = month, year = year, g_waste = g_waste, r_waste = r_waste, company_id=company_id)
                db.session.add(new_Waste)

                db.session.commit()
            else:
                waste_Update = Waste.query.get(waste_ID)
                waste_Update.g_waste = g_waste
                waste_Update.r_waste = r_waste
                db.session.add(waste_Update)

                db.session.commit()
            flash('Your calculated result has been saved successfully.', 'success')
        return redirect(url_for('cal_waste'))
    return render_template('cal_waste.html', user=user, companies=companies)

###route business travel calculation page
@app.route('/cal_b_travel', methods=['GET','POST'])
def cal_b_travel():

    if session['name']:
        with app.app_context():
            user = User.query.filter_by(email = session['email']).first()
            companies = Company.query.all()
    
    if request.method == 'POST':
        month = int(request.form['month'])
        year = int(request.form['year'])
        company_id = int(request.form['company'])
        travel = float(request.form['b_travel'])
        fuel = float(request.form['fuel_eff'])
        bTravel_result = float(request.form['resultFootPrint'])
        print(month)
        print(year)
        print(company_id)
        print(travel)
        print(fuel)
        print(bTravel_result)

        with app.app_context():
            usage_ID = 0
            bTravel_ID = 0

            queryUsage = Usage.query.filter_by(company_id=company_id, month=month, year=year)
            recordUsage = queryUsage.all()

            bTravel = BusinessTravel.query.filter_by(company_id=company_id, month=month, year=year)
            recordbTravel = bTravel.all()

            for r in recordUsage:
                usage_ID = r.id
            
            for e in recordbTravel:
                bTravel_ID = e.id

            #usage table add and update
            if usage_ID == 0:
                new_Usage = Usage(fuel = bTravel_result, energy=0.0, waste= 0.0, month=month, year=year, company_id=company_id)
                db.session.add(new_Usage)

                db.session.commit()
            else:
                usage = Usage.query.get(usage_ID)
                usage.fuel = bTravel_result
                db.session.add(usage)

                db.session.commit()
            
            #Energy Usage table add and update
            if(bTravel_ID == 0):
                new_bTravel = BusinessTravel(month = month, year = year, b_travel = travel, avg_fuel = fuel, company_id=company_id)
                db.session.add(new_bTravel)

                db.session.commit()
            else:
                bTravel_Update = Waste.query.get(bTravel_ID)
                bTravel_Update.b_travel = travel
                bTravel_Update.avg_fuel = fuel
                db.session.add(bTravel_Update)

                db.session.commit()
            flash('Your calculated result has been saved successfully.', 'success')
        return redirect(url_for('cal_b_travel'))
    return render_template('cal_b_travel.html', user=user, companies=companies)

###route add company page
@app.route('/add_company', methods=['GET','POST'])
def add_company():
    if session['name']:
        with app.app_context():
            user = User.query.filter_by(email = session['email']).first()

    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        sector = request.form['sector']
        contact_person = request.form['c_person']
        email = request.form['email']
        postal_code = request.form['postalcode']

        with app.app_context():
            new_company = Company(name=name, address=address, sector=sector, contact_person=contact_person, email=email, postal_code=postal_code)

            db.session.add(new_company)
            db.session.commit()
        
        return redirect(url_for('company_list'))
    
    return render_template('add_company.html', user=user)
    
###route about page
@app.route('/about')
def about():
    if session['name']:
        with app.app_context():
            user = User.query.filter_by(email = session['email']).first()
        return render_template('about.html', user=user)
    
@app.route('/clear_session_result', methods=['POST'])
def clear_session_result():
    session.pop('result', None)
    return jsonify({"message": "Session result removed"}), 200

@app.route('/dashboard')
def dashboard():
     if session['name']:
        with app.app_context():
            user = User.query.filter_by(email = session['email']).first()
            companies = Company.query.all()
        return render_template('dashboard.html', user=user, companies=companies)

@app.route('/get_data', methods=['GET'])
def get_data():
    thisMonth = datetime.now()
    thisMonthNum = thisMonth.strftime("%m")
    lastMonth = thisMonth - relativedelta(months=1)
    lastMonthNum = lastMonth.strftime("%m")

    with app.app_context():

            record = db.session.query(Company, Usage).join(Usage, Usage.company_id == Company.id).filter(Usage.month == lastMonthNum).all()
            total = []
            company_name = []
            color = []

            for c, u in record:
                company_name.append(c.name)
                t = round((u.energy + u.waste + u.fuel),2)
                total.append(t)
                color.append(get_random_rgb())

            pie_data = {"labels": company_name, "values": total, "color": color, "label": "kgCO2FD"}
            return jsonify(pie_data)

@app.route('/get_table_data', methods=['GET'])
def get_table_data():
    thisMonth = datetime.now()
    thisMonthNum = thisMonth.strftime("%m")
    lastMonth = thisMonth - relativedelta(months=1)
    lastMonthNum = lastMonth.strftime("%m")

    with app.app_context():
        t_record = db.session.query(Company, Usage).join(Usage, Usage.company_id == Company.id).filter(Usage.month == lastMonthNum).all()
        comp_name = []
        comp_sect = []
        energy = []
        waste = []
        fuel = []
        tableData = []
    
        for c, u in t_record:
            comp_name.append(c.name)
            comp_sect.append(c.sector)
            energy.append(u.energy)
            waste.append(u.waste)
            fuel.append(u.fuel)
            eachCompany = {"name": c.name, "sector": c.sector, "energy": u.energy, "waste": u.waste, "fuel": u.fuel}
            tableData.append(eachCompany)
        
        t_data = {"comp_name": comp_name, "sector": comp_sect, "energy": energy, "waste": waste, "fuel": fuel}

        print(t_data)
    return jsonify(tableData)

def get_random_rgb():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))
##Get Dashboard Data
def get_dashboard_data(time_range):

    # Get the current date and time
    thisMonth = datetime.now()

    # Get the current month number (as a string)
    thisMonthNum = thisMonth.strftime("%m")
    print(f"Current Month: {thisMonthNum}")

    # Calculate the previous month using relativedelta
    lastMonth = thisMonth - relativedelta(months=1)
    lastMonthNum = lastMonth.strftime("%m")
    print(f"Last Month: {lastMonthNum}")
    current_date = datetime.now()

    if time_range == "last_3_month":
        with app.app_context():
            user = User.query.filter_by(email = session['email']).first()
            companies = Company.query.all()

            record = db.session.query(Company, Usage).join(Usage, Usage.company_id == Company.id).filter(Usage.month == lastMonthNum).all()
            total = []
            company_name = []
            color = []

            for c, u in record:
                company_name.append(c.name)
                t = round((u.energy + u.waste + u.fuel),2)
                total.append(t)
                color.append(get_random_rgb())

            pie_data = {"labels": company_name, "values": total, "color": color, "label": "kgCO2TT"}
        return pie_data
    elif time_range == "last_month":
        return {"title": "Last 3 Month"}
    elif time_range == "last_6_month":
        return {"title": "Last 3 Month"}
    else:
        return {"title": "Unknown Range"}

@app.route('/update_dashboard', methods=["GET","POST"])
def update_dashboard():
    time_range = request.json.get("selectedMonth")
    jdata = get_dashboard_data(time_range)
    return jdata

def get_last_three_months_with_year():
    today = datetime.today()
    last_three_months = [
        ((today - relativedelta(months=i)).year, (today - relativedelta(months=i)).month)
        for i in range(1, 4)
    ]
    return last_three_months


if __name__ == "__main__":
    app.run(debug=True)
