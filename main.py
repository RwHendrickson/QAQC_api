import os
import json
import psycopg2
from psycopg2 import sql, extras
from flask import Flask, request, render_template

# Initialize

# Interpolation Names

interp_names = ['PM2_5_Kriging', 'Temp_Kriging', 'Elevation_Kriging', 
                'PM2_5_Temp_Errors', 'Elevation_Errors']

# Functions

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

# The APP

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/' to submit form"
    if request.method == 'POST':
        
        form_data = request.form
        
        interp_name = form_data['rast']
        
        ## Database Credentials

        pg_connection_dict = {'dbname':form_data['dbname'],
                              'user':form_data['user'],
                              'password':form_data['password'],
                              'port':form_data['port'],
                              'host':form_data['host']}
        
        
        geojson = get_data(pg_connection_dict, interp_name)
        
        return geojson
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
