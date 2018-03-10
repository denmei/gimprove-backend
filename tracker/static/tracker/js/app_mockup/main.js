/*
AJAX for updating the User-Profile page quickly.
*/

$(document).ready(function () {

    var i = 1;
    // TODO: change when deploying to heroku
    //var link_set_detail = 'https://app-smartgym.herokuapp.com/tracker/set_detail_rest/';
    // var link_userprofile_detail = 'https://app-smartgym.herokuapp.com/tracker/userprofile_detail_rest/';
    var link_set_detail = 'http://127.0.0.1:8000/tracker/set_detail_rest/';
    var link_userprofile_detail = 'http://127.0.0.1:8000/tracker/userprofile_detail_rest/';
    link_userprofile_detail = link_userprofile_detail + user_id;
    var active = false;

    function loop() {
        setTimeout(function () {
            console.log(link_userprofile_detail)
            // check whether there is an active set. If so, show set data.
            $.ajax({
                type: 'GET',
                url: link_userprofile_detail,
                success: function(response_set) {
                    console.log(response_set)
                        // if active set, get data and update
                       console.log(link_set_detail + response_set._pr_active_set)
                        $.ajax({
                            type: 'GET',

                            url: link_set_detail + response_set._pr_active_set,
                            success: function(response_set) {
                                console.log(response_set.repetitions);
                                var s = "/static/tracker/pictures/app_mockup/mockup_" + response_set.repetitions + ".png"
                                $('#mockup-img').attr("src", s);
                            }
                        });

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