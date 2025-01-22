$(document).ready(function() {
    function checkAllFields() {
        const name = $('#name').val().trim();
        const phone = $('#phone').val().trim();
        const email = $('#email').val().trim();

        if (name !== '' && isValidPhone(phone) && isValidEmail(email)) {
            $('#equipmentChoiceBtn2').prop('disabled', false);
        } else {
            $('#equipmentChoiceBtn2').prop('disabled', true);
        }
    }

    $('#name, #phone, #email').on('input', function() {
        checkAllFields();
    });

    $("#equipmentChoiceBtn2").click(function(event) {
        event.preventDefault();

        if ($('#equipmentChoiceBtn2').prop('disabled')) {
            return false;
        }

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

        console.log("Отправляемые данные:");
        form_data.forEach(function(value, key) {
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
            success: function(response) {
                console.log("Ответ сервера:", response);
                if (response.success == true) {
                    $("#name").val('');
                    $("#phone").val('');
                    $("#email").val('');
                    $("#comment").val('');
                    $("#multipleFileInput").val('');

                    $("#equipmentChoiceModalTwo").modal('hide');
                    $("#messageSuccessModal").modal('show');
                }
            },
            error: function(error) {
                console.error("Ошибка при отправке формы:", error);
                alert("Произошла ошибка!");
            },
            complete: function() {
                $('#equipmentChoiceBtn2').prop('disabled', false);
            }
        });
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

});
