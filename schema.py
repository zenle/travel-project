import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import Department as DepartmentModel
from models import Employee as EmployeeModel
from models import Role as RoleModel
from models import Flight as FlightModel
from models import FlightList as FlightListModel
from scrap import scrap_flights
from database import save_flights



class Flight(MongoengineObjectType):

    class Meta:
        model = FlightModel
        interfaces = (Node,)


class FlightList(MongoengineObjectType):

    class Meta:
        model = FlightListModel
        interfaces = (Node,)


class Department(MongoengineObjectType):

    class Meta:
        model = DepartmentModel
        interfaces = (Node,)


class Role(MongoengineObjectType):

    class Meta:
        model = RoleModel
        interfaces = (Node,)


class Employee(MongoengineObjectType):

    class Meta:
        model = EmployeeModel
        filter_fields = ['name']
        interfaces = (Node,)


class SearchFlight(graphene.relay.ClientIDMutation):

    class Input:
        destination = graphene.String(required=True)
        departure_date = graphene.String(required=False)
        returning_date = graphene.String(required=False)

    flightList = graphene.Field(FlightList)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        destination = input.get('destination')
        departure_date = input.get('departure_date')
        returning_date = input.get('returning_date')

        flight_list = scrap_flights(destination, departure_date, returning_date)

        flights = []
        for s in flight_list:
        
            flight = FlightModel(
                            airline=s['airline'], 
                            duration=s['duration'],
                            price=s['price'],
                            airports=s['airports'],
                            stops=s['stops'],
                            layover=' '.join(s['layover']),
                            flight_time=s['flight_time']
                           )
            flight.save()
            flights.append(flight)

        flightList = FlightListModel(destination=destination, flights=flights)
        flightList.save()
        return SearchFlight(flightList=flightList)

        



class Query(graphene.ObjectType):
    node = Node.Field()
    all_employees = MongoengineConnectionField(Employee)
    all_role = MongoengineConnectionField(Role)
    all_flights = MongoengineConnectionField(Flight)
    role = graphene.Field(Role)
    employee = graphene.List(Employee)

    def resolve_employee(self, info, **args):
        return list(EmployeeModel.objects.all())


class Mutation(graphene.ObjectType):
    search_flight = SearchFlight.Field()


schema = graphene.Schema(query=Query, mutation=Mutation, types=[Department, Employee, Role, Flight, SearchFlight])
