(function() {
    $('#test').bind('click', function() {
        $.getJSON('/run',
            function(data) {
                value = document.getElementById("msg").value
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