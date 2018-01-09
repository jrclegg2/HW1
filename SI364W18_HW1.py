import requests
import json
## HW 1
## SI 364 W18
## 1000 points

#################################

## List below here, in a comment/comments, the people you worked with on this
## assignment AND any resources you used to find code (50 point deduction for
## not doing so). If none, write "None".

## NONE


## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the
## code so that once you run this application locally and go to the URL
## 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"

from flask import Flask, request
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_to_you():
    return 'Welcome to SI 364!'

## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL
## 'http://localhost:5000/movie/<name-of-movie-here-one-word>' you see a big
## dictionary of data on the page. For example, if you go to the URL
## 'http://localhost:5000/movie/ratatouille', you should see something like the
##  data shown in the included file sample_ratatouille_data.txt, which contains
## data about the animated movie Ratatouille. However, if you go to the url
## http://localhost:5000/movie/titanic, you should get different data, and if
## you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' for example,
## you should see data on the page that looks like this:

## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!

@app.route('/movie/<movieTitle>')
def movieRoute(movieTitle):
    requestURL = "https://itunes.apple.com/search"
    requestParams = {'term' : movieTitle, 'media' : 'movie'}
    requesting = requests.get(requestURL, params = requestParams).text.encode('utf-8')
    return requesting

## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application
## locally and got to the URL http://localhost:5000/question, you see a form
## that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web
##  page that says "Double your favorite number is <number>". For example, if
## you enter 2 into the form, you should then see a page that says "Double your
## favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.
@app.route('/question', methods = ['POST', 'GET'])
def questionRoute():
    s = """<!DOCTYPE html>
    <html>
    <body>
    <form method = "POST" action = "http://localhost:5000/question/double">
    Enter your favorite number:<br>
    <input type="text" name="number" value="1">
    <br>
    <input type="submit" value="Submit">
    </form>
    </body>
    """
    return s
@app.route('/question/double', methods = ['POST', 'GET'])
def questionDouble():
    if request.method == 'POST':
        numberFav = int(request.form['number'])
        doubleNum = numberFav * 2
        stringReturn = "Double your favorite number is {}.".format(doubleNum)
        return stringReturn

## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen
## dynamically in the Flask application, and build it into the above code for a
## Flask application, following a few requirements.
## You should create a form that appears at the route: http://localhost:5000/problem4form
## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends
# upon the data entered into the submission form and is readable by humans
# (more readable than e.g. the data you got in Problem 2 of this HW). The new
# data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think
# going slowly and carefully writing out steps for a simpler data transaction,
# like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect
# in your form; you do not need to handle errors or user confusion.
# (e.g. if your form asks for a name, you can assume a user will type a reasonable
#  name; if your form asks for a number, you can assume a user will type a reasonable
# number; if your form asks the user to select a checkbox, you can assume they will do that.)
@app.route('/problem4form', methods = ['POST', 'GET'])
def problemForm():
    darkskykey = '94e0fbc1b9dff53bfe21e0833af05685'
    if request.method == 'POST':
        lat = request.form['lat']
        long = request.form['long']
        data = request.form['data']
        darksky_URL = 'https://api.darksky.net/forecast/{}/{},{}'.format(darkskykey, lat, long)
        requesting_darksky = requests.get(darksky_URL).text.encode('utf-8')
        jsonWeather = json.loads(requesting_darksky)
        if data == 'current':
            temp = jsonWeather['currently']['temperature']
            return "The current temperature right now at your latitude and longitude is {}!".format(temp)
        if data == 'highlow':
            high = jsonWeather['daily']['data'][0]['temperatureHigh']
            low = jsonWeather['daily']['data'][0]['temperatureLow']
            return "The low temperature today will be {}, and the high will be {}.".format(low, high)
    s = """<!DOCTYPE html>
    <html>
    <body>
    <form method = "POST" action = "http://localhost:5000/problem4form">
    Enter a latitude:<br>
    <input type="text" name="lat" value="42.271039">
    <br>
    Enter a longitude:<br>
    <input type="text" name="long" value="-83.743722">
    <br>
    What would you like to see?<br>
    <input type="radio" name="data" value="current" checked> Current temperature <br>
    <input type="radio" name="data" value="highlow"> High/Low Temp for today <br>
    <br>
    <input type="submit" value="Submit">
    </form>
    </body>
    """
    return s


# Points will be assigned for each specification in the problem.
if __name__ == '__main__':
    app.run()
