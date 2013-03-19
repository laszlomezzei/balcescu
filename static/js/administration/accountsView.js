AccountsView.prototype = new View;
//constructor definition
AccountsView.prototype.constructor = AccountsView;

function AccountsView() {
    
}

AccountsView.prototype.renderIndex = function(model){
	$($('#adminMainContent').render({
		type:"Account",
		placeholder:"Account name",
		templateEditAccounts:"#templateEditAccounts",
		item:controller.model.item,
		permissions:controller.permissions})
		)
		.appendTo('#main-content');
	
	this.attachLiveEvents();
};

AccountsView.prototype.attachLiveEvents = function(){
	View.prototype.attachLiveEvents();

	$('.aola-delete').live('click', function(ev) {
		$('.aola-edit, .aola-delete').removeClass('active');
		$(this).addClass('active');	
		itemid = $(this).closest('li').attr("rel");
		controller.viewer.renderRemove(itemid, "Delete Company?");
	});
	
	$('.aole-delete input').live('click', function(ev) {
		controller.remove($(this).data("itemid"));
	});


	
};
