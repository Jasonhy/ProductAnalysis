$(function () {
    "use strict";


    /* ==========================================================================
     Background Slideshow images
     ========================================================================== */

    $(".main").backstretch([
        "/static/img/bg-1.jpg",
        "/static/img/bg-2.jpg"

    ], {
        fade: 750,
        duration: 4000
    });


    /* ==========================================================================
     On Scroll animation
     ========================================================================== */

    if ($(window).width() > 992) {
        new WOW().init();
    }
    ;


    /* ==========================================================================
     Fade On Scroll
     ========================================================================== */


    if ($(window).width() > 992) {

        $(window).on('scroll', function () {
            $('.main').css('opacity', function () {
                return 1 - ($(window).scrollTop() / $(this).outerHeight());
            });
        });
    }
    ;


    $(".rotate").textrotator({
        animation: "dissolve",
        separator: ",",
        speed: 2500
    });


});
