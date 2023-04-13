import os
import json
import psycopg2
from psycopg2 import sql, extras
from flask import Flask, request, render_template
 
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/' to submit form"
    if request.method == 'POST':
        form_data = request.form
        
        ## Database Credentials

        pg_connection_dict = form_data
        
        
        return form_data

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
