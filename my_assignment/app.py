from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from model import db, app, User, Company

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
                return render_template('index.html', error='Invalid user')

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

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if session['name']:
        with app.app_context():
            user = User.query.filter_by(email = session['email']).first()
        return render_template('dashboard.html', user=user)

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
        company = int(request.form['company'])
        e_bill = float(request.form['e_bill'])
        g_bill = float(request.form['g_bill'])
        f_bill = float(request.form['f_bill'])
        result = float(request.form['resultFootPrint'])
        print(month)
        print(year)
        print(company)
        print(e_bill)
        print(g_bill)
        print(f_bill)
        print(result)
        
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
        pass

    return render_template('cal_waste.html', user=user, companies=companies)

###route business travel calculation page
@app.route('/cal_b_travel', methods=['GET','POST'])
def cal_b_travel():

    if session['name']:
        with app.app_context():
            user = User.query.filter_by(email = session['email']).first()
            companies = Company.query.all()
    
    if request.method == 'POST':
        pass

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

if __name__ == "__main__":
    app.run(debug=True)
