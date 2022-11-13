# based on Flask-SQLAlchemy Quickstart - https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/

from flask import Flask, abort
from flask_restful import Resource, Api, reqparse, inputs, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy
import sys
import datetime

db = SQLAlchemy()               # create sqlalchemy database object for Flask
app = Flask(__name__)           # create Flask object
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webcal.db'  # database filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)                # initialise app with extensions


class Webcal(db.Model):         # define database structure with webcal table
    __tablename__ = 'webcal'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)


resource_fields = {
    'id': fields.Integer,
    'event': fields.String,
    'date': fields.DateTime(dt_format='iso8601'),
    }

api = Api(app)                  # create api object for Flask
post_parser = reqparse.RequestParser()  # define how to parse web POST request arguments
post_parser.add_argument('event',
                         type=str,
                         help="The event name is required!",
                         required=True)
post_parser.add_argument('date',
                         type=inputs.date,
                         help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
                         required=True)

parser = reqparse.RequestParser()  # define how to parse web GET request arguments
parser.add_argument('event', type=str, required=False)
parser.add_argument('date', type=inputs.date, required=False)
parser.add_argument('start_time', type=inputs.date, required=False)
parser.add_argument('end_time', type=inputs.date, required=False)


# define web resources and their methods
class WebcalEvent(Resource):
    def post(self):                     # add event to SQL
        args = post_parser.parse_args()  # get data from POST request and Build webcal entry
        webcal_entry = Webcal(event=args['event'], date=args['date'])
        db.session.add(webcal_entry)    # write to SQL
        db.session.commit()
        return {
            "message": "The event has been added!",
            "event": args["event"],
            "date": str(args["date"]).split()[0]
            }

    @marshal_with(resource_fields)
    def get(self, **kwargs):
        args = parser.parse_args()
        if args['start_time'] is not None:
            if args['end_time'] is not None:    # query range
                event_list = Webcal.query.filter(db.and_(Webcal.date >= args['start_time'],
                                                         Webcal.date <= args['end_time'])).all()
                if not event_list:
                    abort(404, message='No events in range!')
                else:
                    e_list = [{'id': e.id, 'event': e.event, 'date': e.date} for e in event_list]
                    return e_list
        event_list = Webcal.query.all()         # get a list of all events from SQL
        e_list = [{'id': e.id, 'event': e.event, 'date': e.date} for e in event_list]
        return e_list


class WebcalToday(Resource):
    @marshal_with(resource_fields)
    def get(self):          # query events with today's date
        # args = parser.parse_args()
        events_today = Webcal.query.filter(Webcal.date == datetime.date.today()).all()
        if events_today is None:
            return {'message': 'No events for today...'}
        else:
            e_list = [{'id': e.id, 'event': e.event, 'date': e.date} for e in events_today]
            return e_list


class EventByID(Resource):
    # @marshal_with(resource_fields)
    def get(self, event_id):
        # args = parser.parse_args()
        eid = Webcal.query.filter(Webcal.id == event_id).all()
        if eid == []:
            return {"message": "The event doesn't exist!"}, 404
        rd = {'id': eid[0].id, 'event': eid[0].event, 'date': eid[0].date.strftime('%Y-%m-%d')}
        return rd, 200

    # @marshal_with(resource_fields)
    def delete(self, event_id):
        # args = parser.parse_args()
        eid = Webcal.query.get(event_id)
        try:
            db.session.delete(eid)
            db.session.commit()
        except Exception:
            return {'message': "The event doesn't exist!"}, 404
        return {'message': 'The event has been deleted!'}, 200


with app.app_context():
    db.create_all()                 # create database and tables

# map API resources to web URI
api.add_resource(WebcalEvent, '/event')
api.add_resource(WebcalToday, '/event/today')
api.add_resource(EventByID, '/event/<int:event_id>')

# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
