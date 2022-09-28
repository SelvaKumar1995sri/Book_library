import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy



project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookdatabase2.db"

db = SQLAlchemy(app)

class Book(db.Model):   
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)


@app.route('/create')
def index():
     db.create_all()
     return "Created"

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method.upper() == "GET":
         books = Book.query.all()
         return render_template("home.html", books=books)
    else:
        if request.form:
            try:
            
                book = Book(title=request.form.get("title"))
                db.session.add(book)
                db.session.commit()
            except Exception as e:
                print("Failed to add book", str(e))
        books = Book.query.all()
        return render_template("home.html", books=books)

@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        book = Book.query.filter_by(title=oldtitle).first()
        book.title = newtitle
        db.session.commit()
    except Exception as e:
        print("Couldn't update book title", str(e))
       
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    try:
        title = request.form.get("title")
        book = Book.query.filter_by(title=title).first()
        db.session.delete(book)
        db.session.commit()
    except Exception as e:
        print("Couldn't delete book title", str(e))
    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)