from flask import Flask

app = Flask('main')


@app.route('/storage/images/<filename>')
def main_view(filename):
    return filename
