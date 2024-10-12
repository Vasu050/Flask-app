from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 


app=Flask(__name__)
#/// for relative path //// for absolute path
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:vasu2005@localhost/test_db'
db=SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self):
     return f'Task {self.id}'
    
with app.app_context():
    db.create_all()  # This line will create the 'test.db' file if it doesn't exist
    print("Database and tables created!")
    
@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
       task_content=request.form['addtext']
       new_task=Todo(content=task_content)
      # return 'hello'
       try:
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
       
       except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return'ISSUE' 
    else:
    #  tasks = Todo.query.all()
       tasks=Todo.query.order_by(Todo.date_created).all()
       return render_template('index.html',tasks=tasks)
       # return "Hello World"

@app.route('/Delete/<int:id>',methods=['GET','POST']) #name can be anything id or task_id
def delete(id):
   task_to_delete=Todo.query.get_or_404(id)
   
   try:
      db.session.delete(task_to_delete)
      db.session.commit()
      return redirect('/')
   except:
      return "error deleting"

@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    task_to_update = Todo.query.get_or_404(id)
    new_content = request.form['task_content']
    task_to_update.content = new_content

    try:
        db.session.commit()
        return redirect('/')
    except:
        db.session.rollback()
        return "Error updating task"


if __name__=="__main__":
    app.run(debug=True)