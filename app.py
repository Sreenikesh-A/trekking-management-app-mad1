from flask import Flask,render_template, request
from config import Config
from models import db,User,Trek,Booking
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail=request.form['mail']
        password=request.form['password']
        return render_template("homepage.html")
    return render_template('loginp.html') 

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        name=request.form['name']
        mail=request.form['mail']
        password=request.form['password']
        role=request.form['role']

        new_user = User(name=name,mail=mail,password=password,role=role)
        db.session.add(new_user)
        db.session.commit()
        return f"{name} registered successfully as {role}"

    return render_template('register.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/manage_trek')
def manage_trek():
    return render_template("manage_trek.html")

@app.route('/add_trek', methods=['GET', 'POST'])
def add_trek():
    if request.method == 'POST':
        trek_name = request.form['trek_name']
        location = request.form['location']
        difficulty = request.form['difficulty']
        duration = request.form['duration']
        slots = request.form['slots']
        status = request.form['status']
        return "Trek Added Successfully"
    return render_template("add_trek.html")
if __name__ == '__main__': 
    app.run(debug=True)
 