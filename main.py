import json  # Importing the json module for handling JSON data
import random  # Importing the random module for generating random short URLs
import string  # Importing the string module for working with strings
from flask import Flask, render_template, redirect, request  # Importing necessary functions and classes from Flask


app = Flask(__name__)


# Function to load shortened URLs from a JSON file
def load_shortened_urls():
    try:
        with open("short_urls.json", "r") as file:  # Open the JSON file in read mode
            return json.load(file)  # Load JSON data from the file and return it
    except FileNotFoundError:  
        return {}  # Return an empty dictionary if the file doesn't exist


# Function to save shortened URLs to a JSON file
def save_shortened_urls(url):
    with open("short_urls.json", "w") as file:  # Open the JSON file in write mode
        json.dump(url, file)  # Write the JSON data to the file


# Function to generate a random short URL
def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits  # Define characters for short URL
    short_url = "".join(random.choice(characters) for _ in range(length))  # Generate a random short URL
    return short_url


# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        original_url = request.form['original_url']
        short_url = generate_short_url()  # Generate a short URL
        while short_url in shortened_urls:  # Check if short URL is unique
            short_url = generate_short_url()

        shortened_urls[short_url] = original_url  # Store the shortened URL in the dictionary
        save_shortened_urls(shortened_urls)  # Save the updated URLs to the JSON file
        return render_template("index.html", shortened_url=f"{request.url_root}{short_url}")  # Render the template with the shortened URL
    return render_template("index.html")  # Render the template with the form


@app.route("/<short_url>")
def redirect_to_original_url(short_url):
    original_url = shortened_urls.get(short_url)  # Get the original URL
    if original_url:  # If URL exists, redirect user
        return redirect(original_url)
    else:  # If URL does not exist, return error message
        return "URL not found", 404


# Load existing shortened URLs on startup
shortened_urls = load_shortened_urls()


if __name__ == "__main__":
    app.run(debug=True)  # Run the Flask application in debug mode