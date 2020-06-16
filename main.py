import requests
from flask import Flask, request, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"] # this is our authorization

secrets = json.load(open(os.getcwd()+"\\secrets.json"))


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
    row_skeleton = ["BOT", '', data.get('Title'), '', data.get('Genre'), '', data.get('Runtime'), '', "low", "n/a"]
    print(row_skeleton)
    movielist.insert_row(row_skeleton, 2, value_input_option="USER_ENTERED")

"""
Flask Stuff goes below. 
"""
app = Flask(__name__)

@app.route('/') # default access
def home_page():
    return render_template("searchpage.html")

@app.route('/', methods=['POST'])
def search_movie():

    data = Search(request.form['movie'])
    if data.get('Response') == 'False':
        # If false we want to make sure it is communicated that there was some sort of error.
        return "Error occurred: movie does not exist in OMDB."

    Add(data)  # Start process of adding the movie to the database/spreadsheet

    return """<style>
            body {background-color: palevioletred;}
            h1   {color: blue;}
            p    {color: red;}
            
            .center {
              display: block;
              margin-left: auto;
              margin-right: auto;
              width: 25%;
            }
            
            </style>        """ + "<img src="+data['Poster']+" class=center><center><p style=\"font-family:Arial;font-size: 44px; \">Successfully added "+data['Title']+" to the movie list.</center>"


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



# We will want to insert an entire row at a time, in t:qhis schema:
# Suggester / Movie Title / Genre / Length / Priority / IMDB Link

#
# data = Search(movie_name)

if __name__ == "__main__":
    app.run(host=secrets["ip"], port="5010")


