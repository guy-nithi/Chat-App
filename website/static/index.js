$(function() {
    $('#test').bind('click', function() {
        $.getJSON('/run',
            function(data) {
                // Do nothing
            });
        return false;
    });
});