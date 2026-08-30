# app.py 
# imports
from flask import Flask, g, render_template
import sqlite3

# constants
DATABASE = 'databace.db'

# program
app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def home():
    #home page- just the ID, Maker, Model and Image URL
    sql = """
    SELECT Cars.CarID, Makers.Name AS Maker, Cars.Model, Cars.ImageURL 
    FROM Cars
    JOIN Makers ON Makers.MakerID = Cars.MakerID;
    """
    results = query_db(sql)
    return render_template('home.html', title='Home', cars=results)


@app.route("/cars")
def cars():
    #cars page- just the ID, Maker, Model and Image URL
    sql = """
    SELECT Cars.CarID, Makers.Name AS Maker, Cars.Model, Cars.ImageURL 
    FROM Cars
    JOIN Makers ON Makers.MakerID = Cars.MakerID;
    """
    results = query_db(sql)
    return render_template('cars.html', title='Cars', cars=results)


@app.route("/cars/<int:id>")
def car(id):
    # just one car based on the id
    sql = """
    SELECT Cars.CarID, Makers.Name AS Maker, Cars.Model, Cars.ImageURL, Cars.Description, Cars.Year, Cars.Cost, Cars.ImageBeforeURL, Cars.ImageAfterURL
    FROM Cars
    JOIN Makers ON Makers.MakerID = Cars.MakerID 
    WHERE Cars.CarID = ?;
    """
    result = query_db(sql, (id,), True)
    return render_template('car.html', title='Car Details', car=result)

@app.route("/tracks")
def tracks():
    #tracks page- just the ID, Maker, Model and Image URL
    sql = """
SELECT Tracks.Trackid, name, location, imageURL, videoURL 
FROM Tracks;
    """
    results = query_db(sql)
    return render_template('tracks.html', title='Tracks', tracks=results)



if __name__ == "__main__":
    app.run(debug=True, port=5050)

