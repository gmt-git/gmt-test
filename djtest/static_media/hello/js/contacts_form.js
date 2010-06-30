$(function() {
    var options = {
        target:        '#update_target',
        beforeSubmit:  on_before_submit,
        success:       on_success
    };

    $('FORM').ajaxForm(options);
});

function on_before_submit(formData, jqForm, options) {
    $('.vDateField+span').remove();
    $('FORM *').attr('disabled', 'disabled');
    return true;
}

function on_success(responseText, statusText, xhr, $form)  {
    $('FORM *').removeAttr('disabled');
    DateTimeShortcuts.init();
}
