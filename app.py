import flask
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

from flask_login import login_required, current_user
import flask_login

app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!
#
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
# Our mock database.
users = {'': {'password': 'admin'}}


# user maxin class provides the implementation of this properties. its the reason you can call
class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email != 'admin':
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user




app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# to avoid warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# for creating database
db = SQLAlchemy(app)


# database Schema


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    complete = db.Column(db.Boolean)


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Credential is not correct please try again.'
        else:
            user = User()
            user.id = 'admin'
            flask_login.login_user(user)
            return flask.redirect(flask.url_for('home'))

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template('logout.html')


@app.route('/')
@flask_login.login_required
def home():
    # get list of all the item
    query = Todo.query.order_by(Todo.id.desc())
    todo_list = query
    return render_template('base.html', todo_list=todo_list)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # rendering the template
    # authenticate user


@app.route('/add', methods=["Post"])
def add():
    # adding tasks
    title = request.form.get("title")
    first_todo = Todo(title=title, complete=False)
    db.session.add(first_todo)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/update/<int:todo_id>')
def update(todo_id):
    # adding tasks
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    # adding tasks
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    # first_todo = Todo(title="todo 1", complete=False)
    # db.session.add(first_todo)
    # db.session.commit()
    app.run(debug=True)
