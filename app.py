from flask import Flask, render_template, url_for, request, redirect,Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from camera import *
# import cv2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

from time import time

inde = 0

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    number=db.Column(db.Integer,default=None)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        global inde
        inde = inde + 1
        task_content = request.form['content']
        new_task = Todo(content=task_content , number=inde)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            inde=inde-1
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks,number=inde)




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



def gen(camera):
    co=0
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')        
    

@app.route('/check')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/check1')
# def check1():
#     cap = cv2.VideoCapture(0)
#     while 1:
#         _,frame=cap.read()
#         cv2.imshow('frame',frame)
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
#     cap.release()
#     cv2.destroyAllWindows()
#     return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)
