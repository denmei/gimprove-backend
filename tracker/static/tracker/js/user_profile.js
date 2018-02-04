/*
AJAX for updating the User-Profile page quickly.
*/

$(document).ready(function () {

    var i = 1;
    // var link = 'http://127.0.0.1:8000/tracker/set_detail_rest/bf7cbf7f1405478790a29ef55e50d35f''
    var link = 'http://127.0.0.1:8000/tracker/set_detail_rest/'
    link = link + prof

    function loop() {
        setTimeout(function () {
            $.ajax({
                type: 'GET',
                url: link,
                success: function(response_set) {
                    $('#exercise_name').text(ex_name);
                    $('#weight').text("Gewicht: " + response_set.weight.toString());
                    $('#repetitions').text("Wiederholungen: " + response_set.repetitions.toString());
                }
            });
            i ++;
            if(true) {
                loop();
            };
        }, 500)
    };

    loop();

});