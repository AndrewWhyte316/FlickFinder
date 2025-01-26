FlickFinder

FlickFinder is a web application designed to help users discover movies, view recommendations, and manage their profiles. Users can sign up, log in, and access features like personalized recommendations, movie showtimes, and profile management.

Features

User Authentication

Sign Up: Users can create an account with a unique username and email.

Log In: Registered users can log in using their credentials.

Log Out: Users can securely log out of their account.

Profile Management

Users can update their personal information, including location and password.

Passwords are securely hashed using bcrypt before being stored in the database.

Movie Recommendations

A dedicated page for movie recommendations based on genres.

Showtimes

Users can view movie showtimes and related details.

Dynamic Navigation Bar

Shows "Sign In" and "Sign Up" when the user is logged out.

Displays "Profile" and "Sign Out" when the user is logged in.

Footer

Includes links to "About Us," "Contact Us," and "Privacy Policy."

Project Structure

FlickFinder/
├── static/
│   ├── styles/
│   │   └── mainstyle2.css
│   └── images/
├── templates/
│   ├── base.html
│   ├── navbar.html
│   ├── footer.html
│   ├── login.html
│   ├── signup.html
│   ├── about_us.html
│   ├── film_showings.html
│   └── recommendations.html
├── flaskmain.py
├── init_db.py
├── requirements.txt
└── README.md

Key Files

flaskmain.py

Main application file containing Flask routes and logic.

init_db.py

Script to initialize the SQLite database with the required tables.

Templates

base.html: The base layout used across all pages.

navbar.html: Contains the navigation bar.

footer.html: Contains the footer.

login.html, signup.html: Pages for user authentication.

about_us.html, film_showings.html, recommendations.html: Functional pages for the app.

Static Files

mainstyle2.css: Stylesheet for custom styling.

Images and other static assets.

Installation

Prerequisites

Python 3.10+

Flask

SQLite3

Bootstrap (via CDN for styling)

Steps

Clone the repository:

git clone https://github.com/yourusername/FlickFinder.git
cd FlickFinder

Set up a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Initialize the database:

python init_db.py

Run the application:

flask run

Open the application in your browser:

Navigate to http://127.0.0.1:5000/

Usage

Sign Up

Create a new account on the Sign Up page.

Log In

Access your account using your credentials.

Profile Management

Update your location or password on the Profile page.

Explore Recommendations

View movie recommendations tailored to genres.

Showtimes

Browse available movie showtimes.

Log Out

Securely log out when finished.

Database Schema

Users Table

Column

Type

Description

id

INTEGER

Primary key

name

TEXT

User's full name

email

TEXT

User's unique email

username

TEXT

Unique username

password

TEXT

Hashed password

location

TEXT

User's location (optional)

Genres Table (Example)

Column

Type

Description

id

INTEGER

Primary key

name

TEXT

Name of the genre

Movies Table (Example)

Column

Type

Description

id

INTEGER

Primary key

title

TEXT

Title of the movie

genre_id

INTEGER

Foreign key to genres

Future Enhancements

Advanced Recommendations: Use machine learning to recommend movies based on user preferences.

Search Functionality: Add a search bar for movies and genres.

User Reviews: Allow users to leave reviews and ratings for movies.

Responsive Design: Optimize the UI for mobile and tablet devices.