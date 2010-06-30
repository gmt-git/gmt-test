$(function() {
    var options = {
        target:        '#update_target',
        beforeSubmit:  on_before_submit,
        success:       on_success,
        error:         on_error,
        complete:      on_complete
    };

    $('FORM').ajaxForm(options);
});

function on_before_submit(formData, jqForm, options) {
    $('.vDateField+span').remove();
    $('FORM *').attr('disabled', 'disabled');

    $('#formindicator').html('Форма відправлена');
    return true;
}

function on_success() {
    $('#formindicator').html('');
}

function on_error(xhr, statusText)  {
    $('#formindicator').html('Помилка відправки');
}

function on_complete(xhr, statusText)  {
    $('FORM *').removeAttr('disabled');
    DateTimeShortcuts.init();
}
