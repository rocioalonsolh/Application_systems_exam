# Import necessary modules from Flask and SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Create a Flask web application
app = Flask(__name__)

# Configure the Flask application to use an SQLite database named 'books.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
# Disable Flask-SQLAlchemy modification tracking feature for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a SQLAlchemy database instance with the configured Flask application
db = SQLAlchemy(app)

# Define the Book model with id, title, author, and publication_year columns
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

# Create the database and tables based on the defined models
with app.app_context():
    db.create_all()

# Route to display the list of books
@app.route('/books')
def books():
    # Query all books from the database
    books_list = Book.query.all()
    # Render the 'books.html' template with the list of books
    return render_template('books.html', books=books_list)

# Route to add a new book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    # Check if the form is submitted with a POST request
    if request.method == 'POST':
        # Extract book information from the form data
        title = request.form['title']
        author = request.form['author']
        publication_year = int(request.form['publication_year'])

        # Create a new Book instance with the extracted information
        new_book = Book(title=title, author=author, publication_year=publication_year)
        # Add the new book to the database session
        db.session.add(new_book)
        # Commit the changes to the database
        db.session.commit()

        # Redirect to the 'books' route to display the updated list of books
        return redirect(url_for('books'))

    # If the request method is GET, render the 'add_book.html' template
    return render_template('add_book.html')

# Run the Flask application on port 5003 in debug mode
if __name__ == '__main__':
    app.run(port=5003, debug=True)
