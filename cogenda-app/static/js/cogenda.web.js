
$(document).ready(function() {

    var commonLanguge;

    $.ajax({
        type: 'GET',
        async: false,
        dataType: 'json',
        url:'/web/init-common-language',
        success: function(data) {
            commonLanguge = $.parseJSON(data);
        }
    });

    $('video').mediaelementplayer({
        features: ['playpause','progress','current','duration','tracks','volume','fullscreen']
    });

    /******************************
     * Setting parsley locale
     *****************************/
    locale = $('#locale').val();
    if (locale.indexOf('zh') >=0) {
        locale = 'zh_cn';
    }
    if (locale.indexOf('en') >=0) {
        locale = 'en';
    }
    window.ParsleyValidator.setLocale(locale);

    // Menu
    if(commonLanguge['username'].trim().length > 0) {
        $('#login').hide();
        show_profile_menu(commonLanguge['username'], commonLanguge['myprofile'], commonLanguge['signout']);
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
                    pop_msg('user-login-msg', result.msg, 0);
                    return;
                }
                $('#loginModal').modal('hide');
                $('#login').hide();
                show_profile_menu(username, commonLanguge['myprofile'], commonLanguge['signout']);
                $('#user-profile-container').show();

                // If @ download page
                if(self.location.href.indexOf('article/downloads') > 0) {
                    self.location = "/article/downloads";
                }
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

    $("#change-password-btn").on('click', function (event) {
        if (event) event.preventDefault();
        if ($('#userProfileModal').parsley().validate()) {
            var username = $('#login-username').text();
            var password1 = $('#password1').val().trim();
            var password2 = $('#password2').val().trim();

            if (password1 !== password2) {
                pop_msg('change-password-msg', commonLanguge['Two passwords are not the same'], 1);
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
                        pop_msg('change-password-msg', commonLanguge['Password is changed successfully'], 2);
                    } else {
                        pop_msg('change-password-msg', commonLanguge['Encounter error in server'], 0);
                    }
                }
            });
        }
    });

    // Load download page
    if(self.location.href.indexOf('article/downloads') > 0) {
        $.ajax({
            type: 'GET',
            async: false,
            dataType: 'json',
            url:'/resources',
            success: function(data) {
                for(var i = 0; i < data.length; i++) {
                    var desc = data[i].description;
                    if(desc === null || desc.length === 0)
                        desc = data[i].name;
                    var tr = "<tr><td >" + desc + "</td><td ><a style=\"cursor: pointer;\" class=\"resource-class\">" + data[i].name + "<input type=\"hidden\" value=\"" + data[i].id + "\"></a></td></tr>";
                    if(data[i].type === '1')
                        $('#documentations tr:last').after(tr);
                    if(data[i].type === '2')
                        $('#publications tr:last').after(tr);
                    if(data[i].type === '3')
                        $('#brochures tr:last').after(tr);
                    if(data[i].type === '4' || data[i].type === '5')
                        $('#installers tr:last').after(tr);
                    if(data[i].type === '6') {
                        $('#private tr:last').after(tr);
                        $('#private-area').show();
                    }
                }
            }
        });
    }

    $('.resource-class').on('click', function (event) {
        if (event) event.preventDefault();

        $('#download-msg-container').hide();

        var r_id = event.target.children[0].value;
        var checkResource = $.ajax({
            "dataType": 'json',
            "type": "GET",
            "url": "/check-resource/" + r_id
        });

        checkResource.done(function (resp) {
            var result = JSON.parse(resp);
            if (typeof(result.auth_status) === 'undefined') {
                pop_msg('download-msg', result.msg, 0);
            } else if (result.auth_status) {
                self.location = result.link;
            } else {
                pop_msg('user-login-msg', result.msg, 1);
                $('#loginModal').modal('show');
            }
        });
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

function switch_locale(locale) {
    $.ajax({
        type: 'GET',
        async: false,
        dataType: 'json',
        url:'/switch/' + locale,
        success: function(resp) {
            var result = JSON.parse(resp);
            if (result.is_success) {
                window.location = '/article/'+result.uri;
            }
        }
    });
}

function show_profile_menu(userName, myProfile, signOut) {
    $('#user-profile-container').append('<a id="login-username" href="#"><span>'+userName+'</span></a><ul><li><a href="/web/logout">'+signOut+'</a></li><li><a id="my-profile">'+myProfile+'</a></li></ul>');

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
}