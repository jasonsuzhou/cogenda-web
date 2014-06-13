$(document).ready(function() {
    // Handle menu click event.
    $('ul.cl-vnavigation li').each(function(index, li) {
        $(li).click(function(e) {
            var sub_menus = $(li).find('ul');
            if (sub_menus.length > 0) {
                return;
            }
            e.preventDefault();
            var parent = $('#main-content');
            var loading = $('<div id="loading" class="loading"><i class="fa fa-spinner"></i></div>');
            loading.appendTo(parent);
            loading.fadeIn(0);
            var $clink = li.children[0];
            History.pushState({
                state: 1,
                rand: Math.random()
            }, null, $clink.href);
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
    var columns = [
        {
          "sTitle": "ID",
          "mData": "id"
        },
        {
          "sTitle": "Name",
          "mData": "username"
        },
        {
          "sTitle": "Email",
          "mData": "email"
        },
        {
          "sTitle": "Active",
          "mData": "active"
        }
    ];

    // Ready common datatable.
    ready_common_datatable("user-mgmt-datatable", "/admin/user-mgmt-data", columns, function(datatable) {
        // Add new user in datatable.
        $("#user-mgmt-proceed").click(function(e) {
            datatable.fnAddData(["Trident-new", "Internet Explorer 4.0", "Win 95+", "4", "X"]);
        });

        // Delete user in datatable.
        $("#user-mgmt-delete").click(function(e) {
            e.preventDefault();
            fnRemoveSelected(datatable);
        });
    });
}

/**
 * Document ready js for resource management page.
 * TODO: Integrate with new datatable fw.
 */
function ready_resource_mgmt() {
    // Ready common datatable.
    ready_common_datatable('resource-mgmt-datatable', "/admin/resource-mgmt-data", function(datatable) {

        // Add new resource in datatable.
        $("#resource-mgmt-proceed").click(function(e) {
            datatable.fnAddData(["Trident-new", "Internet Explorer 4.0", "Win 95+", "4", "X"]);
        });

        // Delete resource in datatable.
        $("#resource-mgmt-delete").click(function(e) {
            e.preventDefault();
            fnRemoveSelected(datatable);
        });
    });
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
function ready_common_datatable(datatable_id, url, columns, fnDatatableCallback) {
    //var _columns = columns;
    $.ajax({
        "dataType": 'json',
        "type": "GET",
        "url": url,
        "success": function(result) {
            console.log(result);

            var data = [
                    {
                        "username": "Tim",
                        "email": "tang.jilong@gmail.com",
                        "active": true,
                        "password": "123",
                        "id": 1
                    },
                    {
                        "username": "Tim",
                        "email": "tang.jilong@gmail.com",
                        "active": true,
                        "password": "123",
                        "id": 2
                    }
            ]

            $('.table-responsive').html('<table class="table table-bordered" id="' + datatable_id + '"></table>');
            var datatable_id = "#" + datatable_id;

            /* Init the table with dynamic ajax loader.*/
            var datatable = $(datatable_id).dataTable({
                "aaData": data,
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