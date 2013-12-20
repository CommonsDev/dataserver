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
        delay:5000,
        transitions: ['dissolve']
    });

    var wW = $('body').width(); 
    $('header').css('left', wW/2 - 475);

    setTimeout(function() {
        $(document).trigger('afterready');
    }, 3000);

    $("a[href^=#]").click(function() {
	    $('html, body').animate({
	        scrollTop: $($(this).attr('href')).offset().top
	    }, 2000);
	});
});

$(window).resize(function(){
	var wW = $('body').width(); 
    $('header').css('left', wW/2 - 475);
    $('#main #slider .pagination').css('left', wW/2 - 475 + 175);
});
