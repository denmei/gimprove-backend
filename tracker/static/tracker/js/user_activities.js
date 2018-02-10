/*
AJAX for updating the User-Profile page quickly.
*/

$(document).ready(function () {

    var i = 1;
    var link_set_detail = 'http://127.0.0.1:8000/tracker/set_detail_rest/'
    var link_userprofile_detail = 'http://127.0.0.1:8000/tracker/userprofile_detail_rest/'
    link_userprofile_detail = link_userprofile_detail + user_id
    var active = true

    function loop() {
        setTimeout(function () {
            // check whether there is an active set. If so, show set data.
            $.ajax({
                type: 'GET',
                url: link_userprofile_detail,
                success: function(response_set) {
                    if(response_set.active_set) {
                        // has active set:
                        if(active == false) {
                            $('#active_set_div').show();
                            active = true;
                        };
                        // if active set, get data and update

                        $.ajax({
                            type: 'GET',
                            url: link_set_detail + response_set.active_set,
                            success: function(response_set) {
                                $('#exercise_name').text("Active Workout: " + ex_name.toString());
                                $('#weight').text(response_set.weight.toString());
                                $('#repetitions').text(response_set.repetitions.toString());
                            }
                        });

                    } else {
                    // no active set:
                        if(active == true) {
                            $('#active_set_div').hide();
                            active = false;
                        };
                    }
                }
            });

            i ++;

            if(true) {
                loop();
            };
        }, 1000)
    };

    loop();

});