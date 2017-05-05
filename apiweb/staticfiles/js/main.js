$(document).ready(function () {

    // Set listeners
    setScrollToTopListener();
});

/**
 * Set the scroll listener to the back-to-top button. Also controls the fading of the
 * element and scrolls the screen to the top when it is clicked.
 */
function setScrollToTopListener() {

    // Call this function when the scroll position changes
    $(window).scroll(function () {
        // Get the height of the footer and the whole page
        var footerheight = $("footer").outerHeight();
        var pageheight = $("html").height();

        // Get scroll position
        var scrolltop = $(this).scrollTop();
        var scrollbottom = scrolltop + $(window).height();

        // Scroll thingy to the correct position
        if (scrollbottom > pageheight - footerheight) {
            $('#backtotop').css("bottom", footerheight - (pageheight - scrollbottom) + 15);
            $('#mc_embed_signup').css("bottom", footerheight - (pageheight - scrollbottom) + 15);
        } else {
            $('#backtotop').css("bottom", 15);
            $('#mc_embed_signup').css("bottom", 15);
        }

        // Fade the thing in and out
        if ($(this).scrollTop() > 30) {
            $('#backtotop').fadeIn();
        } else {
            $('#backtotop').fadeOut();
        }
    });

    // Set OnClickListener to scroll to the top of the page
    $('#backtotop').click(function () {
        $('#backtotop').tooltip('hide');
        $('body,html').animate({
            scrollTop: 0
        }, 800);
        return false;
    });

    // Show tooltip when the mouse hovers over the element
    $('#backtotop').tooltip('show');

    $('a[class="smooth-scroll"]').click(function(event){
        event.preventDefault();
        // console.log("this is the problem");
        $('html, body').animate({

            scrollTop: $( $.attr(this, 'href') ).offset().top
        }, 500);
        // return false;
    });
};
