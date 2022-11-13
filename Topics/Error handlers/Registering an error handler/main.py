from flask import Flask

app = Flask(__name__)

@app.errorhandler(403)
def you_shall_not_pass(e):  # error instance is automatically passed to the function
    return 'You shall not pass'

