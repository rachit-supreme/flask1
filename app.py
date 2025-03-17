from flask import Flask,render_template,url_for,request,redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
    
logging.basicConfig(level=logging.DEBUG)

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)


    def __repr__(self):
        return '<Task %r>' % self.id

with app.app_context():
    db.create_all()

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form.get('content')
        
        if not task_content:
            return 'Content is required', 400
        
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            db.session.rollback()
            logging.error(f'Error adding task: {e}')
            return f'There was an issue adding your task: {str(e)}', 500
    else:
        try:
            tasks = Todo.query.order_by(Todo.date_created).all()
            return render_template('index.html', tasks=tasks)
        except Exception as e:
            logging.error(f'Error fetching tasks: {e}')
            return f'There was an issue fetching tasks: {str(e)}', 500

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error deleting task: {e}')
        return f'There was an issue deleting your task: {str(e)}', 500

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id): 
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
       task.content = request.form.get('content')

       try:
              db.session.commit()
              return redirect('/')
       except Exception as e:
              db.session.rollback()
              logging.error(f'Error updating task: {e}')
              return f'There was an issue updating your task: {str(e)}', 500

    else:
        return render_template('update.html',task=task)
if __name__ == '__main__':
    app.run(debug=True)
