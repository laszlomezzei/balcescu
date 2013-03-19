UsersController.prototype = new Controller;
//constructor definition
UsersController.prototype.constructor = UsersController;

function UsersController() {
	this.model = new UsersModel();
	this.model.stores = IShopRest.getAllStores();
	this.model.items = IShopRest.getAllUsers();
	this.model.filters = IShopRest.getAllStoreGroups();
	this.model.items.sort(sortByUsernameAsc);
	this.model.updateUsersData();
	this.model.filterItems();
	this.viewer = new UsersView();
}

UsersController.prototype.index = function(){
	if(this.permissions.users.indexOf('R')>-1)
		this.viewer.renderIndex(this.model);
};

UsersController.prototype.save = function(item){
	var result = IShopRest.saveUser(item);
	var usr = eval(result);
	if(usr.id){
		//update model.stores
		this.model.save(usr);
		//reload the page, 
		this.viewer.removeAllActiveRows();
		this.viewer.reloadIndex(this.model);
	}
	else {
		alert("Cannot save user.");
	}
};

UsersController.prototype.remove = function(userId){
	this.viewer.removeAllActiveRows();
	//remove from model
	var user = this.model.items.getObjectById(userId);
	user.is_archived = true;
	this.model.remove(userId);
	var result = IShopRest.saveUser(user);
	this.viewer.reloadIndex(this.model);
};
