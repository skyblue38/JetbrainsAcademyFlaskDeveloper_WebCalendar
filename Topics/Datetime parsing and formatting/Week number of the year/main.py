from datetime import datetime


def get_week_number(datetime_obj):
    return "Week number: {}.".format(datetime_obj.strftime("%U"))