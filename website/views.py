from flask import Blueprint, render_template

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")

@views.route("/about")
def about():
    return render_template("about.html")


@views.route('/listings')
def listings():
    return render_template('listings.html')

@views.route('/listing')
def listing():
    return render_template('listing.html')