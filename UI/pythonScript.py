from flask import Flask, jsonify, render_template, request
app = Flask(__name__)

@app.route('/pythonScript')
def mainJs():
    print("read from js: ")
    type = request.args.get('type')
    dataOne = request.args.get('dataOne')
    dataTwo = request.args.get('dataTwo')
    print(type)
    print(dataOne)
    print(dataTwo)
    return jsonify("done")

@app.route('/')
def index():
    return render_template('/index.html')

if __name__ == "__main__":
    app.run(debug=True)
