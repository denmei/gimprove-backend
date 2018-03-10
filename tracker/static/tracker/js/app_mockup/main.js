/*
AJAX for updating the User-Profile page quickly.
*/

$(document).ready(function () {

    var i = 1;
    // TODO: change when deploying to heroku
    // var link_set_detail = 'https://app-smartgym.herokuapp.com/tracker/set_detail_rest/a8c1c41ace8246e282e0a6788ce51c48';
    var link_set_detail = 'http://127.0.0.1:8000/tracker/set_detail_rest/';

    function loop() {
        setTimeout(function () {
            // check whether there is an active set. If so, show set data.
                //get data and update
                $.ajax({
                    type: 'GET',
                    url: link_set_detail,
                    success: function(response_set) {
                        var s = "./img/mockup_" + response_set.repetitions + ".png";
                        console.log(s);
                        $('#mockup-img').attr("src", s);
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
