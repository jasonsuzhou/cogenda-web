/***************************************************************
 *
 *                   CONSTANT VARIABLES
 *
 ***************************************************************/

"use strict";

// Message type
var MSG_ERROR = 0;
var MSG_ALERT = 1;
var MSG_SUCCESS = 2;

// Resource type
var RESOURCE_TYPE_PUBLIC_PUBLICATIONS = '1';
var RESOURCE_TYPE_PUBLIC_DOCUMENTATION = '2';
var RESOURCE_TYPE_PUBLIC_EXAMPLES = '3';
var RESOURCE_TYPE_ALLUSER_SOFTWARE_PACKAGES = '4';
var RESOURCE_TYPE_ALLUSER_INSTALLER = '5';
var RESOURCE_TYPE_PRIVATE = '6';


/***************************************************************
 *
 *                 COMMON JAVASCRIPT METHODS
 *
 ***************************************************************/

// Init nprogress
function init_progress(){
    NProgress.configure({
        showSpinner: false
    });
    NProgress.start();
    NProgress.set(0.4);
    var nprogress_interval = setInterval(function() { NProgress.inc(); }, 200);
    return nprogress_interval;
}

function destroy_progress(interval_id) {
    clearInterval(interval_id);
    NProgress.done();
}

var nprogress_interval = init_progress();

// Switch locale
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

// Show user profile menu
function show_profile_menu(userName, myProfile, signOut) {
    $('#user-profile-container').append('<a class="small button fa fa-user" id="login-username" href="#"><span style="padding:4px;">'+userName+'</span></a><ul><li><a class="small button" href="/web/logout">'+signOut+'</a></li><li><a class="small button" id="my-profile">'+myProfile+'</a></li></ul>');

    $("#my-profile").on('click', function (event) {
        if (event) event.preventDefault();
        $('#password1').val('');
        $('#password2').val('');
        $('#userProfileModal').modal('show').parsley().reset();
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

// Message display
// Type = 0 - Error, 1 - Alert, 2 - Success
function pop_msg(msg_label, msg, type) {
    var label_classes = "";
    var container_classes = "";
    switch(type) {
        case MSG_ERROR:
            container_classes = 'alert alert-danger';
            label_classes = 'fa fa-times-circle sign';
            break;
        case MSG_ALERT:
            container_classes = 'alert alert-warning';
            label_classes = 'fa fa-warning sign';
            break;
        case MSG_SUCCESS:
            container_classes = 'alert alert-success';
            label_classes = 'fa fa-check sign';
            break;
    }
    $('#'+msg_label).text(msg);
    $('#'+msg_label+'-container' + ' i').attr('class', label_classes);
    $('#'+msg_label+'-container').attr('class', container_classes).show();
}


// Document ready
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
    var locale = $('#locale').val();
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
        autoControls: false,
        adaptiveHeight: true,
        mode: 'fade',
        captions: false,
        onSliderLoad: function(){
            $(".bxslider").css("visibility", "visible");
        }
    });

    $("#login").on('click', function (event) {
        if (event) event.preventDefault();
        $('#loginModal').modal('show').parsley().reset();
        $('#user-login-msg-container').hide();
    });

    $("#login-btn").on('click', function (event) {
        if (event) event.preventDefault();
        if ($('#loginModal').parsley().validate()) {
            var username = $('#username').val().trim();
            var password = $('#password').val().trim();
            var client = $('#client').val().trim();

            var credentials = {json: {
                username: username,
                password: password,
                client: client
            }};

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
                    pop_msg('user-login-msg', result.msg, MSG_ERROR);
                    return;
                }
                $('#loginModal').modal('hide');
                $('#login').hide();
                show_profile_menu(username, commonLanguge['myprofile'], commonLanguge['signout']);
                $('#user-profile-container').show();

                // If @ download page
                if(window.location.href.indexOf('article/downloads') > 0) {
                    if($('#r_id').val() !== null && $('#r_id').val().trim().length > 0) {
                        window.location = "/download/"+ $('#r_id').val();
                    }
                    setTimeout(function() {
                        window.location = "/article/downloads";
                    }, 500);
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
        $('#requestAccountModal').modal('show').parsley().reset();
        $('#request-account-msg-container').hide();
    });

    $("#request-account-btn").on('click', function (event) {
        if (event) event.preventDefault();
        if ($('#requestAccountModal').parsley().validate()) {
            $("#request-account-btn").attr('class', 'btn btn-primary btn-processing');

            var username = $('#username2').val().trim();
            var email = $('#email').val().trim();
            var notes = $('#notes').val().trim();

            var account_request = {json: {
                username: username,
                email: email,
                notes: notes
            }};

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
                    pop_msg('request-account-msg', result.msg, MSG_SUCCESS);

                    // Auto refresh download page every 2s.
                    setTimeout(function() {
                        $('#requestAccountModal').modal('hide');
                    }, 2000);

                    $('#request-account-btn').off('click');
                } else {
                    pop_msg('request-account-msg', result.msg, MSG_ALERT);
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
                pop_msg('change-password-msg', commonLanguge['Two passwords are not the same'], MSG_ALERT);
                return;
            }

            var user_pwd = {json: {
                username: username,
                password: password1
            }};

            $.ajax({
                dataType: 'json',
                data: JSON.stringify(user_pwd),
                contentType: "application/json",
                type: "POST",
                url: '/user/change-password',
                success: function (result) {
                    if (result.id) {
                        pop_msg('change-password-msg', commonLanguge['Password is changed successfully'], MSG_SUCCESS);
                    } else {
                        pop_msg('change-password-msg', commonLanguge['Encounter error in server'], MSG_ERROR);
                    }
                }
            });
        }
    });

    /*
    // Load download page
    if(window.location.href.indexOf('article/downloads') > 0) {
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
                    if(data[i].type === RESOURCE_TYPE_PUBLIC_PUBLICATIONS)
                        $('#documentations tr:last').after(tr);
                    if(data[i].type === RESOURCE_TYPE_PUBLIC_DOCUMENTATION)
                        $('#publications tr:last').after(tr);
                    if(data[i].type === RESOURCE_TYPE_PUBLIC_EXAMPLES)
                        $('#brochures tr:last').after(tr);
                    if(data[i].type === RESOURCE_TYPE_ALLUSER_SOFTWARE_PACKAGES || data[i].type === RESOURCE_TYPE_ALLUSER_INSTALLER)
                        $('#installers tr:last').after(tr);
                    if(data[i].type === RESOURCE_TYPE_PRIVATE) {
                        $('#private tr:last').after(tr);
                        $('#private-area').show();
                    }
                }
            }
        });
    }*/

    if(window.location.href.indexOf('article/downloads') > 0) {
        $('.resource-class').on('click', function (event) {
            if (event) event.preventDefault();

            $('#download-msg-container').hide();

            var r_id = event.target.children[0].value;
            $('#r_id').val(r_id);
            var checkResource = $.ajax({
                "dataType": 'json',
                "type": "GET",
                "url": "/check-resource/" + r_id
            });

            checkResource.done(function (resp) {
                var result = JSON.parse(resp);
                if (typeof(result.auth_status) === 'undefined') {
                    pop_msg('download-msg', result.msg, MSG_ERROR);
                } else if (result.auth_status) {
                    window.location = result.link;
                } else {
                    pop_msg('user-login-msg', result.msg, MSG_ALERT);
                    $('#loginModal').modal('show');
                }
            });
        });
    }
});

// Trigger finish when page fully loaded
$(window).load(function(){
    destroy_progress(nprogress_interval);
});

// Trigger bar when exiting the page
$(window).unload(function(){
    NProgress.start();
});
