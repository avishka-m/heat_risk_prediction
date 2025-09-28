from flask import Flask , render_template, request

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('patient_details.html')

@app.route('/getresults', methods=['post'])
def getresults():
    result = request.form
    print(result)
    return('results printed')


app.run(debug=True)