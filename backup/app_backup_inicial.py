from flask import Flask, render_template, request

app = Flask(__name__)


name = ""
email = ""
serie = ""


@app.route('/')
def index():

    return render_template('index.html')

@app.route('/resultado', methods=['POST'])
def resultado():

    global name
    global email
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        return "Form submitted successfully."+f"Name: {name}, Email: {email}"   
    

if __name__ == '__main__':
    app.run(debug=True)
