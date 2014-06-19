var editor; // use a global for the submit and return data rendering in the examples

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
 *
 * Document ready for optimized pages.
 * TODO: Add details pages & dynamic menu handling.
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
 */
function ready_navigation_menu() {
    // Handle menu click event.
    $('ul.cl-vnavigation li').each(function(index, li) {
        var sub_menus = $(li).find('ul');
        //if (sub_menus.length > 0) {
        //    return;
        //}
        var $clink = li.children[0];
        if ($clink.href == String(window.location)) {
            $(this).addClass('active');
        }
    });
}

/**
 * Document ready js for user management page.
 */
function ready_user_mgmt() {
    // Read select2
    ready_common_select2();
    render_role_select();

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
        });

        // Edit by click edit link & row double click
        $("#edit").click(function(e) {
            e.preventDefault();
            edit_user();
        });
        datatable.on("dblclick", "tr", function(e) {
            e.preventDefault();
            edit_user(this);
        });

        // Delete users
        $("#delete").click(function(e) {
            e.preventDefault();
            delete_user();
        });

        // Create new user
        $("#save").click(function(e) {
            e.preventDefault();
            save_user();
        });
    });
}

function delete_user() {
    var datatable = $('#mgmt-datatable').dataTable();
    var selectedTrs = datatable.$('tr.row_selected');
    var selectedRows = selectedTrs.length;
    if (selectedRows > 0) {
        for(i = 0; i < selectedRows; i++) {
            var position = datatable.fnGetPosition(selectedTrs[i]);
            var selectedRowID = datatable.fnGetData(position)['id'];
            $.ajax({
                "dataType": 'json',
                "type": "DELETE",
                "url": '/admin/delete-user/' + selectedRowID,
                "success": function(result) {
                    console.log(">>>>>>>>>>>>delete" + selectedRowID + "successfully");
                }
            });
        }
        remove_selected_rows(datatable);
    }
}

function edit_user(row) {
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
        alert("Select one object to view!");
    } else if (selectedRows === 1) {
        var position = datatable.fnGetPosition(selected_row);
        var selectedRowID = datatable.fnGetData(position)['id'];
        $.ajax({
            "dataType": 'json',
            "type": "GET",
            "url": '/admin/fetch-user/' + selectedRowID,
            "success": function(result) {
                $('#uid').val(result.id);
                $('#name').val(result.username);
                $('#password').val(result.password);
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
            }
        });
        $('#user-new-modal').modal('show');
    } else {
        alert("Selected more than one object!");
    }
}

function save_user() {
    // Prepare user data from UI
    var resource_ids = "";
    var role_id = $('#role').val().trim();
    if(role_id === '2') {
        var selected_resources = $('#resource').val();
        for(var i = 0; i < selected_resources.length; i++) {
            resource_ids = resource_ids + selected_resources[i] + ",";
        }
        resource_ids = resource_ids.substring(0, resource_ids.length - 1);
    }

    var user = {
        id: $('#uid').val().trim(),
        username: $('#name').val().trim(),
        password: $('#password').val().trim(),
        company: $('#company').val().trim(),
        mobile: $('#mobile').val().trim(),
        email: $('#email').val().trim(),
        active: ($('.switch-on') && $('.switch-on').length > 0) ? 1 : 0,
        notes: $('#notes').val().trim(),
        resource: resource_ids,
        role: role_id
    };

    // Add
    if($('#uid').val().trim()) {
        $.ajax({
            dataType: 'json',
            data: JSON.stringify(user),
            contentType: "application/json",
            type: "POST",
            url: '/admin/update-user',
            success: function(result) {
                console.log(result);
                render_user_datatable();
            }
        });
    } else {
        $.ajax({
            dataType: 'json',
            data: JSON.stringify(user),
            contentType: "application/json",
            type: "POST",
            url: '/admin/create-user',
            success: function(result) {
                console.log(result);
                render_user_datatable();
            }
        });
    }
}

function reset_user_create_modal() {
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
    render_role_select();

    // Resource select
    render_resource_select();
}

function render_active_switch(is_active) {
    var _switch = $('.switch-animate');
    if(typeof(is_active) !== 'undefined') {
        if(is_active === 'true') {
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

function render_role_select(selectedRole="1") {
    $('#role').select2("val", convert_role_to_id(selectedRole));
}

function convert_role_to_id(role) {
    var role_id = 1;
    if(role === 'Resource')
        role_id = 1;
    else if(role === 'Resource Owner')
        role_id = 2;
    else if(role === 'Administrator')
        role_id = 3;
    return role_id;
}

function convert_resource(resource_str) {
    if(resource_str === "")
        return [];
    else {
        return resource_str.split(",");
    }
}

function render_resource_select(selectedRole="1", selectedResources) {
    if(selectedRole === '2' || selectedRole === 'Resource Owner') { // 'Resource Owner'
        // Populate resource select
        $.ajax({
            "dataType": 'json',
            "type": "GET",
            "url": "/admin/resources",
            "success": function(result) {
                // console.log(result);
                for(var i = 0; i < result.length; i++) {
                    $('#resource').multiSelect('addOption', {value: result[i].id, text: result[i].name + "[" + result[i].vendor + "]", index: i });
                }
            }
        });
        $('#resource').multiSelect('refresh');
        if(typeof(selectedResources) !== 'undefined') {
            $('#resource').multiSelect('select', selectedResources);
        }
        $('#resource-container').show();
    } else {
        $('#resource-container').hide();
    }
}

/**
 * Document ready js for resource management page.
 * TODO: Integrate with new datatable fw.
 */
function ready_resource_mgmt() {
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
    ready_common_datatable("/admin/resources", columns, function(datatable) {});

    /*
    editor = new $.fn.dataTable.Editor( {
        ajax: "/admin/resources",
        table: "#mgmt-datatable",
        fields: [ {
                label: "ID",
                name: "id"
            }, {
                label: "Resource Name",
                name: "name"
            }, {
                label: "Vendor",
                name: "vendor"
            }, {
                label: "Upload Date",
                name: "upload_date"
            }, {
                label: "Status",
                name: "status"
            }, {
                label: "Type",
                name: "type"
            }, {
                label: "Active",
                name: "active"
            }
        ]
    } );

    editor.on( 'onOpen', function () {
            // Listen for a tab key event
            $(document).on( 'keydown.editor', function ( e ) {
                if ( e.keyCode === 9 ) {
                    e.preventDefault();

                    // Find the cell that is currently being edited
                    var cell = $('div.DTE').parent();

                    if ( e.shiftKey && cell.prev().length && cell.prev().index() !== 0 ) {
                        // One cell to the left (skipping the first column)
                        cell.prev().click();
                    }
                    else if ( e.shiftKey ) {
                        // Up to the previous row
                        cell.parent().prev().children().last(0).click();
                    }
                    else if ( cell.next().length ) {
                        // One cell to the right
                        cell.next().click();
                    }
                    else {
                        // Down to the next row
                        cell.parent().next().children().eq(1).click();
                    }
                }
            } );
        } ).on( 'onClose', function () {
            $(document).off( 'keydown.editor' );
        } );

    $('#resourcestable').on( 'click', 'tbody td:not(:first-child)', function (e) {
        editor.inline( this, {
            submitOnBlur: true
        } );
    } );

    $('#resourcestable').DataTable( {
        dom: "Tfrtip",
        ajax: "/admin/resources",
        columns: [
            { data: "id" },
            { data: "name" },
            { data: "vendor" },
            { data: "upload_date" },
            { data: "status" },
            { data: "type" },
            { data: "active" }
        ],
        order: [ 1, 'asc' ],
        tableTools: {
            sRowSelect: "os",
            sRowSelector: 'td:first-child',
            aButtons: [
                { sExtends: "editor_create", editor: editor },
                { sExtends: "editor_edit",   editor: editor },
                { sExtends: "editor_remove", editor: editor }
            ]
        }
    } );
    */
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
 * Common ready for switch.
 *
 */
function ready_common_multi_select_group() {
    /*Multi-Select Group*/
    $('.privilegeMultiSelect').multiSelect({
        selectableOptgroup: true
    });
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
 * @param datatable identifier
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
                "aaData": result,
                "aoColumns": columns
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

function authenticate() {
    if ($('#security-login-form').parsley().validate()) {
        var username = $('#username').val();
        var password = $('#password').val();
        eventBus.trigger('security:show-loading');
        authenticationProvider.authenticate({
            username: username,
            password: password
        });
    } else {
        console.log('Client side validate error.');
    }
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
