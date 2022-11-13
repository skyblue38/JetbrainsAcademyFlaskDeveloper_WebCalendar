parser = RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('quantity', type=int)

@app.route('/')
def main_view():

    data = parser.parse_args()
    return {'data_from_url': data}