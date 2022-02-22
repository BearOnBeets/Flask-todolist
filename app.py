from asyncio import tasks
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tasks.db'
db = SQLAlchemy(app)

class Tasks(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    tname = db.Column(db.String(100) , nullable=False)
    description = db.Column(db.Text(100) , nullable=False)
    # author = db.Column(db.String(20) , nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return 'Blog Post id: '+ str(self.id)




@app.route('/')
def index():
    return render_template('createtask.html')


@app.route('/tasks',methods=['GET','POST'])
def post():
    if request.method =='POST':
        tname = request.form['tname']
        description = request.form['description']
        new_task = Tasks(tname=tname,description=description)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/alltasks')
    else:
        return redirect('/')
        # return render_template('post.html')

@app.route('/alltasks')
def display():
    all_tasks = Tasks.query.all()
    return render_template('alltasks.html',tasks =all_tasks)
    


@app.route('/delete/<int:id>')
def delete(id):
    task = Tasks.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/alltasks')

@app.route('/edit/<int:id>',  methods=['GET','POST'])
def edit(id):
    if request.method == 'POST':
        task = Tasks.query.get_or_404(id)
        task.tname = request.form['tname']
        task.description = request.form['description']
        db.session.commit()
        return redirect('/alltasks')
    else:
        task = Tasks.query.get_or_404(id)
        return render_template('createtask.html',task=task)


@app.route('/search', methods=['GET'])
def search():
    searchword = request.args.get('search')
    tasks=Tasks.query.filter(Tasks.tname.like(searchword)).all()
    return render_template('search.html',tasks=tasks)


if __name__ == "__main__":
    app.run(debug=True)