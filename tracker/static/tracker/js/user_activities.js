/*
AJAX for updating the User-Profile page quickly.
*/

$(document).ready(function () {

    var i = 1;
    // var link = 'http://127.0.0.1:8000/tracker/set_detail_rest/bf7cbf7f1405478790a29ef55e50d35f''
    var link = 'http://127.0.0.1:8000/tracker/set_detail_rest/'
    link = link + active_set

    function loop() {
        setTimeout(function () {
            $.ajax({
                type: 'GET',
                url: link,
                success: function(response_set) {
                    $('#exercise_name').text("Active Workout: " + ex_name.toString());
                    $('#weight').text(response_set.weight.toString());
                    $('#repetitions').text(response_set.repetitions.toString());
                }
            });
            i ++;
            if(ex_name == "") {
                $('#active_set_div').hide();
            } else {
                $('#active_set_div').show();
            }
            if(true) {
                loop();
            };
        }, 1000)
    };

    loop();

});