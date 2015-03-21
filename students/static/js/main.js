function initJournal() {
    var indicator = $('#ajax-progress-indicator');
    var message = $('#status-message');

    $('.day-box input[type="checkbox"]').click(function(event){
        var box = $(this);
        $.ajax(box.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'pk': box.data('student-id'),
                'date': box.data('date'),
                'present': box.is(':checked') ? '1': '',
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'beforeSend': function(xhr, settings){
                indicator.show();
            },
            'error': function(xhr, status, error){
                alert(error);
                indicator.hide();
                message.empty();
                message.append('Виникла помилка при спробі з’єднання з \
                                сервером. Спробуйте, будь ласка, пізніше.');
                message.addClass('alert alert-danger');

            },
            'success': function(data, status, xhr){
                setTimeout(function() {
                    indicator.hide();
                }, 350);

            }
        });
    });
}

function initGroupSelector() {
    // look up select element with groups attach our even handler
    // on field "change" event
    $('#group-selector select').change(function(event){
        // get value of currently selected group option
        var group = $(this).val();

        if (group) {
            // set cookie with expiration date 1 year since now;
            // cookie creation function takes peroid in days
            $.cookie('current_group', group, {'path': '/', 'expires': 365});
        } else {
            // otherwise we delete the cookie
            $.removeCookie('current_group', {'path': '/'});
        }

        // and reload a page
        location.reload(true);

        return true;
    });
}

function initDateFields() {
    $('input.dateinput').datetimepicker({
        'format': 'YYYY-MM-DD',
        locale: moment.lang('uk')
    }).on('dp.hide', function(event){
        $(this).blur();
    });
}

function initDateFields_1() {
    $('#datetimepicker1').datetimepicker({
        format: 'YYYY-MM-DD',
        locale: moment.lang('uk')
    });
};

$(document).ready(function() {
    initJournal();
    initGroupSelector();
    initDateFields();
    initDateFields_1();
});