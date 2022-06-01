$(function() {
    $('#sendBtn').bind('click', function() {
        var msg = document.getElementById("msg")
        var value = msg.value
        msg.value = ""
        $.getJSON('/send_message',
            {val:value},
            function(data) {

        });
    });
});


window.onload = function(){
// window.addEventListener("load", function(){
    var update_loop = this.setInterval(update, 100);
    update()
};

function update(){
    fetch('/get_messages')
            .then(function (response) {
                return response.json();
            }).then(function (text) {
                for (value of text["messages"]){
                    document.write(value +"<br >");
                }
        });
};