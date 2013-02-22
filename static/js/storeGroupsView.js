StoreGroupsView.prototype = new View;
//constructor definition
StoreGroupsView.prototype.constructor = StoreGroupsView;

function StoreGroupsView() {
    
}

StoreGroupsView.prototype.renderIndex = function(model){
	$($('#adminMainContent').render({
			type:"Storegroup",
			placeholder:"Store group name", 
			headerRowTemplate:"#templateHeaderRowStoreGroups", 
			itemsTemplate:"#templateItemsStoreGroups",
			items:controller.model.filteredItems})
		)
		.appendTo('#main-content');
	this.attachLiveEvents();
};

StoreGroupsView.prototype.renderEdit = function(element){
	this.removeAllActiveRows();
	$('.active').removeClass('active');
	var item  = controller.model.getItemById(element.attr("rel"))[0];
	var tmpl = $('#templateEditStoreGroups').render({item:item, stores:controller.model.stores});
	$(tmpl).hide();	
	$(element).after($(tmpl));
	$('.aol-edit').slideDown();	
};

StoreGroupsView.prototype.renderNew = function(){
	$('.active').removeClass('active');
	this.removeAllActiveRows();
	var tmpl = $('#templateEditStoreGroups').render({item:{id : "", name : "", stores : ""}, stores:controller.model.stores});
	$(tmpl).insertBefore('#asset-overview-sort-list');
};

StoreGroupsView.prototype.reloadIndex = function(model){
	$('#aol-center').empty();
	if(model.filteredItems.length>0)
		$($('#templateItemsStoreGroups').render({items:model.filteredItems})).appendTo('#aol-center');
};

StoreGroupsView.prototype.attachLiveEvents = function(){
	View.prototype.attachLiveEvents();
	
	$('.aea-save').live('click', function(ev){
		li_element = $(this).closest('li');
		var checked = []
		$("input[id='aoli-stores[]']:checked").each(function ()
		{
		    checked.push(parseInt($(this).val()));
		});
		var id = li_element.attr("rel");
		if(id){
			item = controller.model.getItemById(id)[0];
			item.name = $('#aoli-name').val();
			item.stores = checked;
		} else {
			item = {id:"", name:$('#aoli-name').val(), stores:checked};
		}
		controller.save(item);
	});
	
	$('.aola-delete').live('click', function(ev) {
		$('.aola-edit, .aola-delete').removeClass('active');
		$(this).addClass('active');	
		itemid = $(this).closest('li').attr("rel");
		controller.viewer.renderRemove(itemid, "Delete Store group?");
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
	
};
