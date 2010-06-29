$(function() {
    var options = {
        target:        '#update_target',
        beforeSubmit:  on_before_submit,
        success:       on_success
    };

    $('FORM').ajaxForm(options);
});

function on_before_submit(formData, jqForm, options) {
    return true;
}

function on_success(responseText, statusText, xhr, $form)  {
    DateTimeShortcuts.init();
}
