import os
import json
import psycopg2
from psycopg2 import sql, extras
from flask import Flask, request


# Initialize

## interpolation names

interp_names = ['PM2_5_Kriging', 'Temp_Kriging', 'elev_kriging', 
                'PM2_5_Kriging_Errors', 'Temp_Kriging_Errors', 'elev_kriging_errors']

## Database Credentials

cred_pth = os.path.join(os.getcwd(),'db_credentials_template.txt')

with open(cred_pth, 'r') as f:
    
    creds = f.readlines()[0].rstrip('\n').split(', ')

pg_connection_dict = dict(zip(['dbname', 'user', 'password', 'port', 'host'], creds))
    
## Functions
# The endpoints (routes) all do the same thing, 
# just access different tables

def get_data(pg_connection_dict, interp_name):

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
    
### THE APP                

app = Flask(__name__)

## Index

@app.route("/")
def index():
    
    interp_string = '\n'.join(interp_names)
    
    return f'Please select your interpolation:\n\n{interp_string}\n\nAnd add one of these to the base url'    
    
@app.route("/<page>")
def data(page):
    if page in interp_names:
        response = get_data(pg_connection_dict, page)
        return response
        
    else:
    
        return 'ERROR. No Dataset Matches your request'

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
