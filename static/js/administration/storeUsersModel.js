StoreUsersModel.prototype = new Model;
//constructor definition
StoreUsersModel.prototype.constructor = StoreUsersModel;

function StoreUsersModel() {
	this.filterText = "";
}

StoreUsersModel.prototype.filterItems = function(filter){
	if(filter){	
		filter = filter.toLowerCase();
		this.filterText = filter;
		this.filteredItems =  this.items.filter(function (el) {
			  return (el.username.toLowerCase().indexOf(filter) > -1 || el.email.toLowerCase().indexOf(filter) > -1 ||el.store_name.toLowerCase().indexOf(filter) > -1);
			});
	}
	else{
		this.filteredItems =  this.items;
	}
}


StoreUsersModel.prototype.save = function(item){
	var exist_user = this.items.getObjectById(item.id);
	if(exist_user!=null){
		exist_user.username = item.username;
		exist_user.email = item.email;
		exist_user.password = item.password; 
	}
	else{		
		this.items.push(item);
	}
	this.updateUsersData();
};

StoreUsersModel.prototype.updateUsersData = function(){
	for(var i = 0; i < this.items.length; i++){
		var user = this.items[i];
		var store = this.getStoreById(user.store_id);
		if(store!=null && store.length>0)
			store=store[0];
		user["store_name"] = store!=null ? store.name : "&nbsp;";
	}
};

StoreUsersModel.prototype.getStoreById = function(id){
	var found = this.stores.filter(function (el) {
		  return el.id == id;
	});
	if (found.length == 1) return found;
	return null;
};
