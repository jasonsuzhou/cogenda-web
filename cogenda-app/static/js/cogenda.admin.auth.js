
$(document).ready(function() {
    $('#login').on('click', function(event) {
        if (event) event.preventDefault();
        if ($('#security-login-form').parsley().validate()) {
            var username = $('#username').val().trim();
            var password = $('#password').val().trim();

            credentials = {
                username: username,
                password: password
            };

            var authenticate = $.ajax({
                dataType: 'json',
                contentType: "application/json",
                url: '/admin/authenticate',
                data: JSON.stringify(credentials),
                type: 'POST'
            });

            authenticate.done(function(resp) {
                console.log("Auth done!");
                console.log(resp.auth_token);
                window.location = '/admin/user-mgmt';
            });

            authenticate.fail(function(resp, status) {
                //TODO: handle failure.
            });
        } else {
            console.log('Client side validate error.');
        }
    });
});