from flask import Flask,render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy


app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
#to avoid warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#for creating database
db = SQLAlchemy(app)

#database Schema
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    complete = db.Column(db.Boolean)

# Decorator to link the function to url
@app.route('/')
def home():
    #get list of all the item
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('base.html', todo_list=todo_list) 

@app.route('/welcome')
def welcome():
    return render_template('welcome.html') # rendering the template
    #authenticate user
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method =='POST':
        if  request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error= 'Credential is not correct please try agian.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

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
    todo = Todo.query.filter_by(id= todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    # adding tasks
    todo = Todo.query.filter_by(id= todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    db.create_all()
    # first_todo = Todo(title="todo 1", complete=False)
    # db.session.add(first_todo)
    # db.session.commit()   
    app.run(debug= True)