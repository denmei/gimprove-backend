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

    $('.xl-button').on('mouseenter', (event) => {
        $(event.currentTarget).css({'color': 'black', 'background': 'white'});
    });

    $('.xl-button').on('mouseleave', (event) => {
        $(event.currentTarget).css({'color': 'white', 'background': 'transparent'});
    });

});