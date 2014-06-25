/**
 * Document ready
 *
 */
$(document).ready(function() {
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
            self.location.href = $clink;
            $('ul.cl-vnavigation li.active').removeClass('active');
            $(li).addClass('active');
        });
    });
    ready_optimized_page(window.location.pathname);
});

/**
 * Document ready for optimized pages.
 *
 */
function ready_optimized_page(uri) {

    ready_navigation_menu();

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
 * Document ready for navigation menu.
 *
 */
function ready_navigation_menu() {
    // Handle menu click event.
    $('ul.cl-vnavigation li').each(function(index, li) {
        var sub_menus = $(li).find('ul');
        var $clink = li.children[0];
        if ($clink.href == String(window.location)) {
            $(this).addClass('active');
        }
    });
}

/**
 * Document ready js for user management page.
 *
 */
function ready_user_mgmt() {
    // Read select2
    ready_common_select2();
    render_role_select("1");

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
 * Render user datatable
 *
 */
function render_user_datatable() {
    // Prepare displaying columns
    var columns = [
        {
          "sTitle": "ID",
          "mData": "id",
          "bVisible": false
        },
        {
          "sTitle": "User Name",
          "mData": "username"
        },
        {
          "sTitle": "Company",
          "mData": "company"
        },
        {
          "sTitle": "Email",
          "mData": "email"
        },
        {
          "sTitle": "Mobile",
          "mData": "mobile"
        },
        {
          "sTitle": "Role",
          "mData": "role"
        },
        {
          "sTitle": "Active",
          "mData": "active"
        }
    ];

    // Ready common datatable.
    ready_common_datatable("/admin/users", columns, function(datatable) {
        // Call Add modal
        $("#add").click(function(e) {
            reset_user_create_modal();
            $('#user-new-modal').modal('show');
            $('#user-msg-container').hide();
            $('#user-modal-msg-container').hide();
        });

        // Edit by click edit link & row double click
        $("#edit").click(function(e) {
            if (e) e.preventDefault();
            edit_user();
        });
        datatable.on("dblclick", "tr", function(e) {
            if (e) e.preventDefault();
            edit_user(this);
        });

        // Delete users
        $("#delete").click(function(e) {
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
    });
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
        for(i = 0; i < selectedRows; i++) {
            var position = datatable.fnGetPosition(selectedTrs[i]);
            var selectedRowID = datatable.fnGetData(position)['id'];
            if(current_username === datatable.fnGetData(position)['username']) {
                pop_msg('user-msg', 'You cannot delete yourself.', 1); // Alert
                return;
            }
            selectedRowIDs = selectedRowIDs + selectedRowID + ',';
        }
        console.log(selectedRowIDs.substring(0, selectedRowIDs.length - 1));
        $.ajax({
            "dataType": 'json',
            "type": "DELETE",
            "url": '/admin/delete-user/' + selectedRowIDs.substring(0, selectedRowIDs.length - 1),
            "success": function(result) {
                console.log(">>>>>>>>>>>>delete" + selectedRowIDs + "successfully");
                pop_msg('user-msg', 'Remove user(s) successfully.', 2); // Success
            }
        });
        remove_selected_rows(datatable);
    }
}

/**
 * Edit user
 *
 */
function edit_user(row) {
    // Reset parsley
    $('#new-modal').parsley().reset();

    // Reset title/button
    $('#title').text("Modify User");
    $('#save').text("Save");

    var datatable = $('#mgmt-datatable').dataTable();
    var selectedRows = datatable.$('tr.row_selected').length;

    var selected_row = datatable.$('tr.row_selected')[0];
    if(typeof(row) !== 'undefined') {
        selected_row = row;
        selectedRows = 1;
    }

    if (selectedRows === 0) {
        pop_msg('user-msg', 'Select one object to view!', 1);  // Alert
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
        $('#user-new-modal').modal('show');
        $('#user-msg-container').hide();
        $('#user-modal-msg-container').hide();
    } else {
        pop_msg('user-msg', 'Selected more than one object!', 1);  // Alert
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
    if(role_id === '2') {
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
    var user = {
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
    };

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
                    pop_msg('user-modal-msg', result, 0); // Error
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
                    pop_msg('user-modal-msg', result, 0); // Error
                }
            }
        });
    }
}

/**
 * Reset msg & components of user create modal
 *
 */
function reset_user_create_modal() {
    // Reset parsley
    $('#new-modal').parsley().reset();

    // Reset title/button
    $('#title').text("Create User");
    $('#save').text("Create");

    // Reset values here
    $('#uid').val("");
    $('#name').val("");
    $('#password').val("");
    $('#company').val("");
    $('#email').val("");
    $('#mobile').val("");
    $('#notes').val("");

    // Active switch
    render_active_switch();

    // Role select
    render_role_select("1");

    // Resource select
    render_resource_select();
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

/**
 * Convert resource string ids to array
 *
 */
function convert_resource(resource_str) {
    if(resource_str === "")
        return [];
    else {
        return resource_str.split(",");
    }
}

/**
 * Render resource select component
 *
 */
function render_resource_select(selectedRole, selectedResources) {
    if(selectedRole === '2' || selectedRole === 'Resource Owner') { // 'Resource Owner'
        // Populate resource select
        var resource_list = $.ajax({
            "dataType": 'json',
            "type": "GET",
            "url": "/admin/resources"
        });

        resource_list.done(function(result) {
            // console.log(result);
            $('#resource').multiSelect('refresh');
            for (var i = 0; i < result.length; i++) {
                $('#resource').multiSelect('addOption', {value: result[i].id, text: result[i].name + "[" + result[i].vendor + "]", index: i });
            }
            $('#resource').multiSelect('deselect_all');
            if (typeof(selectedResources) !== 'undefined') {
                $('#resource').multiSelect('select', selectedResources);
            }
            $('#resource-container').show();
        });
    } else {
        $('#resource-container').hide();
    }
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

    render_resource_datatable();
}

/**
 * Render resource datatable
 *
 */
function render_resource_datatable() {
    var columns = [
        {
          "sTitle": "ID",
          "mData": "id",
          "bVisible": false
        },
        {
          "sTitle": "Resource Name",
          "mData": "name"
        },
        {
          "sTitle": "Vendor",
          "mData": "vendor"
        },
        {
          "sTitle": "Uploaded Date",
          "mData": "uploaded_date"
        },
        {
          "sTitle": "Status",
          "mData": "status"
        },
        {
          "sTitle": "Type",
          "mData": "type"
        },
        {
          "sTitle": "Active",
          "mData": "active"
        }
    ];

    // Ready common datatable.
    ready_common_datatable("/admin/resources", columns, function(datatable) {
        // Edit by click row double click
        datatable.on("dblclick", "tr", function(e) {
            if (e) e.preventDefault();
            edit_resource(this);
        });

        // Update resource
        $("#update").on('click', function(e) {
            if (e) e.preventDefault();
            update_resource();
        });
    });
}

/**
 * Update resource type and active
 *
 */
function update_resource() {
    // Prepare resource data from UI
    var rid = $('#rid').val().trim();
    var r_type = $('#r_type').val().trim();

    // Assemble resource
    var resource = {
        id: rid,
        type: r_type,
        active: ($('.switch-on') && $('.switch-on').length > 0) ? 1 : 0
    };

    // Update resource
    $.ajax({
        dataType: 'json',
        data: JSON.stringify(resource),
        contentType: "application/json",
        type: "POST",
        url: '/admin/update-resource',
        success: function(result) {
            if(result.id) {
                render_resource_datatable();
                $('#resource-status-modal').modal('hide');
            } else {
                pop_msg('resource-msg', result, 0); // Error
            }
        }
    });
}

/**
 * Edit resource
 *
 */
function edit_resource(row) {
    var datatable = $('#mgmt-datatable').dataTable();
    var position = datatable.fnGetPosition(row);

    $('#rid').val(datatable.fnGetData(position)['id']);
    $('#r_name').text(datatable.fnGetData(position)['name']);
    $('#r_vendor').text(datatable.fnGetData(position)['vendor']);

    var type = datatable.fnGetData(position)['type'] === 'Restricted' ? '2' : '1';
    var active = datatable.fnGetData(position)['active'] === 'Yes' ? true : false;

    render_resource_type_select(type);
    render_active_switch(active);

    $('#resource-status-modal').modal('show');
}

/**
 * Render resource type select component
 *
 */
function render_resource_type_select(type) {
    $('#r_type').select2("val", type);
}

//***************************************************************
//
//              COMMON UI COMPONENTS
//
//***************************************************************
/**
 * Common ready for select2.
 *
 */
function ready_common_select2() {
    /*Select2*/
    $(".select2").select2({
        width: '100%'
    });
}

/**
 * Common ready for switch.
 *
 */
function ready_common_switch() {
    /*Switch*/
    $('.switch').bootstrapSwitch();
}

/**
 * Common ready for searchable multi select.
 *
 */
function ready_common_searchable_multi_select() {
    /*Multi-Select Search*/
    $('.searchable').multiSelect({
        selectableHeader: "<input type='text' class='form-control search-input' autocomplete='off' placeholder='Filter String'>",
        selectionHeader: "<input type='text' class='form-control search-input' autocomplete='off' placeholder='Filter String'>",
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
                if (e.which == 40) {
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

/**
 * Common ready for tables.
 *
 */
function ready_common_datatable(url, columns, fnDatatableCallback) {
    $.ajax({
        "dataType": 'json',
        "type": "GET",
        "url": url,
        "success": function(result) {
            datatable_id = "mgmt-datatable";

            var datatable_div = datatable_id + '-container';
            $("#" + datatable_div).html('<table class="table table-bordered" id="' + datatable_id + '"></table>');
            var datatable_id = "#" + datatable_id;

            /* Init the table with dynamic ajax loader.*/
            var datatable = $(datatable_id).dataTable({
                "aaData": process_user_result(result),
                "aoColumns": columns,
                "columnDefs": [ {
                    "targets": -1,
                    "data": null,
                    "defaultContent": "<button>Click!</button>"
                } ]
            });

            // Add/remove class to a row when clicked on
            $(datatable_id).on('click', 'tbody tr', function(e) {
                $(this).toggleClass('row_selected');
            });

            // Search input style
            $('.dataTables_filter input').addClass('form-control').attr('placeholder', 'Search');
            $('.dataTables_length select').addClass('form-control');

            // Callback method for datatable
            fnDatatableCallback(datatable);
        }
    });
}

/**
 * Process user attributes' values to displaying values
 */
function process_user_result(result) {
    for(var i = 0; i < result.length; i++) {
        result[i].active = get_user_status(result[i].active);
        if(result[i].role) result[i].role = get_role_name(result[i].role);
        if(result[i].status) result[i].status = get_resource_status(result[i].status);
        if(result[i].type) result[i].type = get_resource_type(result[i].type);
    }
    return result;
}

function get_resource_status(status) {
    var resource_status = 'Fail';
    if(status === '1')
        resource_status = 'Successful';
    else
        resource_status = 'Fail';
    return resource_status;
}

function get_resource_type(_type) {
    var resource_type = 'Restricted';
    if(_type == '1')
        resource_type = 'Public';
    else
        resource_type = 'Restricted';
    return resource_type;
}

function get_role_name(role_id) {
    var role_name = 'Resource';
    if(role_id == '1')
        role_name = 'Resource';
    else if(role_id == '2')
        role_name = 'Resource Owner';
    else if(role_id == '3')
        role_name = 'Administrator';
    return role_name;
}

function get_user_status(active) {
    var status = 'No';
    if(active)
        status = 'Yes';
    return status;
}

//***************************************************************
//
//              COMMON JAVASCRIPT METHODS
//
//***************************************************************

function remove_selected_rows(local_table) {
    var selected_rows = local_table.$('tr.row_selected');
    selected_rows.each(function(index, row) {
        local_table.fnDeleteRow(row);
    });
}

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
