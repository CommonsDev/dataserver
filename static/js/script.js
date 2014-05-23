$(document).bind('afterready', function() {
    var wW = $('body').width(); 
    $('#main #slider .pagination').css('left', wW/2 - 475 + 175).fadeIn(1000);
});

$(function(){
    if(!flux.browser.supportsTransitions)
        alert("Flux Slider requires a browser that supports CSS3 transitions");
        
    window.f = new flux.slider('#slider', {
        autoplay: true,
        pagination:true,
        delay:4000,
        transitions: ['dissolve']
    });

    var wW = $('body').width(); 
    $('header').css('left', wW/2 - 475);

    setTimeout(function() {
        $(document).trigger('afterready');
    }, 5000);

    $("a[href^=#]").click(function() {
	    $('html, body').animate({
	        scrollTop: $($(this).attr('href')).offset().top
	    }, 1000);
	});
});

$(window).resize(function(){
    var wW = $('body').width(); 
    $('header').css('left', wW/2 - 475);
    $('#main #slider .pagination').css('left', wW/2 - 475 + 175);
});

$(document).ready(function() {
    var hash = $(location).attr('hash');
    var scrollPos = (hash) ? $(hash).offset().top : 0
    var setFocus = function() {
        console.log(">>>iframe stealing focus !");
        $('html, body').animate({ scrollTop: scrollPos}, 1);
        $("#main").focus();
        $("#carto_iframe").blur();
    }
    $("#carto_iframe").load(function () {
        console.debug('>>>> iFrame loaded!');
        setTimeout(function() {
            $('html, body').animate({ scrollTop: scrollPos}, 1);
        }, 300);
    });
    $("#carto_iframe").focus(setFocus());
    $("#carto_iframe").ready(console.log(">>>> iframe ready !"))
});
