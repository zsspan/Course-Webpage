document.addEventListener("DOMContentLoaded", function() {
    const toggleCheckbox = document.querySelector('.toggle-menu input[type="checkbox"]');
    const loginForm = document.getElementById('login');
    const registerForm = document.getElementById('register');
    const toggleText = document.querySelector('.toggle-menu p');

    // check if the form state is stored in session storage
    const isRegisterShown = sessionStorage.getItem('registerShown');

    // set initial state of button
    if (isRegisterShown === 'true') {
        toggleCheckbox.checked = true;
        registerForm.classList.remove('hidden');
        loginForm.classList.add('hidden');
        toggleText.textContent = "Already registered? Switch to login!";
    }

    // event listener for changing state
    toggleCheckbox.addEventListener("change", function() {
        if (toggleCheckbox.checked) {
            // show register form and hide login form
            sessionStorage.setItem('registerShown', 'true');
            registerForm.classList.remove('hidden');
            loginForm.classList.add('hidden');
            toggleText.textContent = "Already registered? Switch to login!";
        } else {
            // show login form and hide register form
            sessionStorage.removeItem('registerShown');
            loginForm.classList.remove('hidden');
            registerForm.classList.add('hidden');
            toggleText.textContent = "Need an account? Switch to register!";
        }
    });

    // changes state of button
    window.addEventListener("load", function() {
        if (isRegisterShown === 'true') {
            toggleCheckbox.checked = true;
        } else {
            toggleCheckbox.checked = false;
        }
    });
});
