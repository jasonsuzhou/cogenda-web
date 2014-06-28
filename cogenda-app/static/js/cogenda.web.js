

$(document).ready(
    function() {
        $("#loginModal").keydown(function(event) {
            if (event.keyCode == 13) {
                alert('Ready to login...')
                //authenticate();
            }
        })
    }
);

function authenticate() {
    //TODO: front-end validation.
    console.log('Ready to login.')
    return;
    $.ajax({
        type: "post",
        dataType: 'json',
        contentType: "application/json",
        url: '/security/authenticate',
        data: $("#loginModal").serialize(),
        success: function (data) {
            if (data != null || data != "") {
                var results = jQuery.parseJSON(data);
                if (results.is_success) {
                    alert('login success...');
                } else {
                   alert('login failure');
                }
            } else {
                alert("Invalid response data!");
            }
        }
    })
}
