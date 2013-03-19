var IShopHelper = {};


IShopHelper.determineImageSize = function(image_info, width, height) {
	var _return;
	var box_ratio = height/width;
	if (image_info.image_ratio >= box_ratio) {
		if ( image_info.image_ratio < 1) {
			_return = Math.ceil(height / image_info.image_ratio);
			// Never return a size larger then the actual image
			if (_return >= image_info.image_width) {
				_return = image_info.image_width;
			}
		}
		else {
			_return = height;
			// Never return a size larger then the actual image
			if (_return >= image_info.image_heigth) {
				_return = image_info.image_heigth;
			}
		}
	}
	else {
		if (image_info.image_ratio > 1) {
			_return = Math.floor(width * image_info.image_ratio);
			// Never return a size larger then the actual image
			if (_return >= image_info.image_heigth) {
				_return = image_info.image_heigth;
			}
		}
		else {
			_return = width;
			// Never return a size larger then the actual image
			if (_return >= image_info.width) {
				_return = image_info_width;
			}
		}
	}
	return _return;
};

IShopHelper.getImageSize = function(image_info, width, height) {
	var _return = {};
	var box_ratio = height/width;
	if (image_info.image_ratio >= box_ratio) {
		// Never return a size larger then the actual image
		if (height >= image_info.image_heigth) {
			_return = {
					"height": image_info.image_heigth,
					"width": image_info.image_width
				};
		}
		else {
			_return = {
					"height": height,
					"width": height/image_info.image_ratio
				};
		}
	}
	else {
		// Never return a size larger then the actual image
		if (width >= image_info.image_width) {
			_return = {
					"height": image_info.image_heigth,
					"width": image_info.image_width
				};
		}
		else {
			_return = {
					"height": width*image_info.image_ratio,
					"width": width
				};
		}
	}
	return _return;	
};

IShopHelper.initLogoffBox = function() {

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
	
};

IShopHelper.addSaveButtonStates = function() {
	$('.aea-save, #assets-save-all input[type=image], .ie-button input[type=image], .eg-button input[type=image], .tgleg-button input[type=image], .tglc-create-action-section input[type=image], .tglc-edit-action-section input[type=image], #manuals-save-all, #tglwnga-save input[type=image]').live({
		"mousedown": function() {
			$(this).attr('src', 'images/tglc-save-active.png');
		}, 
		"mouseup": function() {
			$(this).attr('src', 'images/tglc-save.png');
		}
	});
};

IShopHelper.addPublishButtonState = function() {
	$('#ga-publish-guideline').bind({
		"mousedown": function() {
			$(this).attr('src', 'images/ngd_button_publish-active.png');
			//alert('a');
		}, 
		"mouseout": function() {
			$(this).attr('src', 'images/ngd_button_publish.png');
		}
	});
};











