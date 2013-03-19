UsersView.prototype = new View;
//constructor definition
UsersView.prototype.constructor = UsersView;

function UsersView() {
    
}

UsersView.prototype.renderIndex = function(model){
	$($('#adminMainContent').render({
			type:"User",
			placeholder:"Username, email or role", 
			headerRowTemplate:"#templateHeaderRowUsers", 
			itemsTemplate:"#templateItemsUsers",
			items:controller.model.filteredItems,
			permissions:controller.permissions})
		)
		.appendTo('#main-content');
	this.attachLiveEvents();
};

UsersView.prototype.renderEdit = function(element){
	this.removeAllActiveRows();
	$('.active').removeClass('active');
	var item  = controller.model.getItemById(element.attr("rel"))[0];
	var tmpl = $('#templateEditUsers').render({item:item, 
		roles:controller.model.roles,
		stores:controller.model.stores,
		filters:controller.model.filters});
	$(tmpl).hide();	
	$(element).after($(tmpl));
	$('.aol-edit').slideDown();	
};

UsersView.prototype.renderNew = function(){
	$('.active').removeClass('active');
	this.removeAllActiveRows();
	var tmpl = $('#templateEditUsers').render({item:{id : "", name : "", email:"", password:"",roles:[]},
		roles:controller.model.roles,
		stores:controller.model.stores,
		filters:controller.model.filters});
	$(tmpl).insertBefore('#asset-overview-sort-list');
};

UsersView.prototype.reloadIndex = function(model){
	$('#aol-center').empty();
	if(model.filteredItems.length>0)
		$($('#templateItemsUsers').render({items:model.filteredItems,
			permissions:controller.permissions})).appendTo('#aol-center');
};

UsersView.prototype.attachLiveEvents = function(){
	View.prototype.attachLiveEvents();
	
	$('.aea-save').live('click', function(ev){
		li_element = $(this).closest('li');
		var id = li_element.attr("rel");
		var item;
		if(id){
			item = controller.model.getItemById(id)[0];
			item.username = $('#aoli-username').val();
			item.email = $('#aoli-email').val();
			if($('#aoli-password').val()!="[PROTECTED]") {
				item.password = $('#aoli-password').val();
			}else{
				delete item.password;
			}
			item.role = $('#aoli-role').val();
		} else {
			item = {id:"", username:$('#aoli-username').val(), email : $('#aoli-email').val(), password : $('#aoli-password').val(), role : $('#aoli-role').val()};
		
		}
		item.roles=["ROLE_USER", item.role];
		if($('#aoli-stores').is(':visible')) {
			item.store_id = $('#aoli-store').val();
		} else {
			delete item.store_id;
		}
		if($('#aoli-filters').is(':visible')) {
			item.filter = $('#aoli-filter').val();
		} else {
			delete item.filter;
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
	
	
	$('#aoli-role').live('change', function(){
		$('#aoli-filters, #aoli-stores').hide();
		console.log($(this).val());
		if($(this).val()=="STORE_MANAGER"){
			$('#aoli-stores').show();
		}
		else if($(this).val()=="REGION_HQ"){
			$('#aoli-filters').show();
		}
	})

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

	$('#sort-role').bind('click', function() {
		if($(this).children("span").hasClass("asc")){
			controller.model.filteredItems.sort(sortByRoleDesc);
			$(this).children("span").removeClass("asc").addClass("desc");
		}else{
			controller.model.filteredItems.sort(sortByRoleAsc);
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

	$('#sort-filter').bind('click', function() {
		if($(this).children("span").hasClass("asc")){
			controller.model.filteredItems.sort(sortByFilterDesc);
			$(this).children("span").removeClass("asc").addClass("desc");
		}else{
			controller.model.filteredItems.sort(sortByFilterAsc);
			$(this).children("span").removeClass("desc").addClass("asc");
		}
		controller.viewer.reloadIndex(controller.model);
	});
};
