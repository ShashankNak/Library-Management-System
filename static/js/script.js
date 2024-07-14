// If you need specific JS functionalities, add them here
document.getElementById('search-btn').addEventListener('click', function() {
    const searchQuery = document.getElementById('search-input').value;
    window.location.href = `/search?query=${searchQuery}`;
});

document.addEventListener('DOMContentLoaded', () => {
    const readMoreLinks = document.querySelectorAll('.read-more');

    readMoreLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const bookCard = this.closest('.book-card');
            const description = bookCard.querySelector('.description');
            const moreText = bookCard.querySelector('.more-text');
            
            if (description.style.display === 'none') {
                description.style.display = 'block';
                moreText.style.display = 'block';
                this.textContent = 'Read Less';
                bookCard.style.maxHeight = '500px'; // Adjust based on content
            } else {
                description.style.display = 'none';
                moreText.style.display = 'none';
                this.textContent = 'Read More';
                bookCard.style.maxHeight = '150px'; // Original height
            }
        });
    });
});

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




document.querySelectorAll('.issue-book-btn').forEach(button => {
    button.addEventListener('click', function () {
        const isbn = this.getAttribute('data-isbn');
        issueBookToDatabase(isbn);
    });
});

function issueBookToDatabase(isbn) {
    // Send a POST request to Flask route to add the ISBN to the database
    fetch('/issue_book', {
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

document.querySelectorAll('.return-book-btn').forEach(button => {
    button.addEventListener('click', function () {
        const isbn = this.getAttribute('data-isbn');
        returnBookToDatabase(isbn);
    });
});

function returnBookToDatabase(isbn) {
    // Send a POST request to Flask route to add the ISBN to the database
    fetch('/return_book', {
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