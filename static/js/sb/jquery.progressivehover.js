/*
 * jQuery Plugin, Progressive hover for IShop dashboard page
 * @author Jan Nosul, jan.nosul@strawberries.nl
 * 
 */

(function ($) {

// Default settings
var DEFAULT_SETTINGS = {
};

// Additional public (exposed) methods
var methods = {
		
    init: function(_options) {
        var settings = $.extend({}, DEFAULT_SETTINGS, _options || {});
        return this.each(function () {
            $(this).data("progressiveHoverObject", new $.ProgressiveHover(this, settings));
        });
    },

//	some API exposing
//	testos_return: function() {
//    	return this.data("progressiveHoverObject").testos_return();
// 	}

};

//Expose the .progressiveHover function to jQuery as a plugin

$.fn.progressiveHover = function (method) {
    if(methods[method]) {
        return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
    } else {
        return methods.init.apply(this, arguments);
    }
};

$.ProgressiveHover = function (dl_element, settings) {

//	main code here
//	get needed dimensions and amount of pictures inside dl wrapper

	settings['dl_width'] = $(dl_element).width();
	settings['dl_height'] = $(dl_element).height();
	settings['images_nr'] = $(dl_element).find('dd img').length;
	settings['overlay_width'] = settings.dl_width / settings.images_nr;
	//console.log(JSON.stringify(settings));
	addHoverOverlays();
	centereImagesVertically();
	showImage(0);
	
	function addHoverOverlay(id) {
		//var left = i
		var left = id * settings.overlay_width+3;
		var overlay = $('<div class="progressive-hover-overlay" rel="'+id+'"></div>').css({
			"width": settings.overlay_width,
			"height": settings.dl_height,
			"left": left+"px",
			"opacity": 0
		});
		
		$(overlay).bind('mouseover', function() {
			$(dl_element).find('dd').addClass('off');
			showImage(parseInt($(this).attr('rel')));
		});
		
		return overlay;
	}
	
	function centereImagesVertically() {
		var _height, _top;
		$(dl_element).find('img').each(function(id) {
			$(this).load(function() {
				_height = $(this).height();
				if (_height != 160) {
					var _top = (160 - _height)/2;
					$(this).css({
						'position': 'relative',
						'top': _top
					});
				}
			});
		});
	};
	
	function addHoverOverlays() {
		for ( var i = 0; i < settings.images_nr; ++i ) {
			var overlay = addHoverOverlay(i);
			$(dl_element).append($(overlay));
		}
	}
	
    function addEvents() {
		$('.progressive-hover-overlay').bind({
			"mouseover": function() {
				showImage(parseInt($(this).attr('rel')));
			}
		});
    }
	
	function showImage(image_nr) {
		$($(dl_element).find('dd')[image_nr]).removeClass('off');
	}

    
};


})(jQuery);


