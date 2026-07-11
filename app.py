from flask import Flask,render_template, request,redirect
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
        user=User.query.filter_by(mail=mail,password=password).first()
        if user:
            return render_template("homepage.html")
        else:
            return "Invalid password"
    return render_template('loginp.html') 

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        name=request.form['name']
        mail=request.form['mail']
        password=request.form['password']
        role=request.form['role']

        if role=="Trek Staff":
            status = "Pending"
        else:
            status = "Approved"

        new_user = User(name=name,mail=mail,password=password,role=role,status=status)
        db.session.add(new_user)
        db.session.commit()
        return f"{name} registered successfully as {role}"

    return render_template('register.html')
@app.route('/homepage')
def homepage():
    total_treks = Trek.query.count()
    total_users = User.query.filter_by(role="User").count()
    total_staff = User.query.filter_by(role="Trek Staff").count()
    total_bookings = Booking.query.count()
    return render_template('homepage.html',total_treks=total_treks,total_users=total_users,total_staff=total_staff,
        total_bookings=total_bookings)

@app.route('/manage_trek')
def manage_trek():
    treks=Trek.query.all()
    return render_template("manage_trek.html",treks=treks)

@app.route('/add_trek', methods=['GET', 'POST'])
def add_trek():
    if request.method == 'POST':
        trek_name = request.form['trek_name']
        location = request.form['location']
        difficulty = request.form['difficulty']
        duration = request.form['duration']
        slots = request.form['slots']
        status = request.form['status']
        new_trek = Trek(trek_name=trek_name, location=location, difficulty=difficulty, duration=duration, slots=slots, status=status)
        db.session.add(new_trek)
        db.session.commit()
        return redirect('/manage_trek')
    return render_template("add_trek.html")

@app.route('/edit_trek/<int:id>', methods=['GET', 'POST'])
def edit_trek(id):
    trek = Trek.query.get(id)
    if request.method == 'POST':
        trek.trek_name = request.form['trek_name']
        trek.location = request.form['location']
        trek.difficulty = request.form['difficulty']
        trek.duration = request.form['duration']
        trek.slots = request.form['slots']
        trek.status = request.form['status']
        db.session.commit()
        return redirect('/manage_trek')
    return render_template("add_trek.html", trek=trek)

@app.route('/delete_trek/<int:id>')
def delete_trek(id):
    trek = Trek.query.get(id)
    db.session.delete(trek)
    db.session.commit()
    return redirect('/manage_trek')
if __name__ == '__main__': 
    app.run(debug=True)
 