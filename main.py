from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import os

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

# Extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Models
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

# Schemas
class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book

class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member

book_schema = BookSchema()
books_schema = BookSchema(many=True)
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

# Routes
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return book_schema.jsonify(new_book), 201

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return book_schema.jsonify(book)

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return books_schema.jsonify(books)

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    db.session.commit()
    return book_schema.jsonify(book)

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return '', 204

@app.route('/members', methods=['POST'])
def create_member():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_member = Member(name=data['name'], email=data['email'], password=hashed_password)
    db.session.add(new_member)
    db.session.commit()
    return member_schema.jsonify(new_member), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    member = Member.query.filter_by(email=data['email']).first()
    if member and bcrypt.check_password_hash(member.password, data['password']):
        token = create_access_token(identity=member.email)
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/members', methods=['GET'])
@jwt_required()
def get_members():
    members = Member.query.all()
    return members_schema.jsonify(members)

if __name__ == '__main__':
    if not os.path.exists('library.db'):
        db.create_all()
    app.run(debug=True)
