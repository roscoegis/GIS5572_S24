import psycopg2
from flask import Flask
import json
import os

# Creates the Flask app that is noted in the Dockerfile
app = Flask(__name__) # setup initial flask app; gets called throughout in routes

 
 # Creates the index route  - main route when you go to the URL
@app.route('/') #python decorator
def index():
    return "The API works! "

# create the data route - where you get the GeoJSON data
@app.route('/exploretable1', methods=['GET'] )
def blegen():
    # create connection to the database
    conn = psycopg2.connect(
        host = os.environ.get("DB_HOST"),
        database = os.environ.get("DB_NAME"),
        user = os.environ.get("DB_USER"),
        password = os.environ.get("DB_PASS"),
        port = os.environ.get("DB_PORT"),
)
    

    # Execute a query to retrieve the polygon as GeoJSON

    with conn.cursor() as cur:
        query = """
        SELECT JSON_BUILD_OBJECT(
            'type', 'FeatureCollection',
            'features', JSON_AGG(
                ST_AsGEOJSON(exploretable1.*)::json
            )
        )
        FROM exploretable1;
        """


    cur.execute(query)
    data = cur.fetchall()   

    # Close the database connection

    conn.close()

# Return the data as GeoJSON
    return data[0][0]
   

# runs the app on the specified host and port
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

