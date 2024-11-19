from flask import Flask, request, render_template, redirect, url_for, session
from model import db, app, User, Company

socketio = SocketIO(app)
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


    #return redirect('index.html')
    '''
        if session['name']:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('index'))
    '''
@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('name', None)
    session.pop('password', None)
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

###route calculation page
@app.route('/calculation', methods=['GET','POST'])
def calculation():

    result = 0
    e_bill = 0.0

    if session['name'] and request.method == 'GET':
        with app.app_context():
            user = User.query.filter_by(email = session['email']).first()
            companies = Company.query.all()

    if request.method == 'POST':

        type = request.form['formSelector']

        month = request.form['month']
        year = request.form['year']

        #companyid
        company_id = int(request.form['company'])

        #for energy usage
        e_bill = round(float(request.form['e_bill']),2)
        g_bill = round(float(request.form['g_bill']),2)
        f_bill = round(float(request.form['f_bill']),2)

        #for waste
        gen_waste = request.form['gen_waste']
        rec_waste = request.form['rec_waste']

        #for travel
        b_travel = request.form['b_travel']
        fuel_eff = request.form['fuel_eff']

        if type == 'energyusage':
            result = (e_bill) * 12 * 0.0005 + (g_bill) * 12 * 0.0053 + (f_bill) * 12 * 2.32
            session['result'] = {'result':result}
            return redirect(url_for('calculation'))
        elif type == 'waste':
            pass
        else:
            pass

    return render_template('calculation.html', user=user, companies=companies)


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

if __name__ == "__main__":
    app.run(debug=True)
