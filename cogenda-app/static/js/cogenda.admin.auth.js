
$(document).ready(function() {
    $('#login').on('click', function() {
        authenticate();
    });
});

function authenticate() {
    if ($('#security-login-form').parsley().validate()) {
        var username = $('#username').val().trim();
        var password = $('#password').val().trim();

        credentials = {
            username: username,
            password: password
        };

        $.ajax({
            dataType: 'json',
            contentType: "application/json",
            url: '/admin/authenticate',
            data: JSON.stringify(credentials),
            type: 'POST',
            success: function(result) {
                console.log("MMMMMMMMMMMMMMMMMMMM");
            }
        });

        /*
        authenticate.promise().done(function(resp) {
            console.log("Auth done!");
            self.location.href = '/admin/user-mgmt';
        });*/
    } else {
        console.log('Client side validate error.');
    }
}
