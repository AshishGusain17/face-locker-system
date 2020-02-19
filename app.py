from flask import Flask, render_template, url_for, request, redirect,Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import cv2
from getcrop import *
from profile_check import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

from time import time

inde = 0

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(200), nullable=False)
    mobile=db.Column(db.Integer,default=None)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')
    obj=inde
    # if request.method == 'POST':
    #     global inde
    #     inde = inde + 1
    #     task_content = request.form['content']
    #     new_task = Todo(content=task_content , number=inde)

    #     try:
    #         db.session.add(new_task)
    #         db.session.commit()
    #         return redirect('/')
    #     except:
    #         inde=inde-1
    #         return 'There was an issue adding your task'

    # else:
    #     tasks = Todo.query.order_by(Todo.date_created).all()
    #     return render_template('index.html', tasks=tasks,number=inde)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')
    else:
        name = request.form['name']
        email = request.form['email']
        data = Todo.query.order_by(Todo.date_created).all()
        if data:
            print(len(data))
            for obj in data:
                # ct=ct+1
                if obj.name == name:

                    if obj.name == name and  obj.email == email:
                        print(obj.name ,name , obj.email , email)
                        ans=pic_confirm(name)
                        if ans[0] ==True:
                            # return 
                            return "profile confirmed"
                        elif ans[0] == False:
                            return "fake profile"
                    else:
                        return "name email does not match"
            return "no such name exists"

        else:
            return "no data"




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        name = request.form['name']
        email = request.form['email']
        mobile =request.form['mobile'] 
        print(name ,email, mobile)
        fun(name)
        newaccount = Todo(name=name,email=email,mobile=mobile)
        try:
            db.session.add(newaccount)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your account'
        return redirect('/')



@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        global inde
        inde=inde-1
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)








if __name__ == "__main__":
    app.run(debug=True)
