from flask import Flask, request, render_template, redirect, url_for, session
from model import db, app, User

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
        return render_template('company_list.html', user=user)
    
###route calculation page
@app.route('/calculation')
def calculation():
    if session['name']:
        with app.app_context():
            user = User.query.filter_by(email = session['email']).first()
        return render_template('calculation.html', user=user)
    
###route add company page
@app.route('/add_company')
def add_company():
    if session['name']:
        with app.app_context():
            user = User.query.filter_by(email = session['email']).first()
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
