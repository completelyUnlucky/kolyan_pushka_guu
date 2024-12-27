from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import LoginForm, SignupForm, RequestForm
from models import db, User, Request
from email_validator import validate_email
import logging


app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

logging.basicConfig(level=logging.DEBUG)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/profile')
@login_required
def profile():
    return render_template('lk.html', user=current_user)


@app.route('/')
def base():
    requests_list = Request.query.all()
    return render_template('base.html', requests=requests_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_url = request.args.get('next')
        if next_url is None or not next_url.startswith('/'):
            next_url = url_for('profile')
        return redirect(next_url)
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = SignupForm()
    if form.validate_on_submit():
        try:
            validated_email = validate_email(form.email.data).normalized
            user = User(username=form.username.data, email=validated_email)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            logging.debug("User added to database")
            flash('User created successfully')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Error: ' + str(e))
            logging.error("Database error: " + str(e))
            return redirect(url_for('signup'))
    return render_template('signup.html', form=form)


@app.route('/place_request', methods=['GET', 'POST'])
@login_required
def place_request():
    form = RequestForm()
    if form.validate_on_submit():
        request = Request(description=form.description.data, payment_amount=form.payment_amount.data, user_id=current_user.id)
        db.session.add(request)
        db.session.commit()
        flash('Заявка размещена успешно')
        return redirect(url_for('base'))
    return render_template('place_request.html', form=form)


@app.route('/request/<int:request_id>')
def view_request(request_id):
    request = Request.query.get_or_404(request_id)
    return render_template('view_request.html', request=request)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
