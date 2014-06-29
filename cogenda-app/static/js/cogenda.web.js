
$(document).ready(function() {
    $("#loginModal").on('click', function (event) {
        if (event) event.preventDefault();
        if ($('#loginModal').parsley().validate()) {
            var username = $('#username').val().trim();
            var password = $('#password').val().trim();

            credentials = {
                username: username,
                password: password
            };

            var authenticate = $.ajax({
                dataType: 'json',
                contentType: "application/json",
                url: '/security/authenticate',
                data: JSON.stringify(credentials),
                type: 'POST'
            });

            authenticate.done(function (resp) {
                var result = JSON.parse(resp);
                if (!result.auth_success) {
                    $('#user-login-msg').text(result.msg);
                    $('#user-login-msg-container').show();
                    return;
                }
                $('#login').hide();
                $('#username').show();
            });

            authenticate.fail(function (resp, status) {
                //TODO: display error msg on ui.
            });
        } else {
            console.log('Client side validate error.');
        }
    });
});
