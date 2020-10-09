$('.form').find('input, textarea').on('keyup blur focus', function (e) {
  
  var $this = $(this),
      label = $this.prev('label');

	  if (e.type === 'keyup') {
			if ($this.val() === '') {
          label.removeClass('active highlight');
        } else {
          label.addClass('active highlight');
        }
    } else if (e.type === 'blur') {
    	if( $this.val() === '' ) {
    		label.removeClass('active highlight'); 
			} else {
		    label.removeClass('highlight');   
			}   
    } else if (e.type === 'focus') {
      
      if( $this.val() === '' ) {
    		label.removeClass('highlight'); 
			} 
      else if( $this.val() !== '' ) {
		    label.addClass('highlight');
			}
    }

});

$('.tab a').on('click', function (e) {
  
  e.preventDefault();
  
  $(this).parent().addClass('active');
  $(this).parent().siblings().removeClass('active');
  
  target = $(this).attr('href');

  $('.tab-content > div').not(target).hide();
  
  $(target).fadeIn(600);
  
});

$("#signup-form").on('submit', function(e) {
	e.preventDefault();
	$.post('/signup', $("#signup-form").serialize(), function(data) {
		title = $("#signup > h1");
		title.text(data.msg);
		if (data.success) {
			title.css('color', '#179b77');
		} else {
			title.css('color', 'red');
		}
	}, dataType="json");
});

$("#login-form").on('submit', function(e) {
	e.preventDefault();
	$.post('/login', $("#login-form").serialize(), function(data) {
		title = $("#login > h1");
		title.text(data.msg);
		if (data.success) {
			title.css('color', '#179b77');
			setTimeout(function() { window.location = '/'; }, 1000);
		} else {
			title.css('color', 'red');
		}
	}, dataType="json");
});
