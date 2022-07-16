from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.book import Book
from flask_app.models.user import User


@app.route('/new/book')
def new_book():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_book.html',user=User.get_by_id(data))


@app.route('/create/book',methods=['POST'])
def create_book():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Book.validate_book(request.form):
        return redirect('/new/book')
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "date": request.form["date"],
        "user_id": session["user_id"]
    }
    book_id=Book.save(data)
    favorite_data={
        'user_id':session['user_id'],
        'book_id':book_id
    }
    User.add_favorite(favorite_data)
    return redirect('/dashboard')

@app.route('/edit/book/<int:id>')
def edit_book(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_book.html",edit=Book.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/book/<int:id>', methods = ['POST'])
def update_book(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Book.validate_book(request.form):
        return redirect(f'/edit/book/{id}')
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "date": request.form["date"],
        "id": id
    }
    Book.update(data)
    return redirect('/dashboard')

@app.route('/book/<int:id>')
def show_book(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_book.html",book=Book.get_by_id(data),user=User.get_by_id(user_data), favorited_users=User.favorited_users(data))

@app.route('/join/user',methods=['POST'])
def join_user():
    data = {
        'user_id': session['user_id'],
        'book_id': request.form['book_id']
    }
    User.add_favorite(data)
    return redirect(f"/book/{request.form['book_id']}")

# @app.route('/delete/user',methods=['POST'])
# def delete_user():
#     data = {
#         'user_id': session['user_id'],
#         'book_id': request.form['book_id']
#     }
#     User.delete_favorite(data)
#     return redirect(f"/book/{request.form['book_id']}")

@app.route('/destroy/book/<int:id>')
def destroy_book(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Book.destroy(data)
    return redirect('/dashboard')

@app.route('/unfavorite/<int:id>', methods=['POST']) 
def unfavorite(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    User.unfavorite(data)
    return redirect(f'/book/{id}')