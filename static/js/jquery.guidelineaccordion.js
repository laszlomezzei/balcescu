/*
 * jQuery Plugin, Guideline accordion for IShopShape
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
            $(this).data("guidelineAccordionObject", new $.GuidelineAccordion(this, settings));
        });
    },

//	some API exposing
    toggleSection: function() {
        this.data("guidelineAccordionObject").toggleSection();
        return this;
    },
    openSection: function() {
        this.data("guidelineAccordionObject").openSection();
        return this;
    },
    closeSection: function() {
        this.data("guidelineAccordionObject").closeSection();
        return this;
    }	
};

$.fn.guidelineAccordion = function (method) {
    if(methods[method]) {
        return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
    } else {
        return methods.init.apply(this, arguments);
    }
};

$.GuidelineAccordion = function (element, settings) {
	var plc_list = $(element).find('.plc-list');
	var header = $(element).find('header');
	
	addEvents();
	
	/**
	 * Some public API exposing
	 */
	 
	 this.toggleSection = function() {
		// call private meth
		toggleSection();
	 }
	 
	 this.openSection = function() {
		// call private meth
		openSection();
	 }
	 
	 this.closeSection = function() {
		// call private meth
		closeSection();
	 }	 
	/**
	 * Events section
	 */
	function addEvents() {
		$(header).click(function() {
			toggleSection();
		});
	}
	
	function toggleSection() {
		if( $(element).hasClass('collapsed') ) {
			openSection();
		}
		else {
			closeSection();
		}
	}
	
	function openSection() {
		if ($(element).hasClass('collapsed')) {
			$(element).removeClass('collapsed');
			$(plc_list).slideDown();
		}
	}
	
	function closeSection() {
		if (!$(element).hasClass('collapsed')) {
			$(plc_list).slideUp(function() {
				$(element).addClass('collapsed');
			});
		}
	}

		
};


})(jQuery);










