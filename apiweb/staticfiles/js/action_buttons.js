(function ($) {

    function fix_actions() {
        var container = $('div.actions');

        if (container.find('option').length < 10) {
            container.find('label, button').hide();

            var buttons = $('<div></div>')
                .prependTo(container)
                .css('display', 'inline')
                .addClass('class', 'action-buttons');

            container.find('option:gt(0)').each(function () {
                $('<button>')
                .appendTo(buttons)
                .attr('name', this.value)
                .addClass('button')
                .text(this.text)
                .click(function () {
                    container.find('select')
                    .find(':selected').attr('selected', '').end()
                    .find('[value=' + this.name + ']').attr('selected', 'selected');
                $('#changelist-form button[name="index"]').click();
                });
            });
        }
    };

    $(function () {
        fix_actions();
    });
})(django.jQuery);
