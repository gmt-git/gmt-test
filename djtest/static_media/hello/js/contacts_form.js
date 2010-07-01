$(function() {
    var options = {
        target:        '#update_target',
        beforeSubmit:  on_before_submit,
        success:       on_success,
        error:         on_error,
        complete:      on_complete
    };

    $('form').ajaxForm(options);
    $('form input').removeAttr('disabled'); // ящко цього нема, то у FF після оновлення
                                            // сторінки поля форми disabled
                                            // (якщо оновлювати без shift
    Date.firstDayOfWeek = 1;
    Date.format = 'yyyy-mm-dd';
    $('.date-pick').datePicker({startDate:'1900-01-01'});
});

function on_before_submit(formData, jqForm, options) {
    $('#id_birth_date').dpSetDisabled(true);
    $('form input').attr('disabled', 'disabled');

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
    $('.date-pick').datePicker({startDate:'1900-01-01'});
    $('#id_birth_date').dpSetDisabled(false);
    $('form input').removeAttr('disabled');
}
