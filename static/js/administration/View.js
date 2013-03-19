View.prototype = new Object;
//constructor definition
View.prototype.constructor = View;

function View() {
    
}

View.prototype.attachLiveEvents = function(){
	$('#als-input').live('blur', function(){
		controller.list($(this).val())
	});

	$('.aola-edit').live('click', function(ev) {
		li_element = $(this).closest('li');
		controller.viewer.renderEdit(li_element);
	});
	
	$('#tf-new-item').live('click', function(ev){
		controller.viewer.renderNew();
	});
	
	$('.aole-cancel').live('click', function(ev) {
		controller.viewer.removeAllActiveRows();
	});
	
	$('.aea-cancel').live('click', function(ev) {
		controller.viewer.removeAllActiveRows();
	});
};

View.prototype.removeAllActiveRows = function() {
	$('.aol-edit').slideUp(function() {
		$(this).remove();
	});
};

View.prototype.renderRemove = function(itemid, deletetext){
	this.removeAllActiveRows();
	var tmpl = $($('#adminDelete').render({itemid:itemid, deletetext:deletetext}));
	$(tmpl).hide();
	$($('li[rel='+itemid+']')).after($(tmpl));
	$(tmpl).slideDown();	
}
