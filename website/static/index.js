(function() {
    $('#test').bind('click', function() {
        $.getJSON('/run',
            function(data) {
                // Do nothing
            });
        return false;
    });
});

function validate(name) {
    if(name.length >= 2){
        return true;
    }
    return false;
}