function displayErrorsForm(response, errorContainerId) {
    try {
        let form_errors = response.responseJSON.form.errors;
        var errorContainer = null;
        if (form_errors) {
            for (var key in form_errors) {
                errorContainer = document.getElementById(errorContainerId);
                document.getElementById(errorContainerId).style.opacity = 0;
                errorContainer.innerHTML = "<div class='alert alert-warning error_message'>" + form_errors[key] + "</div>";
                fadeIn();
            }
        }

        let fields_name = response.responseJSON.form.fields;
        for (var key in fields_name) {
            let field_id = document.getElementById(`id_${key}`)
            let feedbackAreaa = document.querySelector(`#invalid-feedback-${key}`);
            if (fields_name[key].errors.length > 0) {
                for (var fieldkey in fields_name[key].errors) {
                    field_id.classList.add('is-invalid');
                    feedbackAreaa.style.display = "block";
                    feedbackAreaa.innerHTML = `${fields_name[key].errors[fieldkey]}`
                }
            } else {
                field_id.classList.remove('is-invalid');
                feedbackAreaa.style.display = "none";
                field_id.classList.add('is-valid');
            }
        }
    } catch (TypeError) {
        errorContainer = document.getElementById(errorContainerId);
        errorContainer.textContent = 'تعداد درخواست‌ها زیاد است. لطفاً دقایقی دیگر مجدداً تلاش کنید.';
        errorContainer.style.display = 'block';
    }
}


function removeIsInvalidElements(formElements) {
    for (var i = 0; i < formElements.length; i++) {
        let element = formElements[i];
        element.classList.remove('is-invalid');
        let feedbackAreaa = document.querySelector(`#invalid-feedback-${element.name}`);
        if (feedbackAreaa) {
            feedbackAreaa.style.display = "none";
        }
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const profileSections = document.querySelectorAll('.profile-section');
    const menuItems = document.querySelectorAll('.list-group-item');

    // Hide all sections except the dashboard initially
    profileSections.forEach(section => {
        section.style.display = 'none';
    });
    document.getElementById('dashboard').style.display = 'block';

    // Add event listener to menu items
    menuItems.forEach(item => {
        item.addEventListener('click', event => {
            event.preventDefault();
            const target = event.target.getAttribute('data-target');

            if (target === 'logout') {
                // Show a confirmation dialog
                const confirmed = confirm("آیا برای خارج شدن مطمئن هستید؟");
                if (confirmed) {
                    // Proceed with logout
                    window.location.href = event.target.href;
                } else {
                    // Do nothing if not confirmed
                    return;
                }
            } else {
                // Hide all sections
                profileSections.forEach(section => {
                    section.style.display = 'none';
                });

                // Display the selected section
                document.getElementById(target).style.display = 'block';

                // Remove active class from all menu items
                menuItems.forEach(item => {
                    item.classList.remove('active');
                });

                // Add active class to the clicked menu item
                event.target.classList.add('active');
            }
        });
    });
});


function setUsernameAjax() {
    let myForm = document.getElementById('set_username_form');
    let formElements = myForm.elements;

    removeIsInvalidElements(formElements);
    let setUsernameBtn = document.getElementById('setUsernameBtn');
    setUsernameBtn.innerHTML = `در حال تغییر....`;

    var data = new FormData(myForm);

    $.ajax({
        type: 'POST',
        url: setUsernameUrl,
        data: data,
        cache: false,
        processData: false,
        contentType: false,

        success: function (response) {
            setUsernameBtn.innerHTML = `تغییر نام کاربری`;
            location.reload();
            window.scrollTo(0, 0);
        },
        error: function (response) {
            displayErrorsForm(response, "set_username_error_container");
            setUsernameBtn.innerHTML = `تغییر نام کاربری`;
        }
    });
}


function updateProfileAjax() {
    let myForm = document.getElementById('profile_form');
    let formElements = myForm.elements;

    removeIsInvalidElements(formElements);
    let updateProfileBtn = document.getElementById('updateProfileBtn');
    updateProfileBtn.innerHTML = `در حال تغییر....`;

    var data = new FormData(myForm);

    $.ajax({
        type: 'POST',
        url: profileUrd,
        data: data,
        processData: false,
        contentType: false,

        success: function (response) {
            updateProfileBtn.innerHTML = `ذخیره تغییرات`;
            location.reload();
            window.scrollTo(0, 0);
        },
        error: function (response) {
            displayErrorsForm(response, "profile_error_container");
            updateProfileBtn.innerHTML = `ذخیره تغییرات`;
        }
    });

}


function changePassword() {
    let myForm = document.getElementById('change_password_form');
    let formElements = myForm.elements;

    removeIsInvalidElements(formElements);

    let changePasswordBtn = document.getElementById('changePasswordBtn');
    changePasswordBtn.innerHTML = `در حال تغییر رمز عبور....`;

    var data = new FormData(myForm);
    $.ajax({
        type: 'POST',
        url: changePasswordUrl,
        data: data,
        cache: false,
        processData: false,
        contentType: false,

        success: function (response) {
            changePasswordBtn.innerHTML = `تغییر رمز عبور`;
            location.reload();
            window.scrollTo(0, 0);
        },
        error: function (response) {
            displayErrorsForm(response, "change_pass_error_container");
            changePasswordBtn.innerHTML = `تغییر رمز عبور`;
        }
    });
}


function setPassword() {
    let myForm = document.getElementById('set_password_form');
    let formElements = myForm.elements;

    removeIsInvalidElements(formElements);

    let changePasswordBtn = document.getElementById('setPasswordBtn');
    changePasswordBtn.innerHTML = `در حال قراردادن رمز عبور....`;


    var data = new FormData(myForm);
    $.ajax({
        type: 'POST',
        url: setPasswordUrl,
        data: data,
        cache: false,
        processData: false,
        contentType: false,

        success: function (response) {
            changePasswordBtn.innerHTML = `قراردادن رمز عبور`;
            location.reload();
            window.scrollTo(0, 0);
        },
        error: function (response) {
            displayErrorsForm(response, "set_pass_error_container");
            changePasswordBtn.innerHTML = `قراردادن رمز عبور`;
        }
    });
}
