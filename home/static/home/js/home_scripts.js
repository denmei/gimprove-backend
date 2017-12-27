$(document).ready( function() {

    $('.scroll-webapp').on('click', (event) => {
        $('html, body').animate({
            scrollTop: $('#webapp-carousel').offset().top
        }, 400);
    });

    $('.scroll-app').on('click', (event) => {
        $('html, body').animate({
            scrollTop: $('#app-carousel').offset().top
        }, 400);
    });

});