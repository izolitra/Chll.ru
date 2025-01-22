$(document).ready(() => {
    $("#sendRequestBtn").click(() => {
        $("#sendRequestBtn").prop('disabled', true);

        var form_data = new FormData();
        var ins = document.getElementById('multipleFileInput').files.length;

        for (var x = 0; x < ins; x++) {
            form_data.append("files[]", document.getElementById('multipleFileInput').files[x]);
        }

        csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

        headers = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest', 'X-CSRFToken': csrf_token};

        form_data.append("namethree", $("#namethree").val())
        form_data.append("phonethree", $("#phonethree").val())
        form_data.append("emailthree", $("#emailthree").val())

        $.ajax({
            url: "/form/",
            method: "POST",
            headers: headers,
            cache: false,
            data: form_data,
            contentType: false,
            processData: false,
            success: (response) => {
                if (response.success == true) {
                    $("#namethree").val('')
                    $("#phonethree").val('')
                    $("#emailthree").val('')
                    $("#multipleFileInputthree").val('')

                    $("#requestModal").modal('hide');
                    $("#messageSuccessModal").modal('show');
                }
            },
            error: (error) => {
                alert("Произошла ошибка!")
            },
            complete: () => {
                $("#sendRequestBtn").prop('disabled', false);
            }
        })
    });
});


