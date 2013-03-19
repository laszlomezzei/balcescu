UsersModel.prototype = new Model;
//constructor definition
UsersModel.prototype.constructor = UsersModel;

function UsersModel() {
	this.roles = [{name:"Administrator", code:'ADMINISTRATOR'},{name:"Manager VM", code:'HQ'},{name:"Store Group Manager", code:'REGION_HQ'},{name:"Store Manager", code:'STORE_MANAGER'}];
//	this.stores = [{id:3, name:'VR Romania'},{id:4, name:'VR Nederland'},{id:102, name:'VR United States'},{id:106, name:'VR China'}];
//	this.filters = [{id:97, name:'Europe'},{id:101,name:'North America'}];
}

UsersModel.prototype.save = function(user){
	var exist_user = this.items.getObjectById(user.id);
	if(exist_user!=null){
		exist_user.username = user.username;
		exist_user.email = user.email;
		exist_user.password = user.password; 
		exist_user.roles = user.roles;
	}
	else{		
		this.items.push(user);
	}
	this.updateUsersData();
};


UsersModel.prototype.filterItems = function(filter){
	if(filter){	
		filter = filter.toLowerCase();
		this.filterText = filter;
		this.filteredItems =  this.items.filter(function (el) {
			  return (el.username.toLowerCase().indexOf(filter) > -1 || el.email.toLowerCase().indexOf(filter) > -1 || el.role.toLowerCase().indexOf(filter) > -1);
			});
	}
	else{
		this.filteredItems =  this.items;
	}
}
UsersModel.prototype.updateUsersData = function(){
	for(var i = 0; i < this.items.length; i++){
		var user = this.items[i];
	    var store = this.getStoreById(user.store_id);

	    user["store_name"] = store!=null ? store.name : "&nbsp;";
	    user["role"] = this.getRoleNameByCode(user.roles[1]);
	    user["filter_name"] = this.getFilterById(user.filter);
    }
};

UsersModel.prototype.getStoreById = function(id){
     var found = this.stores.filter(function (el) {
               return el.id == id;
     });
     if (found.length == 1) return found[0];
     return null;
};

UsersModel.prototype.getRoleNameByCode = function(code){
	var found = this.roles.filter(function (el) {
		return el.code == code;
	});
	if (found.length == 1) return found[0].name;
	return "&nbsp;";
};


UsersModel.prototype.getFilterById = function(storegroup){
	var found = this.filters.filter(function (el) {
		return el.id == storegroup;
	});
	if (found.length == 1) return found[0].name;
	return "&nbsp;";
};