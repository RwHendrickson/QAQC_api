import os
import json
import psycopg2
from psycopg2 import sql, extras
from flask import Flask, request


# Initialize

## interpolation names

interp_names = ['PM2_5_Kriging', 'Temp_Kriging', 'Elevation_Kriging', 
                'PM2_5_Temp_Errors', 'Elevation_Errors']

## Database Credentials

cred_pth = os.path.join(os.getcwd(),'db_credentials_template.txt')

with open(cred_pth, 'r') as f:
    
    creds = f.readlines()[0].rstrip('\n').split(', ')

pg_connection_dict = dict(zip(['dbname', 'user', 'password', 'port', 'host'], creds))
    
## Functions
# The endpoints (routes) all do the same thing, 
# just access different tables

endpoint_list = []

for i, interp_name in enumerate(interp_names): # Table Names

    ## Define the functions iteratively
    ## See here
    ## https://stackoverflow.com/questions/3431676/creating-functions-or-lambdas-in-a-loop-or-comprehension
    
    def f(interp_name=interp_name):
        
        conn = psycopg2.connect(**pg_connection_dict)

        # Create json cursor
        cur = conn.cursor(cursor_factory = extras.RealDictCursor)

        # Get the example as a Geojson
        cmd = f"""SELECT json_build_object(
    'type', 'FeatureCollection',
    'features', json_agg(ST_AsGeoJSON({interp_name}.*)::json)
    ) FROM {interp_name};"""

        cur.execute(cmd) # Execute

        conn.commit() # Committ command

        geojson = json.loads(json.dumps(cur.fetchall()))[0]["json_build_object"] # Unpack the response...
        
        ## ^ That's a dictionary

        # Close connection
        cur.close()
        conn.close()

        return geojson
        
    # Iteratively format endpoint dictionary 
    # Hack from:
    # Oooh, I lost the link...
    
    endpoint = {
                "route": "/"+interp_name,
                "view_func": f
                }
    
    endpoint_list.append(endpoint)    
    
    
### THE APP                

app = Flask(__name__)

## Index

@app.route("/")
def index():
    
    interp_string = '\n'.join(interp_names)
    
    return f'Please select your interpolation:\n\n{interp_string}\n\nAnd add one of these to the base url'    
    
# Create FLASK APPS from endpoints
# https://flask.palletsprojects.com/en/2.0.x/api/

for endpoint in endpoint_list:
    app.add_url_rule(endpoint['route'], view_func=endpoint['view_func'])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
