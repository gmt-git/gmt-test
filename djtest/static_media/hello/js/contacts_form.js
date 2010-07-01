$(function() {
    var options = {
        target:        '#update_target',
        beforeSubmit:  on_before_submit,
        success:       on_success,
        error:         on_error,
        complete:      on_complete
    };

    $('form').ajaxForm(options);

    calendar_init();
    $('form input').removeAttr('disabled'); // ящко цього нема, то у FF після оновлення
                                            // сторінки поля форми disabled
                                            // (якщо оновлювати без shift
});

function on_before_submit(formData, jqForm, options) {
    form_disable();
    $('#formindicator').html('Форма відправлюється');
    return true;
}

function on_success() {
    if ($('.errorlist').size() > 0) {
        $('#formindicator').html('Помилка вводу');
    }
    else {
        $('#formindicator').html('Форма відправлена');
    }
}

function on_error(xhr, statusText)  {
    $('#formindicator').html('Помилка відправки');
}

function on_complete(xhr, statusText)  {
    calendar_init();
    $('form input').removeAttr('disabled');
}

function calendar_init() {
    Date.firstDayOfWeek = 1;
    Date.format = 'yyyy-mm-dd';
    $('.date-pick').datePicker({startDate:'1900-01-01', createButton: false});
    $('.date-pick').
        after('<a href="#" class="dp-choose-date"><img src="/static_media/hello/images/btn_enabled.png" /></a>');
    $('.dp-choose-date').bind('click', function() {
        $('.date-pick').dpDisplay(this);
        return false;
    });
}

function form_disable() {
    $('.date-pick').dpSetDisabled(true);
    $('.dp-choose-date img').attr('src', '/static_media/hello/images/btn_disabled.png');
    $('form input').attr('disabled', 'disabled');
}
