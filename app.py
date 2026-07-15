from flask import Flask,render_template, request,redirect,session
from config import Config
from models import db,User,Trek,Booking
app = Flask(__name__)
app.secret_key ='sree_secret_key'
app.config.from_object(Config)
db.init_app(app)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail=request.form['mail']
        password=request.form['password']
        user=User.query.filter_by(mail=mail,password=password).first()
        if user:
            session['user_id'] = user.id
            if user.role == "Trek Staff":
                if user.status == "Pending":
                    return "Your account is waiting for admin approval."
                if user.status == "Blacklisted":
                    return "Your account has been blacklisted."
                return redirect(f'/staff_page/{user.id}')
            
            elif user.role == "User":
                return redirect('/user_page')
            else:
                return redirect('/homepage')
        else:
            return "Invalid Email or Password"
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
        return redirect('/')

    return render_template('register.html')
@app.route('/homepage')
def homepage():  #admin page
    total_treks = Trek.query.count()
    total_users = User.query.filter_by(role="User").count()
    total_staff = User.query.filter_by(role="Trek Staff").count()
    total_bookings = Booking.query.count()
    return render_template('homepage.html',total_treks=total_treks,total_users=total_users,total_staff=total_staff,
        total_bookings=total_bookings)

@app.route('/manage_trek')
def manage_trek():
    search=request.args.get('search')
    if search:
        treks=Trek.query.filter(Trek.trek_name.contains(search)).all()
    else:
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

@app.route('/manage_staff')
def manage_staff():
    search=request.args.get('search')
    if search:
        staffs = User.query.filter(User.role=="Trek Staff",User.name.contains(search)).all()
    else:
        staffs = User.query.filter_by(role="Trek Staff").all()
    return render_template("manage_staff.html",staffs=staffs)

@app.route('/approve_staff/<int:id>')
def approve_staff(id):
    staff = User.query.get(id)
    staff.status = "Approved"
    db.session.commit()
    return redirect('/manage_staff')  

@app.route('/blacklist_staff/<int:id>')
def blacklist_staff(id):
    staff = User.query.get(id)
    staff.status = "Blacklisted"
    db.session.commit()
    return redirect('/manage_staff')

@app.route('/assign_staff/<int:id>', methods=['GET', 'POST'])
def assign_staff(id):
    trek = Trek.query.get(id)
    staffs = User.query.filter_by(role="Trek Staff",status="Approved").all()
    if request.method == 'POST':
        trek.assigned_staff_id = request.form['staff_id']
        db.session.commit()
        return redirect('/manage_trek')

    return render_template("assign_staff.html",trek=trek,staffs=staffs)

@app.route('/staff_page/<int:id>')
def staff_page(id):
    treks = Trek.query.filter_by(assigned_staff_id=id).all()
    return render_template("staff_page.html",treks=treks)

@app.route('/user_page')
def user_page():
    treks = Trek.query.filter_by(status="Open").all()
    return render_template("user_page.html",treks=treks)  

@app.route('/book_trek/<int:id>')
def book_trek(id):
    trek = Trek.query.get(id)
    existing_booking = Booking.query.filter_by(user_id=session['user_id'],trek_id=id).first()
    if existing_booking:
        return "You have already booked this trek."
    if trek.slots > 0:
        trek.slots = trek.slots - 1
        new_booking = Booking(user_id=session['user_id'],trek_id=trek.id,status="Booked")
        db.session.add(new_booking)                                                                                                                                                                 
        db.session.commit()
    
        return redirect('/user_page')
    return "No Slots Available"
    
@app.route('/booking_history')
def booking_history():
    bookings = Booking.query.all()
    return render_template("booking_history.html",bookings=bookings) 

@app.route('/my_bookings')
def bookings():
    bookings = Booking.query.filter_by(user_id=session['user_id']).all()
    return render_template("bookings.html",bookings=bookings)  

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/manage_bookings')
def manage_bookings():
    bookings = Booking.query.all()
    return render_template("manage_bookings.html",bookings=bookings)

@app.route('/participants/<int:id>')
def participants(id):
    bookings = Booking.query.filter_by(trek_id=id,status="Booked").all()
    users = []
    for booking in bookings:
        user = User.query.get(booking.user_id)
        users.append(user)
    return render_template("participants.html",users=users)  

@app.route('/update_trek/<int:id>', methods=['GET', 'POST'])
def update_trek(id):
    trek = Trek.query.get(id)
    if request.method == 'POST':
        trek.slots = request.form['slots']
        trek.status = request.form['status']
        db.session.commit()
        return redirect(f"/staff_page/{session['user_id']}")
    return render_template("update_trek.html",trek=trek) 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
if __name__ == '__main__': 
    app.run(debug=True)
 