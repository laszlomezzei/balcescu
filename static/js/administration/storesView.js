StoresView.prototype = new View;
//constructor definition
StoresView.prototype.constructor = StoresView;

function StoresView() {
    
}


StoresView.prototype.renderIndex = function(model){
	$($('#adminMainContent').render({
			type:"Store",
			placeholder:"Name or address", 
			headerRowTemplate:"#templateHeaderRowStores", 
			itemsTemplate:"#templateItemsStores",
			items:controller.model.filteredItems,
			permissions:controller.permissions})
		)
		.appendTo('#main-content');
	this.attachLiveEvents();
};

StoresView.prototype.renderEdit = function(element){
	this.removeAllActiveRows();
	$('.active').removeClass('active');
	var item  = controller.model.getItemById(element.attr("rel"))[0];
	var tmpl = $('#templateEditStores').render({item:item, roles:controller.model.roles});
	$(tmpl).hide();	
	$(element).after($(tmpl));
	$('.aol-edit').slideDown();	
};

StoresView.prototype.renderNew = function(){
	$('.active').removeClass('active');
	this.removeAllActiveRows();
	var tmpl = $('#templateEditStores').render({item:{id : "", name : "", address:""}});
	$(tmpl).insertBefore('#asset-overview-sort-list');
};

StoresView.prototype.reloadIndex = function(model){
	$('#aol-center').empty();
	if(model.filteredItems.length>0)
		$($('#templateItemsStores').render({items:model.filteredItems,
			permissions:controller.permissions})).appendTo('#aol-center');
};

StoresView.prototype.attachLiveEvents = function(){
	View.prototype.attachLiveEvents();
	
	$('.aea-save').live('click', function(ev){
		li_element = $(this).closest('li');
		var id = li_element.attr("rel");
		if(id){
			item = controller.model.getItemById(id)[0];
			item.name = $('#aoli-name').val();
			item.addressl = $('#aoli-address').val();
		} else {
			item = {id:"", name:$('#aoli-name').val(), address : $('#aoli-address').val()};
		}
		controller.save(item);
	});
	
	$('.aola-delete').live('click', function(ev) {
		$('.aola-edit, .aola-delete').removeClass('active');
		$(this).addClass('active');	
		itemid = $(this).closest('li').attr("rel");
		controller.viewer.renderRemove(itemid, "Delete  user?");
	});
	
	$('.aole-delete input').live('click', function(ev) {
		controller.remove($(this).data("itemid"));
	});

	$('#sort-name').bind('click', function() {
		if($(this).children("span").hasClass("asc")){
			controller.model.filteredItems.sort(sortByNameDesc);
			$(this).children("span").removeClass("asc").addClass("desc");
		}else{
			controller.model.filteredItems.sort(sortByNameAsc);
			$(this).children("span").removeClass("desc").addClass("asc");
		}
		controller.viewer.reloadIndex(controller.model);
	});
	
	$('#sort-address').bind('click', function() {
		if($(this).children("span").hasClass("asc")){
			controller.model.filteredItems.sort(sortByAddressDesc);
			$(this).children("span").removeClass("asc").addClass("desc");
		}else{
			controller.model.filteredItems.sort(sortByAddressAsc);
			$(this).children("span").removeClass("desc").addClass("asc");
		}
		controller.viewer.reloadIndex(controller.model);
	});
};



//
//
//
//
//
//
//
//StoresView.prototype.renderIndex = function(model){
//	this.reloadIndex(model);
//	this.attachLiveEvents();
//};
//
//
//StoresView.prototype.reloadIndex = function(model){
//	$('#aol-center').empty();
//	$($('#templateStoreList').render({stores:model.filteredStores})).appendTo('#aol-center');
//};
//
//StoresView.prototype.attachLiveEvents = function(){
//	
//	$('.aea-save').live('click', function(ev){
//		li_element = $(this).closest('li');
//		controller.saveStore(li_element.attr("rel"), $('#aoli-name').val(), $('#aoli-address').val());
//	});
//	
//	$('.aola-delete').live('click', function(ev) {
//		$('.aola-edit, .aola-delete').removeClass('active');
//		$(this).addClass('active');	
//		li_element = $(this).closest('li');
//		controller.renderDelete(li_element);
//	});
//	
//	$('.aole-delete input').live('click', function(ev) {
//		controller.deleteStore($(this).data("storeid"));
//	});
//
//	$('#sort-name').bind('click', function() {
//		if($(this).children("span").hasClass("asc")){
//			controller.model.filteredStores.sort(sortByNameDesc);
//			$(this).children("span").removeClass("asc").addClass("desc");
//		}else{
//			controller.model.filteredStores.sort(sortByNameAsc);
//			$(this).children("span").removeClass("desc").addClass("asc");
//		}
//		controller.viewer.reloadIndex(controller.model);
//	});
//	
//	$('#sort-address').bind('click', function() {
//		if($(this).children("span").hasClass("asc")){
//			controller.model.filteredStores.sort(sortByAddressDesc);
//			$(this).children("span").removeClass("asc").addClass("desc");
//		}else{
//			controller.model.filteredStores.sort(sortByAddressAsc);
//			$(this).children("span").removeClass("desc").addClass("asc");
//		}
//		controller.viewer.reloadIndex(controller.model);
//	});
//	
//};
//
//StoresView.prototype.renderEdit = function(model, element){
//	$('.active').removeClass('active');
//	this.removeAllActiveRows();
//	var tmpl = $('#templateStoreEdit').render({store:model.filteredStores.getObjectById(element.attr("rel"))});
//	$(tmpl).hide();	
//	$(element).after($(tmpl));
//	$('.aol-edit').slideDown();	
//};
//
//StoresView.prototype.renderNew = function(){
//	$('.active').removeClass('active');
//	this.removeAllActiveRows();
//	var tmpl = $('#templateStoreEdit').render({store:{id : "", name : "", address : ""}});
//	//$(tmpl).hide();	
//	$(tmpl).insertBefore('#asset-overview-sort-list');
//	//$('.aol-edit').slideDown();	
//};
//
//
//StoresView.prototype.renderDelete = function(model, element){
//	this.removeAllActiveRows();
//	var tmpl = $('#templateStoreDelete').render({store : model.filteredStores.getObjectById(element.attr("rel"))});
//	$(tmpl).hide();
//	$(element).after($(tmpl));
//	$(tmpl).slideDown();	
//};
//
//StoresView.prototype.deleteStore = function(storeId){
//	this.removeAllActiveRows();
//	$("li[rel='"+storeId+"']").remove();
//};
