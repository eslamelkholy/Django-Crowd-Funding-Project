// run slider for rate
 $(function () {
    $('#slides').slideshow({
        randomize: true,      // Randomize the play order of the slides.
        slideDuration: 6000,  // Duration of each induvidual slide.
        fadeDuration: 1000,    // Duration of the fading transition. Should be shorter than slideDuration.
        animate: true,        // Turn css animations on or off.
        pauseOnTabBlur: true, // Pause the slideshow when the tab is out of focus. This prevents glitches with setTimeout().
        enableLog: true      // Enable log messages to the console. Useful for debugging.
    });

    $('.mouse-scroll').on('click', function () {
        $('html , body').stop().animate({
            scrollTop: $('#' + $(this).data('scroll')).offset().top
        }, 1500);
        event.preventDefault();
    });
 })
