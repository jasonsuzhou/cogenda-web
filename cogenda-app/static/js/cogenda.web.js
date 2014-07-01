
$(document).ready(function() {

    if($('#login-username').text().trim()) {
        $('#login').hide();
        $('#user-profile-container').show();
    } else {
        $('#login').show();
        $('#user-profile-container').hide();
    }

    $('.bxslider').bxSlider({
        auto: true,
        autoControls: true,
        adaptiveHeight: true,
        mode: 'fade',
        preloadImages: 'all',
        captions: false
        //onSlideBefore: function() {
        //    //alert($e);
        //    //console.log($e);
        //    //var cap = $e.attr('title');
        //    //console.log(cap);
        //    $('#img_caption').html('xxxxxxxxxxxxxxxxxxx');
        //},
    });

    $("#login").on('click', function (event) {
        if (event) event.preventDefault();
        $('#loginModal').parsley().reset();
        $('#loginModal').modal('show');
        $('#user-login-msg-container').hide();
    });

    $("#login-btn").on('click', function (event) {
        if (event) event.preventDefault();
        if ($('#loginModal').parsley().validate()) {
            var username = $('#username').val().trim();
            var password = $('#password').val().trim();
            var client = $('#client').val().trim();

            var credentials = {
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

            authenticate.done(function (resp) {
                var result = JSON.parse(resp);
                if (!result.auth_success) {
                    $('#user-login-msg').text(result.msg);
                    $('#user-login-msg-container').show();
                    return;
                }
                $('#loginModal').modal('hide');
                $('#login').hide();
                $('#login-username').text(username);
                $('#user-profile-container').show();
            });
        } else {
            console.log('Client side validate error.');
        }
    });

    $("#request-account").on('click', function (event) {
        if (event) event.preventDefault();
        $('#username2').val('');
        $('#email').val('');
        $('#notes').val('');
        $('#loginModal').modal('hide');
        $('#requestAccountModal').parsley().reset();
        $('#requestAccountModal').modal('show');
        $('#request-account-msg-container').hide();
    });

    $("#request-account-btn").on('click', function (event) {
        if (event) event.preventDefault();
        if ($('#requestAccountModal').parsley().validate()) {
            $("#request-account-btn").attr('class', 'btn btn-primary btn-processing');

            var username = $('#username2').val().trim();
            var email = $('#email').val().trim();
            var notes = $('#notes').val().trim();

            var account_request = {
                username: username,
                email: email,
                notes: notes
            };

            var send_request = $.ajax({
                dataType: 'json',
                contentType: "application/json",
                url: '/user/request-an-account',
                data: JSON.stringify(account_request),
                type: 'POST'
            });

            send_request.done(function (resp) {
                var result = JSON.parse(resp);
                if (result.is_success) {
                    pop_msg('request-account-msg', result.msg, 2);
                    setTimeout(function() {
                        $('#requestAccountModal').modal('hide');
                    }, 2000);
                    $('#request-account-btn').off('click');
                } else {
                    pop_msg('request-account-msg', result.msg, 1);
                }
                $("#request-account-btn").attr('class', 'btn btn-primary btn-check');
            });
        } else {
            console.log('Client side validate error.');
        }
    });

    $("#my-profile").on('click', function (event) {
        if (event) event.preventDefault();
        $('#password1').val('');
        $('#password2').val('');
        $('#userProfileModal').parsley().reset();
        $('#userProfileModal').modal('show');
        $('#change-password-msg-container').hide();

        var username = $('#login-username').text();

        var fetchUserProfile = $.ajax({
            "dataType": 'json',
            "type": "GET",
            "url": "/user/user-profile/" + username
        });

        fetchUserProfile.done(function (result) {
            //$('#uid').val(result.id);
            $('#u_name').text(result.username);
            $('#u_company').text(result.company);
            $('#u_email').text(result.email);
            $('#u_mobile').text(result.mobile);
        });
    });

    $("#change-password-btn").on('click', function (event) {
        if (event) event.preventDefault();
        if ($('#userProfileModal').parsley().validate()) {
            var username = $('#login-username').text();
            var password1 = $('#password1').val().trim();
            var password2 = $('#password2').val().trim();

            if (password1 !== password2) {
                pop_msg('change-password-msg', 'Two passwords are not the same.', 1);
                return;
            }

            var user_pwd = {
                username: username,
                password: password1
            };

            $.ajax({
                dataType: 'json',
                data: JSON.stringify(user_pwd),
                contentType: "application/json",
                type: "POST",
                url: '/user/change-password',
                success: function (result) {
                    if (result.id) {
                        pop_msg('change-password-msg', 'Password is changed.', 2);
                    } else {
                        pop_msg('change-password-msg', 'Encounter error in server.', 0);
                    }
                }
            });
        }
    });
});

function pop_msg(msg_label, msg, type) {
    // type = 0 - Error, 1 - Alert, 2 - Success
    var label_classes = "";
    var container_classes = "";
    if(type == 0) {
        container_classes = 'alert alert-danger';
        label_classes = 'fa fa-times-circle sign';
    } else if(type === 1) {
        container_classes = 'alert alert-warning';
        label_classes = 'fa fa-warning sign';
    } else if(type === 2) {
        container_classes = 'alert alert-success';
        label_classes = 'fa fa-check sign';
    }
    $('#'+msg_label+'-container').attr('class', container_classes);
    $('#'+msg_label+'-container' + ' i').attr('class', label_classes);
    $('#'+msg_label).text(msg);
    $('#'+msg_label+'-container').show();
}
