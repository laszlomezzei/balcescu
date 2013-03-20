StoresController.prototype = new Controller;
//constructor definition
StoresController.prototype.constructor = StoresController;

function StoresController() {
	this.model = new StoresModel();
	this.model.items = IShopRest.getAllStores();
	//this.model.storegroups = IShopRest.getAllStoreGroups();
	this.model.items.sort(sortByNameAsc);
	this.model.filterItems();
	this.viewer = new StoresView();
}

StoresController.prototype.index = function(){
	if(this.permissions.stores.indexOf('R')>-1)
		this.viewer.renderIndex(this.model);
};

StoresController.prototype.save = function(item){
	var result = IShopRest.saveStore(item);
	//update model.stores
	var st = eval(result);
	if(st.id)
	{	
		this.model.save(st);
		//reload the page, 
		this.viewer.removeAllActiveRows();
		this.viewer.reloadIndex(this.model);
	}
	else {
		alert("Cannot save store.");
	}
};

StoresController.prototype.remove = function(storeId){
	this.viewer.removeAllActiveRows();
	//remove from model
	var store = this.model.items.getObjectById(storeId);
	store.is_archived = true;
	this.model.remove(storeId);
	var result = IShopRest.saveStore(store);
	this.viewer.reloadIndex(this.model);
};
