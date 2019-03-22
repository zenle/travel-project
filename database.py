# flask_graphene_mongo/database.py
from mongoengine import connect

from models import Flight, Employee, Role, Department
from scrap import scrap_flights
import json
import pprint

# You can connect to a real mongo server instance by your own.
connect('graphene-mongo-example', host='mongodb://sen:senvanle4@ds149732.mlab.com:49732/collections', alias='default')


def save_flights(flight_list):

    flights = []
    for s in flight_list:
        pprint.pprint(s)
        flight = Flight(
                        airline=s['airline'], 
                        duration=s['duration'],
                        price=s['price'],
                        airports=s['airports'],
                        stops=s['stops'],
                        layover=' '.join(s['layover']),
                        flight_time=s['flight_time']
                       )
        flight.save
        flights.append(flight)
    
    return flights





def init_db():
    # Create the fixtures
    engineering = Department(name='Engineering')
    engineering.save()

    hr = Department(name='Human Resources')
    hr.save()

    manager = Role(name='manager')
    manager.save()

    engineer = Role(name='engineer')
    engineer.save()

    peter = Employee(name='Peter', department=engineering, role=engineer)
    peter.save()

    roy = Employee(name='Roy', department=engineering, role=engineer)
    roy.save()

    tracy = Employee(name='Tracy', department=hr, role=manager)
    tracy.save()
    '''
    
    '''
    

