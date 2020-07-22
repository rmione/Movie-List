import requests
from flask import Flask, request, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
import random
from dotenv import load_dotenv

load_dotenv()
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"] # this is our authorization

API_DATA = os.getenv('API_DATA')
IP = os.getenv('IP')

credentials = ServiceAccountCredentials.from_json_keyfile_name(secrets["api_data"], scope)
client  = gspread.authorize(credentials)
movielist = client.open("The Movie List").sheet1



def Search(movie_name):
    """
    Function searches OMDB for the query given in input.
    Some basic error handling will be in order
    :param movie_name:
    :return:
    """
    response = requests.get(url + "t=" + movie_name)

    print(response.json())

    return response.json()
def Add(data):
    """
    This function assumes that the response was True.
    :param data:
    :return:
    """

    movielist.insert_row(["BOT", '', data.get('Title'), '', data.get('Genre'), '', data.get('Runtime'), '', "low", "n/a"], 2, value_input_option="USER_ENTERED")

"""
Flask Stuff goes below. 
"""
app = Flask(__name__)


def Pick():
    names = movielist.col_values(3)
    names.pop(0)

    # TODO: this is honestly a hack... can probably find a way to deal w this upfront
    return random.choice(names)

@app.route('/random')
def random_movie():
    """
    Uses the Pick() function to pick the movie itself.
    Then the movie is searched for (for redundancy's sake. This is sort of unnecessary otherwise!)
    And if a good response comes back, it will render the random movie page! 
    
    """
    
    selection = Pick()
    data = Search(selection)
    if data.get('Response') == 'False':
        # If false we want to make sure it is communicated that there was some sort of error.
        return "Error occurred: movie does not exist in OMDB."

    return render_template("random.html", movie_name=data.get('Title'), movie_poster=data.get('Poster'))
    

@app.route('/') # Homepage
def home_page():

    return render_template("homepage.html")

@app.route('/', methods=['POST'])
def search_movie():

    data = Search(request.form['movie'])
    if data.get('Response') == 'False':
        # If false we want to make sure it is communicated that there was some sort of error.
        return "Error occurred: movie does not exist in OMDB."

    Add(data)  # Start process of adding the movie to the database/spreadsheet
    return render_template("search.html", movie_name=data.get('Title'), movie_poster=data.get('Poster'))

    



"""
Here I define OMDB api stuff. Unique API key (mine) will be removed when this goes public
"""

KEY = "49378cfc"
url = "http://www.omdbapi.com/?apikey="+KEY+"&"

"""
This part will be re-allocated to the Flask app - 
I want a search bar to be used, and you input it. Clean web interface.
"""
# print("enter the name of the movie you're looking for: \n") #  really simple shit for now... this works fine for testing
# movie_name = str(input())



# We will want to insert an entire row at a time, in this schema:
# Suggester / Movie Title / Genre / Length / Priority / IMDB Link

#
# data = Search(movie_name)

if __name__ == "__main__":
    app.run(host="localhost", port="5010")


