from flask import Flask, render_template

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html')
