from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify, json, send_file
from model import db, app, User, Company, Energy, Waste, BusinessTravel, Usage
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import base64



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

            pie_data = {"labels": company_name, "values": total, "color": color, "label": "kgCO2"}
            #print(jsonify(pie_data))
            return jsonify(pie_data)
#for page load table data
@app.route('/get_table_data', methods=['GET'])
def get_table_data():
    thisMonth = datetime.now()
    lastMonth = thisMonth - relativedelta(months=1)
    lastMonthNum = lastMonth.strftime("%m")

    with app.app_context():
        t_record = db.session.query(Company, Usage).join(Usage, Usage.company_id == Company.id).filter(Usage.month == lastMonthNum).all()
        tableData = []

    
        for c, u in t_record:
            eachCompany = {"name": c.name, "sector": c.sector, "energy": u.energy, "waste": u.waste, "fuel": u.fuel, "month": u.month, "year": u.year}
            tableData.append(eachCompany)

    return jsonify(tableData)

#last 3 months, all companies, for pie and bar
@app.route('/get_calc_data', methods=['GET'])
def get_calc_data():
    month = request.args.get('selected_Month')
    company = request.args.get('company')
    company_id = int(company)
    total_energy = 0.0
    total_waste = 0.0
    total_fuel = 0.0

    if month == 'last_month' and company_id == 0:
        thisMonth = datetime.now()
        thisMonthNum = thisMonth.strftime("%m")
        lastMonth = thisMonth - relativedelta(months=1)
        lastMonthNum = lastMonth.strftime("%m")
        company_totals = {}

        with app.app_context():

            records = db.session.query(Company.name, Company.sector, Usage.energy, Usage.waste, Usage.fuel).join(Usage, Usage.company_id == Company.id).filter(Usage.month == lastMonthNum).all()
            #print(record)
            total = []
            company_name = []
            color = []
            for record in records:
                company, sector, *values = record
                total_for_entry = sum(values)
                if company not in company_totals:
                    company_totals[company] = {"sector": sector, "total": 0, "color": get_random_rgb()}
                    company_totals[company]["total"] += total_for_entry
             
                #pie_data = {"labels": company_name, "values": total, "color": color, "label": "kgCO2"}
                result = [{"labels": company, "sector": info["sector"], "color": info["color"],"values": round(info["total"],2), "label": "kgCO2"} for company, info in company_totals.items()] 
        #print("...........Last Month.................")
        #print(result)
        return jsonify(result)
    if month == 'last_3_months' and company_id == 0:
        three_months = get_last_three_months_with_year()
        company_totals = {}
        for m in three_months:
            year, month = m
        
            with app.app_context():
                records = db.session.query(Company.name, Company.sector, Usage.energy, Usage.waste, Usage.fuel).join(Usage, Usage.company_id == Company.id).filter(Usage.month == month and Usage.year == year).all()

                for record in records:
                
                    company, sector, *values = record
                    total_for_entry = sum(values)
                    if company not in company_totals:
                        company_totals[company] = {"sector": sector, "total": 0, "color": get_random_rgb()}
                    company_totals[company]["total"] += total_for_entry
             
                result = [{"labels": company, "sector": info["sector"], "color": info["color"],"values": round(info["total"],2), "label": "kgCO2"} for company, info in company_totals.items()] 
        return jsonify(result)

    if month == 'last_6_months' and company_id == 0:
        company_totals = {}
        six_months = get_last_six_months_with_year()

        for m in six_months:
            year, month = m
        
            with app.app_context():
                records = db.session.query(Company.name, Company.sector, Usage.energy, Usage.waste, Usage.fuel).join(Usage, Usage.company_id == Company.id).filter(Usage.month == month and Usage.year == year).all()
                # print(records)
                for record in records:
                    
                    company, sector, *values = record
                    total_for_entry = sum(values)
                    if company not in company_totals:
                        company_totals[company] = {"sector": sector, "total": 0, "color": get_random_rgb()}
                    company_totals[company]["total"] += total_for_entry
                
                result = [{"labels": company, "sector": info["sector"], "color": info["color"],"values": round(info["total"],2), "label": "kgCO2"} for company, info in company_totals.items()] 
        #print("...........Six Month.................")
        #print(result)
        return jsonify(result)
    
    if month == 'last_month' and company != 0:
        thisMonth = datetime.now()
        thisMonthNum = thisMonth.strftime("%m")
        lastMonth = thisMonth - relativedelta(months=1)
        t_month = lastMonth.strftime("%m")

        with app.app_context():

            records = db.session.query(Company.name, Company.sector, Usage.energy, Usage.waste, Usage.fuel).join(Usage, Usage.company_id == Company.id).filter(Usage.month == t_month, Usage.company_id == company_id).all()
            #print(records)
            
            for record in records:
                company, sector, energy, waste, fuel = record

                total_energy = total_energy + round(energy,2)
                total_waste = total_waste + round(waste,2)
                total_fuel = total_fuel + round(fuel,2)


            result = [{"labels": ["Engery", "Fuel", "Waste"], "values": [total_energy, total_fuel, total_waste], "color": [get_random_rgb(),get_random_rgb(),get_random_rgb()],"label": "kgCO2"}]

            #print(result)

        return jsonify(result)
    if month == 'last_3_months' and company != 0:
        three_months = get_last_three_months_with_year()
        company_totals = {}
        for m in three_months:
            t_year, t_month = m
        
            with app.app_context():
                records = db.session.query(Company.name, Company.sector, Usage.energy, Usage.waste, Usage.fuel).join(Usage, Usage.company_id == Company.id).filter(Usage.month == t_month, Usage.year == t_year, Usage.company_id == company_id).all()
                # print("Three months data of one company")
                # print(t_month)
                # print(company_id)
                #print(records)

                for record in records:
                    print(record)
                    company, sector, energy, waste, fuel = record

                    total_energy = total_energy + round(energy,2)
                    total_waste = total_waste + round(waste,2)
                    total_fuel = total_fuel + round(fuel,2)


            result = [{"labels": ["Engery", "Fuel", "Waste"], "values": [total_energy, total_fuel, total_waste], "color": [get_random_rgb(),get_random_rgb(),get_random_rgb()],"label": "kgCO2"}]

            #print(result)

        return jsonify(result)
    if month == 'last_6_months' and company != 0:
        six_months = get_last_six_months_with_year()
        company_totals = {}
        for m in six_months:
            t_year, t_month = m

            with app.app_context():
                records = db.session.query(Company.name, Company.sector, Usage.energy, Usage.waste, Usage.fuel).join(Usage, Usage.company_id == Company.id).filter(Usage.month == t_month, Usage.year == t_year, Usage.company_id == company_id).all()

                for record in records:
                    print(record)
                    company, sector, energy, waste, fuel = record

                    total_energy = total_energy + round(energy,2)
                    total_waste = total_waste + round(waste,2)
                    total_fuel = total_fuel + round(fuel,2)


            result = [{"labels": ["Engery", "Fuel", "Waste"], "values": [total_energy, total_fuel, total_waste], "color": [get_random_rgb(),get_random_rgb(),get_random_rgb()],"label": "kgCO2"}]

        return jsonify(result)
    # if company_id != 0:
    #     #t_month, t_year = 0
    #     company_totals = {}

    #     if month == 'last_month':
    #         lastMonth = get_last_three_months_with_year()
    #         company_totals = {}
    #         for m in lastMonth:
    #             t_year, t_month = m

    #     elif month == 'last_3_months':
    #         three_months = get_last_three_months_with_year()
    #         company_totals = {}
    #         for m in three_months:
    #             t_year, t_month = m

    #     else:
    #         six_months = get_last_six_months_with_year()
    #         company_totals = {}
    #         for m in six_months:
    #             t_year, t_month = m
        
    #     with app.app_context():
    #         records = db.session.query(Company.name, Company.sector, Usage.energy, Usage.waste, Usage.fuel).join(Usage, Usage.company_id == Company.id).filter(Usage.month == t_month, Usage.year == t_year, Usage.company_id == company_id).all()

    #         for record in records:
    #             #print(record)
    #             company, sector, energy, waste, fuel = record

    #             total_energy = total_energy + round(energy,2)
    #             total_waste = total_waste + round(waste,2)
    #             total_fuel = total_fuel + round(fuel,2)


    #         result = [{"labels": ["Engery", "Fuel", "Waste"], "values": [total_energy, total_fuel, total_waste], "color": [get_random_rgb(),get_random_rgb(),get_random_rgb()],"label": "kgCO2"}]
    #     return jsonify(result)

    
#for last 6 months table data
@app.route('/fetchCalcTableData', methods=['GET'])
def fetchCalcTableData():
    month = request.args.get('selected_Month')
    company = request.args.get('company')
    company_id = int(company)

    if month == 'last_month' and company_id == 0:
        thisMonth = datetime.now()
        lastMonth = thisMonth - relativedelta(months=1)
        lastMonthNum = lastMonth.strftime("%m")

        with app.app_context():
            t_records = db.session.query(Company.name, Company.sector, Usage.energy, Usage.waste, Usage.fuel, Usage.month, Usage.year).join(Usage, Usage.company_id == Company.id).filter(Usage.month == lastMonthNum).all()
            tableData = []

            for r in t_records:
                eachCompany = {"name": r.name, "sector": r.sector, "energy": r.energy, "waste": r.waste, "fuel": r.fuel, "month": r.month, "year": r.year}
                
                tableData.append(eachCompany)

            return jsonify(tableData)

    if month == 'last_3_months' and company_id == 0:
        tableData = []
        t_records=[]
        three_months = get_last_three_months_with_year()
        for m in three_months:
            t_year, t_month = m
            
            with app.app_context():
                t_records = db.session.query(Company.name, Company.sector, Usage.energy, Usage.waste, Usage.fuel, Usage.month, Usage.year).join(Usage, Usage.company_id == Company.id).filter(Usage.month == t_month and Usage.year == t_year).all()
                
                for r in t_records:
                    eachCompany = {"name": r.name, "sector": r.sector, "energy": r.energy, "waste": r.waste, "fuel": r.fuel, "month": r.month, "year": r.year}
                
                    tableData.append(eachCompany)
        return jsonify(tableData)

    if month == 'last_6_months' and company_id == 0:
        tableData = []
        t_records=[]
        six_months = get_last_six_months_with_year()
        for m in six_months:
            t_year, t_month = m
            
            with app.app_context():
                t_records = db.session.query(Company.name, Company.sector, Usage.energy, Usage.waste, Usage.fuel, Usage.month, Usage.year).join(Usage, Usage.company_id == Company.id).filter(Usage.month == t_month and Usage.year == t_year).all()
                
                for r in t_records:
                    eachCompany = {"name": r.name, "sector": r.sector, "energy": r.energy, "waste": r.waste, "fuel": r.fuel, "month": r.month, "year": r.year}
                
                    tableData.append(eachCompany)
        return jsonify(tableData)
    if month == 'last_month' and company_id != 0:
        thisMonth = datetime.now()
        lastMonth = thisMonth - relativedelta(months=1)
        lastMonthNum = lastMonth.strftime("%m")

        with app.app_context():
            t_records = db.session.query(Company.name, Company.sector, Usage.energy, Usage.waste, Usage.fuel, Usage.month, Usage.year).join(Usage, Usage.company_id == Company.id).filter(Usage.month == lastMonthNum, Usage.company_id == company_id).all()
            tableData = []

            for r in t_records:
                eachCompany = {"name": r.name, "sector": r.sector, "energy": r.energy, "waste": r.waste, "fuel": r.fuel, "month": r.month, "year": r.year}
                
                tableData.append(eachCompany)

            return jsonify(tableData)
    if month == 'last_3_months' and company_id != 0:
        tableData = []
        t_records=[]
        three_months = get_last_three_months_with_year()
        for m in three_months:
            t_year, t_month = m
            
            with app.app_context():
                # t_records = db.session.query(Company.name, Company.sector, Usage.energy, Usage.waste, Usage.fuel, Usage.month, Usage.year).join(Usage, Usage.company_id == Company.id).filter(Usage.month == month, Usage.year == year, Usage.company_id == company_id).all()
                t_records = db.session.query(Company.name, Company.sector, Usage.energy, Usage.waste, Usage.fuel, Usage.month, Usage.year).join(Usage, Usage.company_id == Company.id).filter(Usage.month == t_month, Usage.year == t_year, Usage.company_id == company_id).all()
                
                for r in t_records:
                    eachCompany = {"name": r.name, "sector": r.sector, "energy": r.energy, "waste": r.waste, "fuel": r.fuel, "month": r.month, "year": r.year}
                
                    tableData.append(eachCompany)
        #print(f"Table data com not 0:................{tableData}")
        return jsonify(tableData)
    if month == 'last_6_months' and company_id != 0:
        tableData = []
        t_records=[]
        six_months = get_last_six_months_with_year()
        for m in six_months:
            t_year, t_month = m
            
            with app.app_context():
                t_records = db.session.query(Company.name, Company.sector, Usage.energy, Usage.waste, Usage.fuel, Usage.month, Usage.year).join(Usage, Usage.company_id == Company.id).filter(Usage.month == t_month, Usage.year == t_year, Usage.company_id == company_id).all()
                
                for r in t_records:
                    eachCompany = {"name": r.name, "sector": r.sector, "energy": r.energy, "waste": r.waste, "fuel": r.fuel, "month": r.month, "year": r.year}
                
                    tableData.append(eachCompany)
        print(f"Table 6m data com not 0:................{tableData}")
        return jsonify(tableData)
    
#generate pdf report
@app.route('/export', methods=['POST'])
def export():
    data = request.get_json()

    # Create a PDF in memory
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
   
    # Add table to the PDF
    table_html = data['table']
    c.drawString(100, 750, "Table:")
    c.drawString(100, 735, table_html)  # Simple representation, you may want to format the table more
   
    # Add pie and bar charts as images
    y_position = 650
    for chart_data in data['charts']:
        image_data = base64.b64decode(chart_data.split(',')[1])
        image = Image.open(BytesIO(image_data))
        image.save("temp_chart.png", "PNG")
        c.drawImage("temp_chart.png", 100, y_position, width=400, height=300)
        y_position -= 310  # Adjust for next chart's position
   
    # Save the PDF
    c.save()
    pdf_buffer.seek(0)

    # Send the PDF to the client
    return send_file(pdf_buffer, as_attachment=True, download_name="dashboard_export.pdf", mimetype="application/pdf")
#
@app.route('/get_calc_table_data', methods=['GET'])
def get_calc_table_data():
    return jsonify("Pass")

#get last month
def get_last_month_with_year():
    today = datetime.today()
    last_month = today - relativedelta(months=1)
    return last_month.year, last_month.month


#get last three months. months and years
def get_last_three_months_with_year():
    today = datetime.today()
    last_three_months = [
        ((today - relativedelta(months=i)).year, (today - relativedelta(months=i)).month)
        for i in range(1, 4)
    ]
    # print(last_three_months)
    return last_three_months


#get last six months. months and years
def get_last_six_months_with_year():
    today = datetime.today()
    last_six_months = [
        ((today - relativedelta(months=i)).year, (today - relativedelta(months=i)).month)
        for i in range(1, 7)  # Change this to 7 to include the last 6 months
    ]
    return last_six_months


#get random color
def get_random_rgb():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

if __name__ == "__main__":
    app.run(debug=True)
