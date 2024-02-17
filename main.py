import psycopg2
from flask import Flask, jsonify
import json

app = Flask(__name__) # setup initial flask app; gets called throughout in routes

# Connect to the PostgreSQL database

pgSQL_connect = {
    'dbname':"gis5572",
    'user':"postgres",
    'password':"postgres",
    'host':"35.224.112.3",
    'port':"5000"
}


@app.route('/') #python decorator 
def hello_world(): #function that app.route decorator references
  response = hello()
  return response

def hello():
  return "GIS 5572 Lab 1"

# Route to retrieve polygon as GeoJSON
@app.route('/getgeojson', methods=['GET'])
def get_geojson():
    try:
        # Connect to the database
        connection = psycopg2.connect(**pgSQL_connect)
        cursor = connection.cursor()

        # Query to retrieve polygon as GeoJSON
        query = "SELECT ST_AsGeoJSON(geom) FROM polygon_lab1;"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Close database connection
        cursor.close()
        connection.close()

        # Prepare GeoJSON response
        features = []
        for row in rows:
            feature = {
                "type": "Feature",
                "geometry": json.loads(row[0]),
                "properties": {}
            }
            features.append(feature)

        feature_collection = {
            "type": "FeatureCollection",
            "features": features
        }

        # Return GeoJSON response
        return jsonify(feature_collection)

    except psycopg2.Error as e:
        return jsonify({"error": "Database error: " + str(e)}), 500

if __name__ == "__main__":
    app.run(
      #debug=True, #shows errors 
      host='0.0.0.0', #tells app to run exposed to outside world
      port=5000)
