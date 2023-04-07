//validate password1 == password 2 
// password length =>4   
let password1 = document.querySelector('input[name="password1"]')
let password2 = document.querySelector('input[name="password2"]')
let invalidFeedback = document.getElementById('validation')

function validatePasswords() {

    //check if user input 2 passwords
    if (password1.value && password2.value) {
        //if 2 password => check password format 
        if (password1.value.length < 4 ) {
            document.getElementById('password1-validation').innerText =
                ' !رمز المرور يتكون من 4 حروف و أرقام علي الأقل';
            password1.classList.add('is-invalid');
            password2.classList.add('is-invalid')

        } else {
            //then check 2 passwords are the same
            if (password1.value != password2.value) {
                invalidFeedback.innerText = 'كلمة المرور غير متطابقة';
                invalidFeedback.classList.add('text-danger', 'text-center');
                password2.classList.add('is-invalid');

            } else {
                //everthing is ok !
                password1.classList.remove('is-invalid');
                password2.classList.remove('is-invalid');
                password1.classList.add('is-valid');
                password2.classList.add('is-valid');
                invalidFeedback.innerText = '';
                document.getElementById('password1-validation').innerText = '';
            }
        }

    } else {
        // At least one password is missing
        password1.classList.remove('is-valid', 'is-invalid');
        password2.classList.remove('is-valid', 'is-invalid');
        invalidFeedback.innerText = '';
    }
}

password1.addEventListener('change', validatePasswords);
password2.addEventListener('change', validatePasswords);



//validate username 
let usernameInput = document.querySelector('input[name="username"]');

usernameInput.addEventListener('blur', (event) => {
    let username = event.target.value;

    if (username) {

        // Send an AJAX request to the server to check if the username exists or not
        fetch(`/auth/validate_username?username=${username}`)
            .then(response => response.json())
            .then(data => {
                console.log(data)
                if (data.is_taken) {
                    usernameInput.classList.add('is-invalid');
                    document.getElementById('username-validation').innerText = 'اسم المستخدم مستخدم بالفعل';
                } else {
                    usernameInput.classList.remove('is-invalid');
                    usernameInput.classList.add('is-valid');
                    document.getElementById('username-validation').innerText = '';
                }
            });
    }
});


//disable submit btn if any error 
const form = document.querySelector('#userForm');
const submitBtn = form.querySelector('button[type="submit"]');

form.addEventListener('input', () => {
    if (form.checkValidity()) {
        submitBtn.disabled = false;
    } else {
        submitBtn.disabled = true;
    }
});