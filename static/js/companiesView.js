CompaniesView.prototype = new View;
//constructor definition
CompaniesView.prototype.constructor = CompaniesView;

function CompaniesView() {
    
}

CompaniesView.prototype.renderIndex = function(model){
	$($('#adminMainContent').render({
			type:"Company",
			placeholder:"Company name", 
			headerRowTemplate:"#templateHeaderRowCompanies", 
			itemsTemplate:"#templateItemsCompanies",
			items:controller.model.filteredItems})
		)
		.appendTo('#main-content');
	this.attachLiveEvents();
};

CompaniesView.prototype.renderEdit = function(element){
	this.removeAllActiveRows();
	$('.active').removeClass('active');
	var item  = controller.model.getItemById(element.attr("rel"))[0];
	var tmpl = $('#templateEditCompanies').render({item:item});
	$(tmpl).hide();	
	$(element).after($(tmpl));
	$('.aol-edit').slideDown();	
};

CompaniesView.prototype.renderNew = function(){
	$('.active').removeClass('active');
	this.removeAllActiveRows();
	var tmpl = $('#templateEditCompanies').render({item:{id : "", name : ""}});
	$(tmpl).insertBefore('#asset-overview-sort-list');
};

CompaniesView.prototype.reloadIndex = function(model){
	$('#aol-center').empty();
	if(model.filteredItems.length>0)
		$($('#templateItemsCompanies').render({items:model.filteredItems})).appendTo('#aol-center');
};

CompaniesView.prototype.attachLiveEvents = function(){
	View.prototype.attachLiveEvents();
	
	$('.aea-save').live('click', function(ev){
		li_element = $(this).closest('li');
		var id = li_element.attr("rel");
		if(id){
			item = controller.model.getItemById(id)[0];
			item.name = $('#aoli-name').val();
		} else {
			item = {id:"", name:$('#aoli-name').val()};
		}
		controller.save(item);
	});
	
	$('.aola-delete').live('click', function(ev) {
		$('.aola-edit, .aola-delete').removeClass('active');
		$(this).addClass('active');	
		itemid = $(this).closest('li').attr("rel");
		controller.viewer.renderRemove(itemid, "Delete Company?");
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
