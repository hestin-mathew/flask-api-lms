from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    isbn TEXT NOT NULL,
                    publication_year INTEGER,
                    status TEXT DEFAULT 'Available'
                )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    membership_id TEXT NOT NULL UNIQUE,
                    contact_info TEXT
                )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS rentals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    member_id INTEGER NOT NULL,
                    FOREIGN KEY (book_id) REFERENCES books (id),
                    FOREIGN KEY (member_id) REFERENCES members (id)
                )''')
    conn.commit()
    conn.close()

init_db()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def books():
    return render_template('books.html')

@app.route('/members')
def members():
    return render_template('members.html')

# Books CRUD operations

@app.route('/api/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    books_list = [dict(book) for book in books]
    conn.close()
    return jsonify(books_list)

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    conn.close()
    if book:
        return jsonify(dict(book))
    else:
        return jsonify({'error': 'Book not found'}), 404

@app.route('/api/books', methods=['POST'])
def create_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    publication_year = data.get('publication_year')
    if not title or not author or not isbn:
        return jsonify({'error': 'Missing required fields'}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, isbn, publication_year) VALUES (?, ?, ?, ?)",
                   (title, author, isbn, publication_year))
    conn.commit()
    book_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': book_id}), 201

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    publication_year = data.get('publication_year')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title = ?, author = ?, isbn = ?, publication_year = ? WHERE id = ?",
                   (title, author, isbn, publication_year, book_id))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({'error': 'Book not found'}), 404
    else:
        return jsonify({'message': 'Book updated successfully'})

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({'error': 'Book not found'}), 404
    else:
        return jsonify({'message': 'Book deleted successfully'})

# Rent and Return Book

@app.route('/api/books/<int:book_id>/rent', methods=['POST'])
def rent_book(book_id):
    data = request.get_json()
    member_id = data.get('member_id')
    if not member_id:
        return jsonify({'error': 'Member ID is required'}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ? AND status = 'Available'", (book_id,))
    book = cursor.fetchone()
    if not book:
        return jsonify({'error': 'Book not available'}), 404
    cursor.execute("INSERT INTO rentals (book_id, member_id) VALUES (?, ?)", (book_id, member_id))
    cursor.execute("UPDATE books SET status = 'Rented' WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Book rented successfully'})

@app.route('/api/books/<int:book_id>/return', methods=['POST'])
def return_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ? AND status = 'Rented'", (book_id,))
    book = cursor.fetchone()
    if not book:
        return jsonify({'error': 'Book not rented'}), 404
    cursor.execute("DELETE FROM rentals WHERE book_id = ?", (book_id,))
    cursor.execute("UPDATE books SET status = 'Available' WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Book returned successfully'})

# Members CRUD operations

@app.route('/api/members', methods=['GET'])
def get_members():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    members_list = [dict(member) for member in members]
    conn.close()
    return jsonify(members_list)

@app.route('/api/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
    member = cursor.fetchone()
    conn.close()
    if member:
        return jsonify(dict(member))
    else:
        return jsonify({'error': 'Member not found'}), 404

@app.route('/api/members', methods=['POST'])
def create_member():
    data = request.get_json()
    name = data.get('name')
    membership_id = data.get('membership_id')
    contact_info = data.get('contact_info')
    if not name or not membership_id:
        return jsonify({'error': 'Missing required fields'}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO members (name, membership_id, contact_info) VALUES (?, ?, ?)",
                       (name, membership_id, contact_info))
        conn.commit()
        member_id = cursor.lastrowid
        conn.close()
        return jsonify({'id': member_id}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Membership ID already exists'}), 400

@app.route('/api/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    data = request.get_json()
    name = data.get('name')
    membership_id = data.get('membership_id')
    contact_info = data.get('contact_info')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE members SET name = ?, membership_id = ?, contact_info = ? WHERE id = ?",
                   (name, membership_id, contact_info, member_id))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({'error': 'Member not found'}), 404
    else:
        return jsonify({'message': 'Member updated successfully'})

@app.route('/api/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({'error': 'Member not found'}), 404
    else:
        return jsonify({'message': 'Member deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)