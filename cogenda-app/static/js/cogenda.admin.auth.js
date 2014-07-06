
$(document).ready(function() {
    $('#login').on('click', function(event) {
        if (event) event.preventDefault();
        if ($('#security-login-form').parsley().validate()) {
            var username = $('#username').val().trim();
            var password = $('#password').val().trim();
            var client = $('#client').val().trim();

            credentials = {
                username: username,
                password: password,
                client: client
            };

            var authenticate = $.ajax({
                dataType: 'json',
                contentType: "application/json",
                url: '/security/authenticate',
                data: JSON.stringify(credentials),
                type: 'POST'
            });

            authenticate.done(function(resp) {
                var result = JSON.parse(resp);
                if (!result.auth_success) {
                    $('#login-msg').text(result.msg);
                    $('#login-msg-container').show();
                    return;
                }
                window.location = result.refer;
            });

            authenticate.fail(function(resp, status) {
                //TODO: display error msg on ui.
            });
        } else {
            console.log('Client side validate error.');
        }
    });
});
