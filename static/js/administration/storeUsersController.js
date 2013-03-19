StoreUsersController.prototype = new Controller;
//constructor definition
StoreUsersController.prototype.constructor = StoreUsersController;

function StoreUsersController() {
	this.model = new StoreUsersModel();
	this.model.items = IShopRest.getAllStoreUsers();
	this.model.stores = IShopRest.getAllStores();
	this.model.updateUsersData();
	this.model.items.sort(sortByStorenameAsc);
	this.model.filterItems();
	this.viewer = new StoreUsersView();
}


StoreUsersController.prototype.index = function(){
	if(this.permissions.store_users.indexOf('R')>-1)
		this.viewer.renderIndex(this.model);
};

StoreUsersController.prototype.save = function(item){
	var result = IShopRest.saveUser(item);
	var usr = eval(result);
	if(usr.id){
		this.model.save(usr);
		//reload the page, 
		this.viewer.removeAllActiveRows();
		this.viewer.reloadIndex(this.model);
	}
	else {
		alert("Cannot save user.");
	}
};

StoreUsersController.prototype.remove = function(userId){
	this.viewer.removeAllActiveRows();
	//remove from model
	var user = this.model.items.getObjectById(userId);
	user.is_archived = true;
	this.model.remove(userId);
	var result = IShopRest.saveUser(user);
	this.viewer.reloadIndex(this.model);
};

