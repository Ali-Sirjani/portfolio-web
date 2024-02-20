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


function createMessage() {
    let myForm = document.getElementById('contact_form');
    let formElements = myForm.elements;

    removeIsInvalidElements(formElements);
    let contactFormBtn = document.getElementById('id_contact_form_btn');
    contactFormBtn.innerHTML = `در حال ارسال....`;

    var data = new FormData(myForm);

    $.ajax({
        type: 'POST',
        url: createMessageUrl,
        data: data,
        cache: false,
        processData: false,
        contentType: false,

        success: function (response) {
            contactFormBtn.innerHTML = `ارسال پیام`;
            location.reload();
            window.scrollTo(0, 0);
        },
        error: function (response) {
            console.log('this is locg')
            displayErrorsForm(response, "error-msg");
            contactFormBtn.innerHTML = `ارسال پیام`;
        }
    });
}
