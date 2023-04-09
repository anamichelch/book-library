from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
all_books = []

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


# create a new book object and add it to the session
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    books = Book.query.all()
    return render_template('index.html', all_books=books)


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/submit_book', methods=['POST'])
def submit_book():
    if request.method == "POST":
        # get the form data from the request object
        title = request.form["title"]
        author = request.form["author"]
        rating = request.form["rating"]

        #add to db
        new_book = Book(title=title, author=author,rating=rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template(url_for('add.html'))










if __name__ == "__main__":
    app.run(debug=True)
