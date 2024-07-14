// If you need specific JS functionalities, add them here
document.getElementById('search-btn').addEventListener('click', function () {
    const searchQuery = document.getElementById('search-input').value;
    window.location.href = `/searchL?query=${searchQuery}`;
});

document.querySelectorAll('.add-book-btn').forEach(button => {
    button.addEventListener('click', function () {
        const isbn = this.getAttribute('data-isbn');
        addBookToDatabase(isbn);
    });
});

function addBookToDatabase(isbn) {
    // Send a POST request to Flask route to add the ISBN to the database
    fetch('/add_book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ isbn: isbn })
    })
        .then(response => {
            if (response.ok) {
                // Handle success if needed (e.g., show a message)
                console.log('Book added successfully!');
            } else {
                // Handle error if needed
                console.error('Error adding book to database');
            }
        })
        .catch(error => {
            console.error('Error adding book to database:', error);
        });
}


document.querySelectorAll('.del-book-btn').forEach(button => {
    button.addEventListener('click', function () {
        const isbn = this.getAttribute('data-isbn');
        delBookToDatabase(isbn);
    });
});

function delBookToDatabase(isbn) {
    // Send a POST request to Flask route to add the ISBN to the database
    fetch('/delete_book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ isbn: isbn })
    })
        .then(response => {
            if (response.ok) {
                // Handle success if needed (e.g., show a message)
                console.log('Book Deleted successfully!');
            } else {
                // Handle error if needed
                console.error('Error Deleting book to database');
            }
        })
        .catch(error => {
            console.error('Error Deleting book to database:', error);
        });
}


document.querySelector('.signout').addEventListener('click', function() {
    fetch('/signout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url;  // Redirect to the login page
        }
    }).catch(error => console.error('Error:', error));
});