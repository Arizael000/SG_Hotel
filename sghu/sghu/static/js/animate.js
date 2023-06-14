$(window).scroll(function() {
  $('.animate-card').each(function() {
    var position = $(this).offset().top;
    var scroll = $(window).scrollTop();
    var windowHeight = $(window).height();
    if (scroll > position - windowHeight + 200) {
      $(this).animate({ 'opacity': '1', 'margin-top': '0px' }, 1000);
    }
  });
});

