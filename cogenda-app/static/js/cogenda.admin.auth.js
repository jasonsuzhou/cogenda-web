
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
                url: '/security/authenticate',
                data: JSON.stringify(credentials),
                type: 'POST'
            });

            authenticate.done(function(resp) {
                $('#password-error ul').children().remove();
                console.log("Auth done!");
                var result = JSON.parse(resp);
                if (!result.auth_success) {
                    //TODO: display error msg on UI.
                    console.log(result.msg);

                    $('#auth-error ul').children().remove();
                    var li = $('<li>');
                    li.attr('class', 'parsley-required');
                    li.text(result.msg);
                    $('#auth-error ul').attr('class', 'parsley-errors-list filled').append(li);

                    return
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
