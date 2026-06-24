from flask import Flask,render_template, request
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return f"login for {username}"
    return render_template('loginp.html') 

if __name__ == '__main__':
    app.run(debug=True)
 