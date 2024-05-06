document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');

    if (!loginForm) {
        console.error('Login form not found on the page.');
        return; // Ensure the login form is present to prevent errors
    }

    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        if (!username || !password) {
            alert('Username and password are required.');
            return; // Stop the submission if fields are empty
        }

        fetch('/login', {
            method: 'POST',
            body: new URLSearchParams({ 'username': username, 'password': password }),
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        }).then(response => {
            if (response.redirected) {
                window.location.href = response.url; // Follow redirect if occurred
                return null; // Stop further processing the promise chain
            }
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json(); // Convert to JSON if response is valid
        }).then(data => {
            if (!data) return; // Stop if data is null (due to redirect handling)
            // Handle any JSON data from the server
            if (data.message) {
                alert(data.message);
            }
        }).catch(error => {
            // Handle any errors that occurred during fetch
            console.error('Error:', error);
            alert('Login failed. Please check the console for more information.');
        });
    });
});
