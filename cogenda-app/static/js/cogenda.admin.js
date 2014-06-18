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

    // Prepare displaying columns
    var columns = [
        {
          "sTitle": "ID",
          "mData": "id"
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

    // Prepare hidden columns
    var hiddenColumns = [
        {
            "targets": [2],
            "visible": false,
            "searchable": false
        }
    ]

    // Read select2
    ready_common_select2();

    // Ready multi-select
    ready_common_searchable_multi_select();

    // Ready switch
    ready_common_switch();

    // Role > Resource Owner > Resource select
    $('#role').change(function() {
        var selectedRole = $(this).children('option:selected').val();
        if(selectedRole === '2') // 'Resource Owner'
            $('#resource-container').show();
        else
            $('#resource-container').hide();
    });

    // Ready common datatable.
    ready_common_datatable("userstable", "/admin/users", columns, hiddenColumns, function(datatable) {
        // Add new user in datatable.
        $("#add").click(function(e) {
            reset_user_create_modal();
        });

        $("#edit").click(function(e) {
            // Reset title/button
            $('#title').text("Modify User");
            $('#save').text("Save");

            var selectedRows = datatable.$('tr.row_selected').length;
            if (selectedRows === 0) {
                alert("Select one object to view!");
            } else if (selectedRows === 1) {
                var selectedRowID = datatable.$('tr.row_selected')[0].cells[0].childNodes[0].textContent;
                $.ajax({
                    "dataType": 'json',
                    "type": "GET",
                    "url": '/admin/users/' + selectedRowID,
                    "success": function(result) {
                        $('#user-new-modal #name').val(result.username);
                        $('#user-new-modal #password').val(result.password);
                        $('#user-new-modal #company').val(result.company);
                        $('#user-new-modal #email').val(result.email);
                        $('#user-new-modal #mobile').val(result.mobile);
                        //$('#user-new-modal #role').val(‘1’);
                        $('#user-new-modal #active').attr('checked', false);
                        $('#user-new-modal #notes').val(result.notes);
                    }
                });
                $('#user-new-modal').modal('show');
            } else {
                alert("Selected more than one object!");
            }
        });

        // Delete user in datatable.
        $("#delete").click(function(e) {
            e.preventDefault();

            var selectedRows = datatable.$('tr.row_selected').length;
            if (selectedRows > 0) {
                var selectedRowID = datatable.$('tr.row_selected')[0].cells[0].childNodes[0].textContent;
                $.ajax({
                    "dataType": 'json',
                    "type": "DELETE",
                    "url": '/admin/users/' + selectedRowID,
                    "success": function(result) {
                        console.log(">>>>>>>>>>>>delete successfully");
                    }
                });

                fnRemoveSelected(datatable);
            }
        });
    });

    // Create new user
    $("#save").click(function(e) {
        e.preventDefault();
        save_user();
    });
}

function save_user() {
    // Prepare user data from UI
    var user = {
        username: $('#user-new-modal #name').val().trim(),
        password: $('#user-new-modal #password').val().trim(),
        company: $('#user-new-modal #company').val().trim(),
        mobile: $('#user-new-modal #mobile').val().trim(),
        email: $('#user-new-modal #email').val().trim(),
        role: $('#user-new-modal #role').val().trim(),
        resource: $('#user-new-modal #resource').val().trim(),
        active: ($('#user-new-modal .switch-on') && $('#user-new-modal .switch-on').length > 0) ? 1 : 0,
        notes: $('#user-new-modal #notes').val().trim()
    };

    console.log(user);

    $.ajax({
        dataType: 'json',
        data: JSON.stringify(user),
        contentType: "application/json",
        type: "POST",
        url: '/admin/user/create',
        success: function(result) {
            console.log(result);
            //console.log('>>>>>>>>>success!');
        }
    });
}

function reset_user_create_modal() {
    // Reset title/button
    $('#title').text("Create User");
    $('#save').text("Create");

    // Reset values here
    $('#user-new-modal #name').val("");
    $('#user-new-modal #password').val("");
    $('#user-new-modal #company').val("");
    $('#user-new-modal #email').val("");
    $('#user-new-modal #mobile').val("");
    //$('#user-new-modal #role').val('1');
    $('#user-new-modal #active').attr('checked', false);
    $('#user-new-modal #notes').val("");
}

/**
 * Document ready js for resource management page.
 * TODO: Integrate with new datatable fw.
 */
function ready_resource_mgmt() {
    var columns = [
        {
          "sTitle": "ID",
          "mData": "id"
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
    ready_common_datatable('resource-mgmt-datatable', "/admin/resource-mgmt-data", columns, [], function(datatable) {});

    /*
    editor = new $.fn.dataTable.Editor( {
        ajax: "/admin/resource-mgmt-data",
        table: "#resource-mgmt-datatable",
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

    $('#resource-mgmt-datatable').on( 'click', 'tbody td:not(:first-child)', function (e) {
        editor.inline( this, {
            submitOnBlur: true
        } );
    } );

    $('#resource-mgmt-datatable').DataTable( {
        dom: "Tfrtip",
        ajax: "/admin/resource-mgmt-data",
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
function ready_common_datatable(datatable_id, url, columns, hiddenColumns, fnDatatableCallback) {
    $.ajax({
        "dataType": 'json',
        "type": "GET",
        "url": url,
        "success": function(result) {
            console.log(result);

            $('.table-responsive').html('<table class="table table-bordered" id="' + datatable_id + '"></table>');
            var datatable_id = "#" + datatable_id;

            /* Init the table with dynamic ajax loader.*/
            var datatable = $(datatable_id).dataTable({
                "columnDefs": hiddenColumns,
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
/*
 * I don't actually use this here, but it is provided as it might be useful and demonstrates
 * getting the TR nodes from DataTables
 */
function fnRemoveSelected(local_table) {
    var selected_rows = local_table.$('tr.row_selected');
    selected_rows.each(function(index, row) {
        local_table.fnDeleteRow(row);
    });
}
