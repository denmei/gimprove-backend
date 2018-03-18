
$(document).ready(function () {

    var i = 1;
    var active = false;
    var reps = 0;

    var currentLocation = window.location;

    if(currentLocation.toString().indexOf("127.0.0.1") > -1) {
        var link_set_detail = 'http://127.0.0.1:8000/tracker/set_detail_rest/';
        var link_userprofile_detail = 'http://127.0.0.1:8000/tracker/userprofile_detail_rest/';
    } else {
        var link_set_detail = 'https://app-smartgym.herokuapp.com/tracker/set_detail_rest/';
        var link_userprofile_detail = 'https://app-smartgym.herokuapp.com/tracker/userprofile_detail_rest/';
    };

    link_userprofile_detail = link_userprofile_detail + user_id;

    if(navigator.userAgent.match(/Android/i)){
    window.scrollTo(0,1);
    }

    // set width of progress circle
    var circle_width = $('.circle-container').width() * 0.85;
    console.log(circle_width);

    // init progress circle
  $('.circle').circleProgress({
    value: (0 / 10),
    size: circle_width,
    fill: {
      color: "white"
    },
    thickness: circle_width/35,
    emptyFill: 'rgba(0, 0, 0, 0.0)'
  });

  $('#counter').text("0");
  $('#weight').hide();
  $('#exercise-name').hide();

    function loop() {
        setTimeout(function () {
            // check whether there is an active set. If so, show set data.
            $.ajax({
                type: 'GET',
                url: link_userprofile_detail,
                success: function(response_set) {
                       console.log(response_set)
                        // if active set, get data and update
                        $.ajax({
                            type: 'GET',

                            url: link_set_detail + response_set._pr_active_set,
                            success: function(response_set) {
                            // change value of progress circle
                                console.log(response_set.repetitions);
                                if (response_set.repetitions != reps) {
                                    reps = response_set.repetitions;
                                    $('.circle').circleProgress({
                                    value: (reps / 10),
                                    fill: {
                                      color: 'rgb(255, 150, 1)'
                                    },
                                    emptyFill: 'rgba(0, 0, 0, 0.0)',
                                    animationStartValue: ((reps-1)/10)
                                  });
                                  $('#counter').text(reps.toString());
                                  $('#weight').show();
                                  $('#exercise-name').show();
                                };
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