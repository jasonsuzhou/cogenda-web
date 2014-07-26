/***************************************************************
 *
 *                    CONSTANT VARIABLES
 *
 ***************************************************************/
"use strict";

// Object type
var OBJ_USER = 'USER';
var OBJ_RESOURCE = 'RESOURCE';

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

// User type
var USER_TYPE_RESOURCE = '1';
var USER_TYPE_RESOURCE_OWNER = '2';
var USER_TYPE_ADMINISTRATOR = '3';

// Vendor type
var VENDOR_TYPE_OOS = 'oss';
var VENDOR_TYPE_S3 = 's3';

// Vendor display name
var VENDOR_OOS_DISPLAY_NAME = 'AliYun';
var VENDOR_S3_DISPLAY_NAME = 'AWS S3';

/*****************************************************************
 *
 *                      NProgress
 *
 *****************************************************************/
// Init nprogress
$(function() {
    $(document).on('ajaxStart', function() { NProgress.start(); });
    $(document).on('ajaxStop',  function() { NProgress.done();  });
});

function init_progress(){
    NProgress.start();
    NProgress.set(0.4);
    var nprogress_interval = setInterval(function() { NProgress.inc(); }, 200);
    return nprogress_interval;
}

function destroy_progress(interval_id) {
    clearInterval(interval_id);
    NProgress.done();
}

/****************************************************************
 *
 *                COMMON JAVASCRIPT METHODS
 *
 * **************************************************************/


var nprogress_interval = init_progress();

var commonLanguge;

function ready_common_i18n_info() {
    $.ajax({
        type: 'GET',
        async: false,
        dataType: 'json',
        url:'/admin/init-common-language',
        success: function(data) {
            commonLanguge = $.parseJSON(data);
        }
    });
}

function remove_selected_rows(local_table) {
    var selected_rows = local_table.$('tr.row_selected');
    selected_rows.each(function(index, row) {
        local_table.fnDeleteRow(row);
    });
}

// Render pop-up message.
function pop_msg(msg_label, msg, type) {
    // type = 0 - Error, 1 - Alert, 2 - Success
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

// Mapping vendor display name.
function convert_vendor_name(vendor) {
    if(vendor === VENDOR_TYPE_OOS)
        return VENDOR_OOS_DISPLAY_NAME;
    else if(vendor === VENDOR_TYPE_S3)
        return VENDOR_S3_DISPLAY_NAME;
    else
        return vendor;
}

// Retrieve resource display type.
function get_resource_type(_type) {
    var resource_type = 'Private';
    switch(_type) {
        case RESOURCE_TYPE_PUBLIC_PUBLICATIONS:
            resource_type = 'Public - Publications';
            break;
        case RESOURCE_TYPE_PUBLIC_DOCUMENTATION:
            resource_type = 'Public - Documentation';
            break;
        case RESOURCE_TYPE_PUBLIC_EXAMPLES:
            resource_type = 'Public - Examples';
            break;
        case RESOURCE_TYPE_ALLUSER_SOFTWARE_PACKAGES:
            resource_type = 'AllUser - Software Packages';
            break;
        case RESOURCE_TYPE_ALLUSER_INSTALLER:
            resource_type = 'AllUser - Installer';
            break;
        case RESOURCE_TYPE_PRIVATE:
            resource_type = 'Private';
            break;
    }
    return resource_type;
}

// Retrieve role i18n display name.
function get_role_name(role_id) {
    var role_name = commonLanguge['Resource'];
    if(role_id === USER_TYPE_RESOURCE)
        role_name = commonLanguge['Resource'];
    else if(role_id === USER_TYPE_RESOURCE_OWNER)
        role_name = commonLanguge['Resource Owner'];
    else if(role_id === USER_TYPE_ADMINISTRATOR)
        role_name = commonLanguge['Administrator'];
    return role_name;
}


// Retrieve user i18n status.
function get_user_status(active) {
    var status = commonLanguge['No'];
    if(active)
        status = commonLanguge['Yes'];
    return status;
}

// Retrieve user table i18n columns.
function get_user_table_columns(userTableTitle) {
    var columns = [
        {
          "sTitle": "ID",
          "mData": "id",
          "bVisible": false
        },
        {
          "sTitle": userTableTitle['username'],
          "mData": "username"
        },
        {
          "sTitle": userTableTitle['company'],
          "mData": "company"
        },
        {
          "sTitle": userTableTitle['email'],
          "mData": "email"
        },
        {
          "sTitle": userTableTitle['mobile'],
          "mData": "mobile"
        },
        {
          "sTitle": userTableTitle['role'],
          "mData": "role"
        },
        {
          "sTitle": userTableTitle['active'],
          "mData": "active"
        }
        ];
        return columns;
}

// Retrieve resource table i18n columns.
function get_resource_table_columns(resourceTableTitle) {
    var columns = [
        {
          "sTitle": "ID",
          "mData": "id",
          "bVisible": false
        },
        {
          "sTitle": resourceTableTitle['Resource Name'],
          "mData": "name"
        },
        {
          "sTitle": resourceTableTitle['Description'],
          "mData": "description"
        },
        {
          "sTitle": resourceTableTitle['Vendor'],
          "mData": "vendor"
        },
        {
          "sTitle": resourceTableTitle['Uploaded Date'],
          "mData": "uploaded_date"
        },
        {
          "sTitle": resourceTableTitle['Type'],
          "mData": "type"
        },
        {
          "sTitle": resourceTableTitle['Active'],
          "mData": "active"
        }
    ];
    return columns;
}

// Process object attributes' values to displaying values
function process_object_result(obj_type, result) {
    result.splice(result.length - 1,result.length);
    for(var i = 0; i < result.length; i++) {
        // Common attributes
        result[i].active = get_user_status(result[i].active);
        // Convert object User
        if(obj_type === OBJ_USER)
            result[i].role = get_role_name(result[i].role);
        // Convert object Resource
        if(obj_type === OBJ_RESOURCE)
            result[i].type = get_resource_type(result[i].type);
    }
    return result;
}


/***************************************************************
 *
 *                 COMMON UI COMPONENTS
 *
 ***************************************************************/

// Retrieve data table columns via the url
function get_table_columns(tableTitle, url) {
    if('/admin/users' === url) {
       return get_user_table_columns(tableTitle);
    }
    if('/admin/resources' === url) {
        return get_resource_table_columns(tableTitle);
    }
}

// Common ready for select2.
function ready_common_select2() {
    $(".select2").select2({
        width: '100%'
    });
}

// Common ready for switch.
function ready_common_switch() {
    $('.switch').bootstrapSwitch();
}

// Common ready for searchable multi select.
function ready_common_searchable_multi_select() {
    /*Multi-Select Search*/
    $('.searchable').multiSelect({
        selectableHeader: "<input type='text' class='form-control search-input' autocomplete='off' placeholder="+ commonLanguge['Filter String'] +">",
        selectionHeader: "<input type='text' class='form-control search-input' autocomplete='off' placeholder="+ commonLanguge['Filter String'] +">",
        afterInit: function(ms) {
            var that = this,
                $selectableSearch = that.$selectableUl.prev(),
                $selectionSearch = that.$selectionUl.prev(),
                selectableSearchString = '#' + that.$container.attr('id') + ' .ms-elem-selectable:not(.ms-selected)',
                selectionSearchString = '#' + that.$container.attr('id') + ' .ms-elem-selection.ms-selected';

            that.qs1 = $selectableSearch.quicksearch(selectableSearchString).on('keydown', function(e) {
                if (e.which === 40) {
                    that.$selectableUl.focus();
                    return false;
                }
            });

            that.qs2 = $selectionSearch.quicksearch(selectionSearchString).on('keydown', function(e) {
                if (e.which === 40) {
                    that.$selectionUl.focus();
                    return false;
                }
            });
        },
        afterSelect: function() {
            this.qs1.cache();
            this.qs2.cache();
        },
        afterDeselect: function() {
            this.qs1.cache();
            this.qs2.cache();
        }
    });
}

// Common ready for data tables.
function ready_common_datatable(obj_type, url, orderIndex, fnDatatableCallback) {
    $.ajax({
        "dataType": 'json',
        "type": "GET",
        "url": url,
        "success": function(result) {
            var datatable_id = "mgmt-datatable";

            var datatable_div = datatable_id + '-container';
            $("#" + datatable_div).html('<table class="table table-bordered" id="' + datatable_id + '"></table>');
            datatable_id = "#" + datatable_id;

            /* Init the table with dynamic ajax loader.*/
            var tableLanguage;
            $.ajax({
                type: 'GET',
                async: false,
                dataType: 'json',
                url:'/admin/init-table-language',
                success: function(data) {
                    tableLanguage = $.parseJSON(data);
                }
            });
            var tableColumns = result[result.length - 1];
            var columns = get_table_columns(tableColumns, url);
            var datatable = $(datatable_id).dataTable({
                "aaData": process_object_result(obj_type, result),
                "aoColumns": columns,
                "aaSorting": [[orderIndex, "desc"]],
                "oLanguage": {
                    "sLengthMenu" : " "+tableLanguage['sShowRows']+" ",
                    "sZeroRecords" : tableLanguage['sZeroRecords'],
                    "sInfo" : tableLanguage['sInfo'],
                    "sInfoEmpty" : tableLanguage['sInfoEmpty'],
                    "sInfoFiltered" : tableLanguage['sInfoFiltered'],
                    "oPaginate": {
                        "sFirst" : tableLanguage['oPaginate_sFirst'],
                        "sPrevious" : tableLanguage['oPaginate_sPrevious'],
                        "sNext" : tableLanguage['oPaginate_sNext'],
                        "sLast" : tableLanguage['oPaginate_sLast']
                    }
                }
            });

            // Add/remove class to a row when clicked on
            $(datatable_id).on('click', 'tbody tr', function(e) {
                $(this).toggleClass('row_selected');
            });

            // Search input style
            $('.dataTables_filter input').addClass('form-control').attr('placeholder', tableLanguage['sSearch']);
            $('.dataTables_length select').addClass('form-control');

            // Callback method for datatable
            fnDatatableCallback(datatable);
        }
    });
}

// Ready for login page.
function ready_login_page() {
    $('#login').on('click', function(event) {
        if (event) event.preventDefault();
        if ($('#security-login-form').parsley().validate()) {
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

            authenticate.done(function(resp) {
                var result = JSON.parse(resp);
                if (!result.auth_success) {
                    $('#login-msg').text(result.msg);
                    $('#login-msg-container').show();
                    return;
                }
                window.location = result.refer;
            });
        } else {
            console.log('Client side validate error.');
        }
    });
}

// Document ready for navigation menu.
function ready_navigation_menu() {
    // Handle menu click event.
    $('ul.cl-vnavigation li').each(function(index, li) {
        var sub_menus = $(li).find('ul');
        var $clink = li.children[0];
        if ($clink.href === String(window.location)) {
            $(this).addClass('active');
        }
    });
}

/**
 * Render active switch component
 *
 */
function render_active_switch(is_active) {
    var _switch = $('.switch-animate');
    if(typeof(is_active) !== 'undefined') {
        if(is_active) {
            _switch.removeClass('switch-off');
            _switch.addClass('switch-on');
        } else {
            _switch.removeClass('switch-on');
            _switch.addClass('switch-off');
        }
    } else {
        _switch.removeClass('switch-off');
        _switch.addClass('switch-on');
    }
}

/**
 * Render role select component
 *
 */
function render_role_select(selectedRole) {
    $('#role').select2("val", selectedRole);
}

// Convert resource string ids to array
function convert_resource(resource_str) {
    if(!resource_str || 0 === resource_str.length){
        return [];
    }
    return resource_str.split(",");
}

// Render resource select component
function render_resource_select(selectedRole, selectedResources) {
    if(selectedRole === USER_TYPE_RESOURCE_OWNER || selectedRole === 'Resource Owner') { // 'Resource Owner'
        // Populate resource select
        $.ajax({
            "dataType": 'json',
            "type": "GET",
            "url": "/admin/private-resources",
            "success": function(result) {
                // console.log(result);
                $('#resource').multiSelect('refresh');
                var k = 0;
                for (var i = 0; i < result.length; i++) {
                    $('#resource').multiSelect('addOption', {value: result[i].id, text: result[i].name + "[" + result[i].vendor + "]", index: k++ });
                }
                $('#resource').multiSelect('deselect_all');
                if (typeof(selectedResources) !== 'undefined') {
                    $('#resource').multiSelect('select', selectedResources);
                }
                $('#resource-container').show();
            }
        });
    } else {
        $('#resource-container').hide();
    }
}

// Reset msg & components for user create modal
function reset_user_create_modal() {
    // Reset parsley
    $('#new-modal').parsley().reset();

    // Reset title/button
    $('#title').text(commonLanguge['Create User']);

    // Reset values here
    $('#uid').val("");
    $('#name').val("");
    $('#password').val("");
    $('#company').val("");
    $('#email').val("");
    $('#mobile').val("");
    $('#notes').val("");

    // Reset password
    $('#password').show();
    $('#reset-password-container').hide();

    // Active switch
    render_active_switch();

    // Role select
    render_role_select(USER_TYPE_RESOURCE);

    // Resource select
    render_resource_select();
}

function off_user_click_event() {
    // Call Add modal
    $("#add").off('click');

    // Edit by click edit link & row double click
    $("#edit").off('click');

    // Delete users
    $("#delete").off('click');

    // Create new user
    $("#save").off('click');

    // Reset password
    $("#reset-password").off('click');

    // Save as new user
    $("#save-as").off('click');
}

/**
 * Delete users
 *
 */
function delete_user() {
    $('#user-msg-container').hide();
    var current_username = $('#username').text().trim();
    var datatable = $('#mgmt-datatable').dataTable();
    var selectedTrs = datatable.$('tr.row_selected');
    var selectedRows = selectedTrs.length;
    var selectedRowIDs = "";
    if (selectedRows > 0) {
        for(var i = 0; i < selectedRows; i++) {
            var position = datatable.fnGetPosition(selectedTrs[i]);
            var selectedRowID = datatable.fnGetData(position)['id'];
            if(current_username === datatable.fnGetData(position)['username']) {
                pop_msg('user-msg', commonLanguge['You cannot delete yourself'], MSG_ALERT); // Alert
                return;
            }
            selectedRowIDs = selectedRowIDs + selectedRowID + ',';
        }
        // console.log(selectedRowIDs.substring(0, selectedRowIDs.length - 1));
        $.ajax({
            "dataType": 'json',
            "type": "DELETE",
            "url": '/admin/delete-user/' + selectedRowIDs.substring(0, selectedRowIDs.length - 1),
            "success": function(result) {
                pop_msg('user-msg', commonLanguge['Remove user successful'], MSG_SUCCESS); // Success
            }
        });
        remove_selected_rows(datatable);
    }
}

/**
 * Save as user
 *
 */
function save_as_user(row) {
    var datatable = $('#mgmt-datatable').dataTable();
    var selectedRows = datatable.$('tr.row_selected').length;

    var selected_row = datatable.$('tr.row_selected')[0];
    if(typeof(row) !== 'undefined') {
        selected_row = row;
        selectedRows = 1;
    }

    if (selectedRows === 0) {
        pop_msg('user-msg', commonLanguge['Select one user'], MSG_ALERT);  // Alert
    } else if (selectedRows === 1) {
        var position = datatable.fnGetPosition(selected_row);
        var selectedRowID = datatable.fnGetData(position)['id'];
        var fetchUser = $.ajax({
            "dataType": 'json',
            "type": "GET",
            "url": '/admin/fetch-user/' + selectedRowID
        });
        fetchUser.done(function(result) {
            // Reset as create user modal
            reset_user_create_modal();
            // Role select
            render_role_select(result.role);
            // Resource select
            render_resource_select(result.role, convert_resource(result.resource));
        });
        $('#user-new-modal').modal('show');
        $('#user-msg-container').hide();
        $('#user-modal-msg-container').hide();
    } else {
        pop_msg('user-msg', commonLanguge['Selected more than one user'], MSG_ALERT);  // Alert
    }
}

function prepare_edit_user_modal() {

    // Reset parsley
    $('#new-modal').parsley().reset();

    // Reset title/button
    $('#title').text(commonLanguge['Modify User']);
    $('#save').text(commonLanguge['Save']);

    // Reset password
    $('#password').hide();
    $('#reset-password-container').show();

    $('#user-new-modal').modal('show');
    $('#user-msg-container').hide();
    $('#user-modal-msg-container').hide();
}

/**
 * Edit user
 *
 */
function edit_user(row) {
    var datatable = $('#mgmt-datatable').dataTable();
    var selectedRows = datatable.$('tr.row_selected').length;

    var selected_row = datatable.$('tr.row_selected')[0];
    if(typeof(row) !== 'undefined') {
        selected_row = row;
        selectedRows = 1;
    }

    if (selectedRows === 0) {
        pop_msg('user-msg', commonLanguge['Select one user'], MSG_ALERT);  // Alert
    } else if (selectedRows === 1) {
        var position = datatable.fnGetPosition(selected_row);
        var selectedRowID = datatable.fnGetData(position)['id'];
        var fetchUser = $.ajax({
            "dataType": 'json',
            "type": "GET",
            "url": '/admin/fetch-user/' + selectedRowID
        });
        fetchUser.done(function(result) {
                $('#uid').val(result.id);
                $('#uname').val(result.username);
                $('#name').val(result.username);
                $('#password').val('admin');//result.password);
                $('#company').val(result.company);
                $('#email').val(result.email);
                $('#mobile').val(result.mobile);
                $('#notes').val(result.notes);
                // Role select
                render_role_select(result.role);
                // Resource select
                render_resource_select(result.role, convert_resource(result.resource));
                // Active switch
                render_active_switch(result.active);
        });
        prepare_edit_user_modal();
    } else {
        pop_msg('user-msg', commonLanguge['Selected more than one user'], MSG_ALERT);  // Alert
    }
}

/**
 * Add/Edit user
 *
 */
function save_user() {
    // Prepare user data from UI
    var uid = $('#uid').val().trim();
    var username = $('#name').val().trim();
    var password = $('#password').val().trim();
    var email = $('#email').val().trim();

    var resource_ids = "";
    var role_id = $('#role').val().trim();
    if(role_id === USER_TYPE_RESOURCE_OWNER) {
        var selected_resources = $('#resource').val();
        if(selected_resources) {
            for (var i = 0; i < selected_resources.length; i++) {
                resource_ids = resource_ids + selected_resources[i] + ",";
            }
            resource_ids = resource_ids.substring(0, resource_ids.length - 1);
        } else {
            resource_ids = "";
        }
    }

    // Assemble user
    var user = {json: {
        id: uid,
        username: username,
        password: password,
        email: email,
        company: $('#company').val().trim(),
        mobile: $('#mobile').val().trim(),
        active: ($('.switch-on') && $('.switch-on').length > 0) ? 1 : 0,
        notes: $('#notes').val().trim(),
        resource: resource_ids,
        role: role_id
    }};

    // Modify user
    if($('#uid').val().trim()) {
        $.ajax({
            dataType: 'json',
            data: JSON.stringify(user),
            contentType: "application/json",
            type: "POST",
            url: '/admin/update-user',
            success: function(result) {
                if(result.id) {
                    render_user_datatable();
                    $('#user-new-modal').modal('hide');
                } else {
                    pop_msg('user-modal-msg', result, MSG_ERROR); // Error
                }
            }
        });
    }
    // Create user
    else {
        $.ajax({
            dataType: 'json',
            data: JSON.stringify(user),
            contentType: "application/json",
            type: "POST",
            url: '/admin/create-user',
            success: function(result) {
                if(result.username) {
                    render_user_datatable();
                    $('#user-new-modal').modal('hide');
                } else {
                    pop_msg('user-modal-msg', result, MSG_ERROR); // Error
                }
            }
        });
    }
}

// Reset password
function reset_password() {
    $('#processing').show();
    var username = $('#name').val().trim();
    var email = $('#email').val().trim();

    var user_info = {json: {
        username: username,
        email: email
    }};

    var reset_password_request = $.ajax({
        dataType: 'json',
        contentType: "application/json",
        url: '/admin/reset-password',
        data: JSON.stringify(user_info),
        type: 'POST'
    });

    reset_password_request.done(function (resp) {
        var result = JSON.parse(resp);
        if (result.is_success) {
            pop_msg('user-modal-msg', result.msg, MSG_SUCCESS);
        } else {
            pop_msg('user-modal-msg', result.msg, MSG_ALERT);
        }
        $('#processing').hide();
    });
}


/**
 * Render user datatable
 *
 */
function render_user_datatable() {
    // Ready common datatable.
    ready_common_datatable(OBJ_USER, "/admin/users", 0, function(datatable) {
        off_user_click_event();

        // Call Add modal
        $("#add").on('click', function(e) {
            reset_user_create_modal();
            $('#user-new-modal').modal('show');
            $('#user-msg-container').hide();
            $('#user-modal-msg-container').hide();
        });

        // Edit by click edit link & row double click
        $("#edit").on('click', function(e) {
            if (e) e.preventDefault();
            edit_user();
        });
        datatable.on("dblclick", "tr", function(e) {
            if (e) e.preventDefault();
            edit_user(this);
        });

        // Delete users
        $("#delete").on('click', function(e) {
            if (e) e.preventDefault();
            delete_user();
        });

        // Create new user
        $("#save").on('click', function(e) {
            if (e) e.preventDefault();
            if ($('#new-modal').parsley().validate()) {
                save_user();
            }
        });

        // Reset password
        $("#reset-password").on('click', function (e) {
            if (e) e.preventDefault();
            reset_password();
        });

        // Save as new user
        $("#save-as").on('click', function(e) {
            if (e) e.preventDefault();
            save_as_user();
        });
    });
}

/**
 * Document ready js for user management page.
 *
 */
function ready_user_mgmt() {
    // Read select2
    ready_common_select2();
    render_role_select(USER_TYPE_RESOURCE);

    // Ready multi-select
    ready_common_searchable_multi_select();

    // Ready switch
    ready_common_switch();

    // Role > Resource Owner > Resource select
    $('#role').change(function() {
        render_resource_select($(this).children('option:selected').val());
    });

    // Render User datatable
    render_user_datatable();
}

/**
 * Render resource type select component
 *
 */
function render_resource_type_select(type) {
    $('#r_type').select2("val", type);
}

/**
 * Edit resource
 *
 */
function edit_resource(row) {
    var datatable = $('#mgmt-datatable').dataTable();
    var position = datatable.fnGetPosition(row);

    var selected_row_id = datatable.fnGetData(position)['id'];

    var fetch_source = $.ajax({
        "dataType": 'json',
        "type": "GET",
        "url": '/admin/fetch-resource/' + selected_row_id
    });
    fetch_source.done(function(result) {
        if(result.length === 1) {
            $('#rid').val(result[0].id);
            $('#r_vendor_2').text('');
            $('#r_url_2').attr('href', '').attr('title', '').hide();
        } else if(result.length === 2) {
            $('#rid').val(result[0].id + ":" + result[1].id);
            $('#r_vendor_2').text(convert_vendor_name(result[1].vendor));
            $('#r_url_2').attr('href', result[1].url).attr('title', result[1].url).show();
        }

        $('#r_desc').val(result[0].description);
        $('#r_name').text(result[0].name);
        $('#r_vendor_1').text(convert_vendor_name(result[0].vendor));

        $('#r_url_1').attr('href', result[0].url).attr('title', result[0].url);

        render_resource_type_select(result[0].type);
        render_active_switch(result[0].active);

        $('#resource-status-modal').modal('show');
    });
}

/**
 * Update resource type and active
 *
 */
function update_resource() {
    // Prepare resource data from UI
    var rid = $('#rid').val().trim();
    var r_desc = $('#r_desc').val().trim();
    var r_type = $('#r_type').val().trim();

    // Assemble resource
    var resource = {json: {
        id: rid,
        desc: r_desc,
        type: r_type,
        active: ($('.switch-on') && $('.switch-on').length > 0) ? 1 : 0
    }};

    // Update resource
    $.ajax({
        dataType: 'json',
        data: JSON.stringify(resource),
        contentType: "application/json",
        type: "POST",
        url: '/admin/update-resource',
        success: function(result) {
            if(result.length > 0 && result[0].id) {
                render_resource_datatable();
                $('#resource-status-modal').modal('hide');
            } else {
                pop_msg('resource-msg', result, MSG_ERROR); // Error
            }
        }
    });
}

/**
 * Render resource datatable
 *
 */
function render_resource_datatable() {
    // Ready common datatable.
    // Parameter 4 is for sorting index
    ready_common_datatable(OBJ_RESOURCE, "/admin/resources", 4, function(datatable) {
        // Edit by click row double click
        datatable.on("dblclick", "tr", function(e) {
            if (e) e.preventDefault();
            edit_resource(this);
        });

        $("#update").off('click');

        // Update resource
        $("#update").on('click', function(e) {
            if (e) e.preventDefault();
            if ($('#status-modal').parsley().validate()) {
                update_resource();
            }
        });
    });
}

/**
 * Document ready js for resource management page.
 *
 */
function ready_resource_mgmt() {
    // Read select2
    ready_common_select2();
    // Ready switch
    ready_common_switch();
    // Ready resource datatable
    render_resource_datatable();
}

/**
 * Document ready for optimized pages.
 *
 */
function ready_optimized_page(uri) {

    ready_navigation_menu();

    ready_common_i18n_info();

    switch (uri) {
    case "/admin/user-mgmt":
        ready_user_mgmt();
        break;
    case "/admin/resource-mgmt":
        ready_resource_mgmt();
        break;
    }
}


/**
 *
 * Main document ready
 *
 */
$(document).ready(function() {

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

    var url = window.location.pathname;
    if(url === "/admin/login") {
        ready_login_page();
    } else {
        // Handle menu click event.
        $('ul.cl-vnavigation li').each(function(index, li) {
            $(li).click(function(e) {
                var sub_menus = $(li).find('ul');
                if (sub_menus.length > 0) {
                    return;
                }
                var parent = $('#main-content');
                var loading = $('<div id="loading" class="loading"><i class="fa fa-spinner"></i></div>');
                loading.appendTo(parent);
                loading.fadeIn(0);
                var $clink = li.children[0];
                window.location.href = $clink;
                $('ul.cl-vnavigation li.active').removeClass('active');
                $(li).addClass('active');
            });
        });
        ready_optimized_page(url);
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