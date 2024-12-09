document.addEventListener('DOMContentLoaded', function() {
    const addBookButton = document.getElementById('add-book');
    const addBookModal = document.getElementById('add-book-modal');
    const addBookForm = document.getElementById('add-book-form');
    const addBookClose = document.getElementsByClassName('close')[0];

    const updateBookModal = document.getElementById('update-book-modal');
    const updateBookForm = document.getElementById('update-book-form');
    const updateBookClose = document.getElementsByClassName('close')[1];

    const rentBookModal = document.getElementById('rent-book-modal');
    const rentBookForm = document.getElementById('rent-book-form');
    const rentBookClose = document.getElementsByClassName('close')[2];

    const returnBookModal = document.getElementById('return-book-modal');
    const returnBookForm = document.getElementById('return-book-form');
    const returnBookClose = document.getElementsByClassName('close')[3];

    const addMemberButton = document.getElementById('add-member');
    const addMemberModal = document.getElementById('add-member-modal');
    const addMemberForm = document.getElementById('add-member-form');
    const addMemberClose = document.getElementsByClassName('close')[4];

    const updateMemberModal = document.getElementById('update-member-modal');
    const updateMemberForm = document.getElementById('update-member-form');
    const updateMemberClose = document.getElementsByClassName('close')[5];

    // Fetch and display books
    function fetchBooks() {
        fetch('/api/books')
            .then(response => response.json())
            .then(data => {
                const booksTable = document.getElementById('books-table').getElementsByTagName('tbody')[0];
                booksTable.innerHTML = '';
                data.forEach(book => {
                    const row = booksTable.insertRow();
                    row.insertCell(0).textContent = book.id;
                    row.insertCell(1).textContent = book.title;
                    row.insertCell(2).textContent = book.author;
                    row.insertCell(3).textContent = book.isbn;
                    row.insertCell(4).textContent = book.publication_year;
                    row.insertCell(5).textContent = book.status;
                    const actionsCell = row.insertCell(6);
                    const updateButton = document.createElement('button');
                    updateButton.textContent = 'Update';
                    updateButton.onclick = () => openUpdateBookModal(book);
                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Delete';
                    deleteButton.onclick = () => deleteBook(book.id);
                    const rentButton = document.createElement('button');
                    rentButton.textContent = 'Rent';
                    rentButton.onclick = () => openRentBookModal(book);
                    const returnButton = document.createElement('button');
                    returnButton.textContent = 'Return';
                    returnButton.onclick = () => openReturnBookModal(book);
                    actionsCell.appendChild(updateButton);
                    actionsCell.appendChild(deleteButton);
                    actionsCell.appendChild(rentButton);
                    actionsCell.appendChild(returnButton);
                });
            });
    }

    // Fetch and display members
    function fetchMembers() {
        fetch('/api/members')
            .then(response => response.json())
            .then(data => {
                const membersTable = document.getElementById('members-table').getElementsByTagName('tbody')[0];
                membersTable.innerHTML = '';
                data.forEach(member => {
                    const row = membersTable.insertRow();
                    row.insertCell(0).textContent = member.id;
                    row.insertCell(1).textContent = member.name;
                    row.insertCell(2).textContent = member.membership_id;
                    row.insertCell(3).textContent = member.contact_info;
                    const actionsCell = row.insertCell(4);
                    const updateButton = document.createElement('button');
                    updateButton.textContent = 'Update';
                    updateButton.onclick = () => openUpdateMemberModal(member);
                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Delete';
                    deleteButton.onclick = () => deleteMember(member.id);
                    actionsCell.appendChild(updateButton);
                    actionsCell.appendChild(deleteButton);
                });
            });
    }

    // Add Book Modal
    addBookButton.onclick = () => addBookModal.style.display = 'block';
    addBookClose.onclick = () => addBookModal.style.display = 'none';
    addBookForm.onsubmit = (event) => {
        event.preventDefault();
        const formData = new FormData(addBookForm);
        fetch('/api/books', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: formData.get('title'),
                author: formData.get('author'),
                isbn: formData.get('isbn'),
                publication_year: formData.get('publication_year')
            })
        }).then(() => {
            addBookModal.style.display = 'none';
            fetchBooks();
        });
    };

    // Update Book Modal
    function openUpdateBookModal(book) {
        document.getElementById('update-book-id').value = book.id;
        document.getElementById('update-title').value = book.title;
        document.getElementById('update-author').value = book.author;
        document.getElementById('update-isbn').value = book.isbn;
        document.getElementById('update-publication_year').value = book.publication_year;
        updateBookModal.style.display = 'block';
    }
    updateBookClose.onclick = () => updateBookModal.style.display = 'none';
    updateBookForm.onsubmit = (event) => {
        event.preventDefault();
        const formData = new FormData(updateBookForm);
        fetch(`/api/books/${formData.get('id')}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: formData.get('title'),
                author: formData.get('author'),
                isbn: formData.get('isbn'),
                publication_year: formData.get('publication_year')
            })
        }).then(() => {
            updateBookModal.style.display = 'none';
            fetchBooks();
        });
    };

    // Delete Book
    function deleteBook(bookId) {
        fetch(`/api/books/${bookId}`, {
            method: 'DELETE'
        }).then(() => fetchBooks());
    }

    // Rent Book Modal
    function openRentBookModal(book) {
        document.getElementById('rent-book-id').value = book.id;
        rentBookModal.style.display = 'block';
    }
    rentBookClose.onclick = () => rentBookModal.style.display = 'none';
    rentBookForm.onsubmit = (event) => {
        event.preventDefault();
        const formData = new FormData(rentBookForm);
        fetch(`/api/books/${formData.get('id')}/rent`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                member_id: formData.get('member_id')
            })
        }).then(() => {
            rentBookModal.style.display = 'none';
            fetchBooks();
        });
    };

    // Return Book Modal
    function openReturnBookModal(book) {
        document.getElementById('return-book-id').value = book.id;
        returnBookModal.style.display = 'block';
    }
    returnBookClose.onclick = () => returnBookModal.style.display = 'none';
    returnBookForm.onsubmit = (event) => {
        event.preventDefault();
        const formData = new FormData(returnBookForm);
        fetch(`/api/books/${formData.get('id')}/return`, {
            method: 'POST'
        }).then(() => {
            returnBookModal.style.display = 'none';
            fetchBooks();
        });
    };

    // Add Member Modal
    addMemberButton.onclick = () => addMemberModal.style.display = 'block';
    addMemberClose.onclick = () => addMemberModal.style.display = 'none';
    addMemberForm.onsubmit = (event) => {
        event.preventDefault();
        const formData = new FormData(addMemberForm);
        fetch('/api/members', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: formData.get('name'),
                membership_id: formData.get('membership_id'),
                contact_info: formData.get('contact_info')
            })
        }).then(() => {
            addMemberModal.style.display = 'none';
            fetchMembers();
        });
    };

    // Update Member Modal
    function openUpdateMemberModal(member) {
        document.getElementById('update-member-id').value = member.id;
        document.getElementById('update-name').value = member.name;
        document.getElementById('update-membership_id').value = member.membership_id;
        document.getElementById('update-contact_info').value = member.contact_info;
        updateMemberModal.style.display = 'block';
    }
    updateMemberClose.onclick = () => updateMemberModal.style.display = 'none';
    updateMemberForm.onsubmit = (event) => {
        event.preventDefault();
        const formData = new FormData(updateMemberForm);
        fetch(`/api/members/${formData.get('id')}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: formData.get('name'),
                membership_id: formData.get('membership_id'),
                contact_info: formData.get('contact_info')
            })
        }).then(() => {
            updateMemberModal.style.display = 'none';
            fetchMembers();
        });
    };

    // Delete Member
    function deleteMember(memberId) {
        fetch(`/api/members/${memberId}`, {
            method: 'DELETE'
        }).then(() => fetchMembers());
    }

    // Initial fetch
    fetchBooks();
    fetchMembers();
});