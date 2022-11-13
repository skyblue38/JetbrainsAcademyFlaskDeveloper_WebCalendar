from flask import Flask, abort

app = Flask(__name__)

@app.route("/capital/<country>")
def capital(country):
    capitals_dictionary = {
        "Russia":"Moscow",
        "Ukraine":"Kiev",
        "USA":"Washington"
    }
    if country in capitals_dictionary:
        return capitals_dictionary[country]
    return abort(404, 'Resource not found')
