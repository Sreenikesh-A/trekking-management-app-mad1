from flask import Flask,render_template, request
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return render_template("homepage.html")
    return render_template('loginp.html') 

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        name=request.form['name']
        mail=request.form['mail']
        password=request.form['password']
        role=request.form['role']
        return f"{name} registered successfully as {role}"

    return render_template('register.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/manage_trek')
def manage_trek():
    return render_template("manage_trek.html")
if __name__ == '__main__': 
    app.run(debug=True)
 