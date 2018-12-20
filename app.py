from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create the application instance
app = Flask(__name__)

# Use PyMongo to establish Mongo Connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create a URL route in the application for "/"
@app.route("/")
def home():
    # Find record from the mongo db
    mars_data = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html", mars_data = mars_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scraper():
    # Run the scrape function
    mars_data = mongo.db.mars_data
    mars_data_data = scrape_mars.scrape()

    #Update the Mongo database using update and insert=True)
    mars_data.update({},mars_data_data,upsert=True)

    #Redirect back to the home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)