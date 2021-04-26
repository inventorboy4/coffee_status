from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
import time

from data import db_session
from data.login_form import LoginForm
from data.objects import Objects
from data.register import RegisterForm
from data.users import User
from data.add_device import AddDeviceForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def start(update, context):
    reply_keyboard = [['/status', '/site']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text(
        "Используйте /status для проверки состояния устройства",
        reply_markup=markup
    )


def site(update, context):
    update.message.reply_text('http://127.0.0.1:5000/')


def status(update, context):
    update.message.reply_text(str(time.asctime()) + ' - status: online')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    objects = db_sess.query(Objects).all()
    users = db_sess.query(User).all()
    names = {name.id: name.name for name in users}
    return render_template("index.html", objects=objects, names=names, title='iviRayMS')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пользователь с этим именем уже зарегистрирован")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Вход', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/addobject', methods=['GET', 'POST'])
def addjob():
    add_form = AddDeviceForm()
    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        device = Objects(
            device=add_form.device.data,
            creator=add_form.creator.name,
            users=add_form.users.data,
            status=add_form.status.data,
            is_working=add_form.is_working.data
        )
        db_sess.add(device)
        db_sess.commit()
        return redirect('/')
    return render_template('adddevice.html', title='Добавление устройства', form=add_form)


@app.route('/easter_egg')
def image():
    return f'''<img src="{url_for('static', filename='img/easteregg.jpeg')}" 
           alt="здесь должна была быть картинка, но не нашлась">'''


def tele_main():
    updater = Updater('1618420717:AAFvqGcbdds9103SB1SYzUz9-RFjJBzDn4k', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler('status', status))
    dp.add_handler(CommandHandler('site', site))
    updater.start_polling()
    updater.idle()


def main():
    db_session.global_init("db/coffee.sqlite")
    app.run()


if __name__ == '__main__':
    # tele_main()
    main()

