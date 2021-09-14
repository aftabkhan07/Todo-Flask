from flask import Flask, render_template, request, redirect #we use render to read html from templates request to get info from form and redirect to change the site
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db" #we can change the databasename and the folder we want it to be put
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

# to make our database
class Todo(db.Model):                                     
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
# return the 2 imp values when try to print all the database in terminal
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET', 'POST']) # to receive the filled variables from the form
def hello_world():
    if request.method=='POST':         # if recieved data
        title = request.form['title']   #using the recieved data
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)   #putting the data in database
        db.session.add(todo)                  #committing the data to database
        db.session.commit()
        
    allTodo = Todo.query.all()                                 #after if just print tall the query
    return render_template('index.html', allTodo=allTodo)      #to go in the index template and use alltodo by jinja

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is products page'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])     #/update/<int:sno> when go to this site just use the sno 
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()        #using sno to filter from database and make changes
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()               #to change the sno which was passed
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)

