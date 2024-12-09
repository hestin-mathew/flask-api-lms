import unittest
import app
import json

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        app.app.config['TESTING'] = True
        app.init_db()

    def test_update_book(self):
        # Create a book
        create_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890',
            'publication_year': 2023
        }
        create_response = self.app.post('/books', json=create_data)
        self.assertEqual(create_response.status_code, 201)
        book_id = create_response.json['id']

        # Update the book
        update_data = {
            'title': 'Updated Test Book',
            'author': 'Updated Test Author',
            'isbn': '0987654321',
            'publication_year': 2022
        }
        response = self.app.put(f'/books/{book_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Book updated successfully')

        # Retrieve the book to check updates
        get_response = self.app.get(f'/books/{book_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json['title'], 'Updated Test Book')
        self.assertEqual(get_response.json['author'], 'Updated Test Author')
        self.assertEqual(get_response.json['isbn'], '0987654321')
        self.assertEqual(get_response.json['publication_year'], 2022)

    def test_update_member(self):
        # Create a member
        create_data = {
            'name': 'Test Member',
            'membership_id': 'TEST123',
            'contact_info': 'test@example.com'
        }
        create_response = self.app.post('/members', json=create_data)
        self.assertEqual(create_response.status_code, 201)
        member_id = create_response.json['id']

        # Update the member
        update_data = {
            'name': 'Updated Test Member',
            'membership_id': 'TEST456',
            'contact_info': 'updated_test@example.com'
        }
        response = self.app.put(f'/members/{member_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Member updated successfully')

        # Retrieve the member to check updates
        get_response = self.app.get(f'/members/{member_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json['name'], 'Updated Test Member')
        self.assertEqual(get_response.json['membership_id'], 'TEST456')
        self.assertEqual(get_response.json['contact_info'], 'updated_test@example.com')

    def test_search_books(self):
        # Create a few books
        book1_data = {
            'title': 'Book One',
            'author': 'Author A',
            'isbn': '1111111111',
            'publication_year': 2020
        }
        self.app.post('/books', json=book1_data)

        book2_data = {
            'title': 'Book Two',
            'author': 'Author B',
            'isbn': '2222222222',
            'publication_year': 2021
        }
        self.app.post('/books', json=book2_data)

        # Search for books by title
        response = self.app.get('/books?title=One')
        self.assertEqual(response.status_code, 200)
        books = response.json
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]['title'], 'Book One')

        # Search for books by author
        response = self.app.get('/books?author=Author B')
        self.assertEqual(response.status_code, 200)
        books = response.json
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]['author'], 'Author B')

    def test_pagination_books(self):
        # Create multiple books
        for i in range(1, 6):
            data = {
                'title': f'Book {i}',
                'author': f'Author {i}',
                'isbn': f'123456789{i}',
                'publication_year': 2020 + i
            }
            self.app.post('/books', json=data)

        # Get page 1 with per_page=2
        response = self.app.get('/books?page=1&per_page=2')
        self.assertEqual(response.status_code, 200)
        books = response.json
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0]['title'], 'Book 1')
        self.assertEqual(books[1]['title'], 'Book 2')

        # Get page 2 with per_page=2
        response = self.app.get('/books?page=2&per_page=2')
        self.assertEqual(response.status_code, 200)
        books = response.json
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0]['title'], 'Book 3')
        self.assertEqual(books[1]['title'], 'Book 4')

        # Get page 3 with per_page=2
        response = self.app.get('/books?page=3&per_page=2')
        self.assertEqual(response.status_code, 200)
        books = response.json
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]['title'], 'Book 5')