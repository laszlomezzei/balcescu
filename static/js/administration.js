/* Author:

*/


Cufon.replace('.cuf, #main-nav li a',{
    hover:  true
});

var addClick = function() {
	var elem = $('#lw-hello');
	var opacity;
	$(elem).toggleClass('closed');

	if ($(elem).hasClass('closed')) {
		opacity = 0;
		display = "none";
	}
	else {
		opacity = 1;
		display = "block";
	}
	$('#lw-bye').css('display', display).animate({
			"opacity": opacity
		}, {
			"duration": 700
	});
};

$('#logoff-wrapper').css('min-width', '102');

$('#lw-hello').bind('click', function() {
	addClick();
});

$('body').bind('click', function(ev) {
	if ($(ev.target).attr('id') != 'lw-hello') {
		if (!$('#lw-hello').hasClass('closed')) {
		
			$('#lw-hello').addClass('closed');
			$('#lw-bye, #lv-stores, #lw-users').css('display', 'none').animate({
					"opacity": 0
				}, {
					"duration": 700
			});
		}
	}

	if ( $('#dashboard-dialog-popup').length > 0 ) {
		if ($(ev.target).attr('id') == 'screen-white-overlay') {
			IShopGuidelines.removeDashboardDialogPopup();
		}
	}
});



//Array helpers
Array.prototype.getObjectById = function (obj) {
  var i = this.length;
  while (i--) {
      if (this[i].id + "" == obj + "") {
          return this[i];
      }
  }
  return null;
};

Array.prototype.getIndexById = function (obj) {
  var i = this.length;
  while (i--) {
      if (this[i].id + "" == obj + "") {
          return i;
      }
  }
  return -1;
};
