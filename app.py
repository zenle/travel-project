# flask_graphene_mongo/app.py
from database import init_db
from flask import Flask
from flask_graphql import GraphQLView
from schema import schema
from models import Department, Employee, Role, Flight
from flask import Flask, render_template
import requests
#from flask_cors import CORS


app = Flask(__name__)
#app.config['CORS_HEADERS'] = 'Content-Type'
#cors = CORS(app)


app.add_url_rule(
  '/graphql',
  view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)


@app.rout("/test")
def template_test():
  r = requests.post("https://9ffc5b68.ngrok.io/graphql?query={ allEmployees {edges { node{ name } } } }")
  l = r.text
  #print(l)
  return l
  
if __name__ == '__main__':
  init_db()
  app.run(debug=True, port=4000)
