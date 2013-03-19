StoreUsersView.prototype = new View;
//constructor definition
StoreUsersView.prototype.constructor = StoreUsersView;

function StoreUsersView() {
    
}

StoreUsersView.prototype.renderIndex = function(model){
	$($('#adminMainContent').render({
			type:"Storeuser",
			placeholder:"Store, user name or email", 
			headerRowTemplate:"#templateHeaderRowStoreUsers", 
			itemsTemplate:"#templateItemsStoreUsers",
			items:controller.model.filteredItems,
			permissions:controller.permissions})
		)
		.appendTo('#main-content');
	this.attachLiveEvents();
};

StoreUsersView.prototype.renderEdit = function(element){
	this.removeAllActiveRows();
	$('.active').removeClass('active');
	var item  = controller.model.getItemById(element.attr("rel"))[0];
	var tmpl = $('#templateEditStoreUsers').render({item:item, stores:controller.model.stores});
	$(tmpl).hide();	
	$(element).after($(tmpl));
	$('.aol-edit').slideDown();	
};

StoreUsersView.prototype.renderNew = function(){
	$('.active').removeClass('active');
	this.removeAllActiveRows();
	var tmpl = $('#templateEditStoreUsers').render({item:{id : "", name : "", stores : ""}, stores:controller.model.stores});
	$(tmpl).insertBefore('#asset-overview-sort-list');
};

StoreUsersView.prototype.reloadIndex = function(model){
	$('#aol-center').empty();
	if(model.filteredItems.length>0)
		$($('#templateItemsStoreUsers').render({items:model.filteredItems,
			permissions:controller.permissions})).appendTo('#aol-center');
};

StoreUsersView.prototype.attachLiveEvents = function(){
	View.prototype.attachLiveEvents();
	
	$('.aea-save').live('click', function(ev){
		li_element = $(this).closest('li');
		var id = li_element.attr("rel");
		var item;
		if(id){
			item = controller.model.getItemById(id)[0];
			item.username = $('#aoli-username').val();
			if($('#aoli-password').val()!="[PROTECTED]") {
				item.password = $('#aoli-password').val();
			} else {
				delete item.password;
			}
			item.email = $('#aoli-email').val();
			item.store_id = $('#aoli-store').val();
		} else {
			item = {id:"", username:$('#aoli-username').val(),email : $('#aoli-email').val(), password : $('#aoli-password').val(), store_id : $('#aoli-store').val()};
		}
		item.roles=["ROLE_USER","STORE"]
		controller.save(item);
	});
	
	$('.aola-delete').live('click', function(ev) {
		$('.aola-edit, .aola-delete').removeClass('active');
		$(this).addClass('active');	
		itemid = $(this).closest('li').attr("rel");
		controller.viewer.renderRemove(itemid, "Delete Store user?");
	});
	
	$('.aole-delete input').live('click', function(ev) {
		controller.remove($(this).data("itemid"));
	});

	$('#sort-username').bind('click', function() {
		if($(this).children("span").hasClass("asc")){
			controller.model.filteredItems.sort(sortByUsernameDesc);
			$(this).children("span").removeClass("asc").addClass("desc");
		}else{
			controller.model.filteredItems.sort(sortByUsernameAsc);
			$(this).children("span").removeClass("desc").addClass("asc");
		}
		controller.viewer.reloadIndex(controller.model);
	});
	

	$('#sort-storename').bind('click', function() {
		if($(this).children("span").hasClass("asc")){
			controller.model.filteredItems.sort(sortByStorenameDesc);
			$(this).children("span").removeClass("asc").addClass("desc");
		}else{
			controller.model.filteredItems.sort(sortByStorenameAsc);
			$(this).children("span").removeClass("desc").addClass("asc");
		}
		controller.viewer.reloadIndex(controller.model);
	});

	$('#sort-email').bind('click', function() {
		if($(this).children("span").hasClass("asc")){
			controller.model.filteredItems.sort(sortByEmailDesc);
			$(this).children("span").removeClass("asc").addClass("desc");
		}else{
			controller.model.filteredItems.sort(sortByEmailAsc);
			$(this).children("span").removeClass("desc").addClass("asc");
		}
		controller.viewer.reloadIndex(controller.model);
	});

};
