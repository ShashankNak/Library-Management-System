document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('search-btn');
    const signoutBtn = document.querySelector('.signout');
    const readMoreLinks = document.querySelectorAll('.read-more');

    searchBtn.addEventListener('click', function() {
        const searchQuery = document.getElementById('search-input').value;
        alert('Searching for: ' + searchQuery);
    });

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

// document.querySelector('.signout').addEventListener('click', function() {
//     fetch('register', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         }
//     }).then(response => {
//         if (response.redirected) {
//             window.location.href = response.url;  // Redirect to the login page
//         }
//     }).catch(error => console.error('Error:', error));
// });
