$(document).ready(function () {

    // Set listeners
    setModalImageClickListener();
    setCollapsibleMenuClickListeners();
    setScrollToTopListener();
    setPictureZoom();
    $('.feedback').feedback();


    // Tooltip with certificate info in product modal
    $("[data-toggle=tooltip]").tooltip();

    $(function() {
      // Javascript to enable link to tabpages
      var hash = document.location.hash;

      // Change hash for page-reload
      $('.certificate').on('show.bs.tab', function (e) {
        window.location.hash = e.target.hash;
      });

      var url = window.location.href;
      var index = url.indexOf("#");

      if (index > 0) {
          var activeTab = url.substring(index + 1);
          $(".tab-pane").removeClass("active in");
          $("#" + activeTab).addClass("active in");
        }

    });

    // console.log(sessionStorage['news_closed']);
    // console.log(localStorage['news_closed']);
    if ((sessionStorage['news_closed'] != 'True') && (localStorage['news_closed'] != 'True')) {
        console.log('show letter');
        $('#mc_embed_signup').css('visibility', 'visible');
    }
});

function setPictureZoom() {
        $('img.grote-foto').on('click', function() {
            $('.enlargeImageModalSource').attr('src', $(this).attr('src'));
            $('#enlargeImageModal').modal('show');
        });
}

function centerModal(im) {
    $(this).css('display', 'block');
    var $dialog = $(this).find(".modal-dialog");
    var offset = ($(window).height() - $dialog.height()) / 2;
    $('#picpopup').attr('src', im); //$("img", $(".mini-foto")).attr("src"));
    // Center modal vertically in window
    $dialog.css("margin-top", offset);
}



/**
 * Sets listeners to the small images in the modal. When a picture is clicked, they are
 * shown in the big picture holder.
 */

function setModalImageClickListener() {

    var current_image = $('.grote-foto').attr("src");
    console.log(current_image);

    // In modal: Displays the image that is clicked on.
    $(".mini-foto").click( function () {
        $(this).closest('.detail-left-block').find('.grote-foto').attr("src", $("img", $(this)).attr("src"));
//        current_image = $("img", $(this)).attr("src");
        current_image = console.log($("img", $(this)).attr("src"));
//        console.log(current_image);
    });


    $("#closeX").click( function () {
        // console.log('clicked!');
        $(this).closest('#mc_embed_signup').hide(100);
        sessionStorage['news_closed'] = 'True';

    });

    $("#mc-embedded-subscribe").click( function () {
        // console.log('subscribed!');
        $(this).closest('#mc_embed_signup').hide(100);
        localStorage['news_closed'] = 'True';
    });


    $('.modal').on('show.bs.modal', centerModal(current_image));
    $(window).on("resize", function () {
        $('.modal:visible').each(centerModal(current_image));
    });
}

/**
 * Changes the icons of the collapsible menus when they are clicked.
 */
function setCollapsibleMenuClickListeners() {
    // Switch up and down arrows on click in the sidebar
    function toggleChevron(e) {
        $(e.target).prev().prev().toggleClass('glyphicon-chevron-down glyphicon-chevron-up');
    }

    function toggleChevronFaq(e) {
        $(e.target)
            .prev('.question')
            .find("i.indicator")
            .toggleClass('fa-chevron-down fa-chevron-up');
    }
    $('#accordion').on('hidden.bs.collapse', toggleChevronFaq);
    $('#accordion').on('shown.bs.collapse', toggleChevronFaq);

    // Set clicklisteners
    $('#collapse-menu').on('hidden.bs.collapse', toggleChevron);
    $('#collapse-menu').on('shown.bs.collapse', toggleChevron);
}

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



$(".nr-pages li a").click(function(){
  $(this).parents(".pages-parent").find('.dropdown-toggle').html($(this).text() + ' <span class="caret"></span>');
  $(this).parents(".pages-parent").find('.dropdown-toggle').val($(this).data('value'));
});


jQuery(document).ready(function($){
    //update these values if you change these breakpoints in the style.css file (or _layout.scss if you use SASS)
    var MqM= 768,
        MqL = 1024;

    var faqsSections = $('.cd-faq-group'),
        faqTrigger = $('.cd-faq-trigger'),
        faqsContainer = $('.cd-faq-items'),
        faqsCategoriesContainer = $('.cd-faq-categories'),
        faqsCategories = faqsCategoriesContainer.find('a'),
        closeFaqsContainer = $('.cd-close-panel');

    //select a faq section
    faqsCategories.on('click', function(event){
        event.preventDefault();
        var selectedHref = $(this).attr('href'),
            target= $(selectedHref);
        if( $(window).width() < MqM) {
            faqsContainer.scrollTop(0).addClass('slide-in').children('ul').removeClass('selected').end().children(selectedHref).addClass('selected');
            closeFaqsContainer.addClass('move-left');
            $('body').addClass('cd-overlay');
        } else {
            $('body,html').animate({ 'scrollTop': target.offset().top - 19}, 200);
        }
    });

    //close faq lateral panel - mobile only
    $('body').bind('click touchstart', function(event){
        if( $(event.target).is('body.cd-overlay') || $(event.target).is('.cd-close-panel')) {
            closePanel(event);
        }
    });
    faqsContainer.on('swiperight', function(event){
        closePanel(event);
    });

    //show faq content clicking on faqTrigger
    faqTrigger.on('click', function(event){
        event.preventDefault();
        $(this).next('.cd-faq-content').slideToggle(200).end().parent('li').toggleClass('content-visible');
    });

    //update category sidebar while scrolling
    $(window).on('scroll', function(){
        if ( $(window).width() > MqL ) {
            (!window.requestAnimationFrame) ? updateCategory() : window.requestAnimationFrame(updateCategory);
        }
    });

    $(window).on('resize', function(){
        if($(window).width() <= MqL) {
            faqsCategoriesContainer.removeClass('is-fixed').css({
                '-moz-transform': 'translateY(0)',
                '-webkit-transform': 'translateY(0)',
                '-ms-transform': 'translateY(0)',
                '-o-transform': 'translateY(0)',
                'transform': 'translateY(0)',
            });
        }
        if( faqsCategoriesContainer.hasClass('is-fixed') ) {
            faqsCategoriesContainer.css({
                'left': faqsContainer.offset().left,
            });
        }
    });

    function closePanel(e) {
        e.preventDefault();
        faqsContainer.removeClass('slide-in').find('li').show();
        closeFaqsContainer.removeClass('move-left');
        $('body').removeClass('cd-overlay');
    }

    function updateCategory(){
        updateCategoryPosition();
        updateSelectedCategory();
    }

    function updateCategoryPosition() {
        //TODO: Variable top does not work, there is no class called '.cd-faq'.
        //var top = $('.cd-faq').offset().top,

        var height = jQuery('.cd-faq').height() - jQuery('.cd-faq-categories').height(),
            margin = 20;
        if( top - margin <= $(window).scrollTop() && top - margin + height > $(window).scrollTop() ) {
            var leftValue = faqsCategoriesContainer.offset().left,
                widthValue = faqsCategoriesContainer.width();
            faqsCategoriesContainer.addClass('is-fixed').css({
                'left': leftValue,
                'top': margin,
                '-moz-transform': 'translateZ(0)',
                '-webkit-transform': 'translateZ(0)',
                '-ms-transform': 'translateZ(0)',
                '-o-transform': 'translateZ(0)',
                'transform': 'translateZ(0)',
            });
        } else if( top - margin + height <= $(window).scrollTop()) {
            var delta = top - margin + height - $(window).scrollTop();
            faqsCategoriesContainer.css({
                '-moz-transform': 'translateZ(0) translateY('+delta+'px)',
                '-webkit-transform': 'translateZ(0) translateY('+delta+'px)',
                '-ms-transform': 'translateZ(0) translateY('+delta+'px)',
                '-o-transform': 'translateZ(0) translateY('+delta+'px)',
                'transform': 'translateZ(0) translateY('+delta+'px)',
            });
        } else {
            faqsCategoriesContainer.removeClass('is-fixed').css({
                'left': 0,
                'top': 0,
            });
        }
    }

    function updateSelectedCategory() {
        faqsSections.each(function(){
            var actual = $(this),
                margin = parseInt($('.cd-faq-title').eq(1).css('marginTop').replace('px', '')),
                activeCategory = $('.cd-faq-categories a[href="#'+actual.attr('id')+'"]'),
                topSection = (activeCategory.parent('li').is(':first-child')) ? 0 : Math.round(actual.offset().top);

            if ( ( topSection - 20 <= $(window).scrollTop() ) && ( Math.round(actual.offset().top) + actual.height() + margin - 20 > $(window).scrollTop() ) ) {
                activeCategory.addClass('selected');
            }else {
                activeCategory.removeClass('selected');
            }
        });
    }
});

// Bug report

// AJAX for posting
function create_post() {
    // alert("it works!");
    // console.log("create post is working!") // sanity check

    $.ajax({
        url : "www.google.nl",    // $(this).attr('action'), // the endpoint
        type : "GET", // http method
        dataType: 'json',
        // data : { res : $('#post-text').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            alert('got data');
            alert(json);
        //     $('#post-text').val(''); // remove the value from the input
        //     console.log(json); // log the returned json to the console
        //     console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            alert('oeps error:  ' + errmsg);
        //     $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
        //         " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
        //     console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

};


(function ( $ ) {
    $.fn.feedback = function(success, fail) {
        self=$(this);
        self.find('.dropdown-menu-form').on('click', function(e){e.stopPropagation()})

        self.find('.screenshot').on('click', function(){
            self.find('.cam').removeClass('fa-camera fa-check').addClass('fa-refresh fa-spin');
            html2canvas($(document.body), {
                onrendered: function(canvas) {
                    self.find('.screen-uri').val(canvas.toDataURL("image/png"));
                    self.find('.cam').removeClass('fa-refresh fa-spin').addClass('fa-check');
                }
            });
        });

        self.find('.do-close').on('click', function(){
            self.find('.dropdown-toggle').dropdown('toggle');
            self.find('.reported, .failed').hide();
            self.find('.report').show();
            self.find('.cam').removeClass('fa-check').addClass('fa-camera');
            self.find('.screen-uri').val('');
            self.find('textarea').val('');
        });

        // failed = function(){
        //     self.find('.loading').hide();
        //     self.find('.failed').show();
        //     if(fail) fail();
        // }

        self.find('form').on('submit', function(){
            self.find('.report').hide();
            self.find('.loading').show();
            // console.log('first part');
            // create_post();

            $.post( $(this).attr('action'), $(this).serialize(), null, 'json').always(function(){
                // var test = "{{ form }}";
                // alert(test);
                // create_post();

                // if(res.result == 'success'){
                // console.log('second part');
                self.find('.loading').hide();
                self.find('.reported').show();


                    // if(success) success();
                // } else fail/ed();
            }
            );
            return false;


        });
    };
}( jQuery ));
