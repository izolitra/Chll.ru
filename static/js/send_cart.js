$(document).ready(function() {
    const commentTextArea = document.getElementById('comment');
    const charCountDisplay = document.getElementById('commentCharCount');
    const maxChars = commentTextArea.getAttribute('maxlength');

    commentTextArea.addEventListener('input', function () {
        const currentLength = commentTextArea.value.length;
        charCountDisplay.textContent = `${currentLength}/${maxChars}`;
    });

    function checkAllFields() {
        const name = $('#name').val().trim();
        const phone = $('#phone').val().trim();
        const email = $('#email').val().trim();

        if (name !== '' && isValidPhone(phone) && isValidEmail(email)) {
            $('#equipmentChoiceBtn').prop('disabled', false);
        } else {
            $('#equipmentChoiceBtn').prop('disabled', true);
        }
    }

    $('#name, #phone, #email').on('input', function() {
        checkAllFields();
    });

    function isValidPhone(phone) {
        const phoneRegex = /^(?:\+?\d{1,15}|\d{1,15})$/;
        return phoneRegex.test(phone);
    }

    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    checkAllFields();

    $('#equipmentChoiceModal').on('submit', 'form', function(event) {
        event.preventDefault();

        if ($('#equipmentChoiceBtn').prop('disabled')) {
            return false;
        }

        $('#equipmentChoiceBtn').prop('disabled', true);
        $('#loadingIndicator').show();

        var form_data = new FormData();
        var ins = document.getElementById('multipleFileInput').files.length;

        for (var x = 0; x < ins; x++) {
            form_data.append("files[]", document.getElementById('multipleFileInput').files[x]);
        }

        var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        var headers = {
            'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest',
            'X-CSRFToken': csrf_token
        };

        form_data.append("name", $("#name").val());
        form_data.append("phone", $("#phone").val());
        form_data.append("email", $("#email").val());
        form_data.append("comment", $("#comment").val());
        form_data.append("cartDetails", $("#cartDetails").val());

        console.log("Отправляемые данные:");
        form_data.forEach((value, key) => {
            console.log(key + ": " + value);
        });

        $.ajax({
            url: "/form/",
            method: "POST",
            headers: headers,
            cache: false,
            data: form_data,
            contentType: false,
            processData: false,
            success: (response) => {
                console.log("Ответ сервера:", response);
                if (response.success) {
                    $("#name").val('');
                    $("#phone").val('');
                    $("#email").val('');
                    $("#comment").val('');
                    $("#cartDetails").val('');
                    $("#multipleFileInput").val('');

                    $("#equipmentChoiceModal").modal('hide');
                    $("#messageSuccessModal").modal('show');
                }
            },
            error: (error) => {
                console.error("Ошибка при отправке формы:", error);
                alert("Произошла ошибка!");
            },
            complete: () => {
                $('#equipmentChoiceBtn').prop('disabled', false);
                $('#loadingIndicator').hide();
            }
        });
    });

});
