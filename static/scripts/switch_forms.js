
document.addEventListener('DOMContentLoaded', () => {
    const signUpContainer = document.getElementById('sign-up-container');
    const loginContainer = document.getElementById('login-container');
    const showLoginLink = document.getElementById('show-login');
    const showSignUpLink = document.getElementById('show-signup');

    // Initially, show the login form and hide the sign-up form
    signUpContainer.style.display = 'none';
    loginContainer.style.display = 'block';

    showLoginLink.addEventListener('click', (event) => {
        event.preventDefault();
        signUpContainer.style.display = 'none';
        loginContainer.style.display = 'block';
    });

    showSignUpLink.addEventListener('click', (event) => {
        event.preventDefault();
        loginContainer.style.display = 'none';
        signUpContainer.style.display = 'block';
    });
});
