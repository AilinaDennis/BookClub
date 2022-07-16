from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Book:
    db_name = 'users_books'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.description = db_data['description']
        self.date = db_data['date']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.users_who_favorited = []
        self.users_who_unfavorited = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO books (title, description, date, user_id, created_at) VALUES (%(title)s,%(description)s,%(date)s,%(user_id)s, NOW());"
        # query = "INSERT INTO favorites (book_id, user_id, created_at, updated_at) VALUES (%(book_id)s,%(user_id)s, NOW(), NOW());"
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM books WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL(cls.db_name).query_db(query)
        books = []
        for row in results: 
            books.append(cls(row))
        return books

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM books LEFT JOIN favorites ON books.id = favorites.book_id LEFT JOIN users ON users.id = favorites.user_id WHERE books.id = %(id)s;"
        results = connectToMySQL('users_books').query_db(query,data)

        book = cls(results[0])

        for row in results:
            if row['users.id'] == None:
                break
            data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": None,
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            book.users_who_favorited.append(user.User(data))
            book.users_who_unfavorited.append(user.User(data))
        return book    

    @classmethod
    def update(cls, data):
        query = "UPDATE books SET title=%(title)s, description=%(description)s, date=%(date)s, WHERE id = %(id)s, created_at;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM books WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)


    @staticmethod
    def validate_book(book):
        is_valid = True
        if len(book['title']) < 3:
            is_valid = False
            flash("Title must be at least 3 characters","book")
        if len(book['description']) < 3:
            is_valid = False
            flash("Description must be at least 5 characters","book")
        if book['date'] == "":
            is_valid = False
            flash("Please enter a date","book")
        return is_valid