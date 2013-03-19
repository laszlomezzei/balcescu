StoreGroupsController.prototype = new Controller;
//constructor definition
StoreGroupsController.prototype.constructor = StoreGroupsController;

function StoreGroupsController() {
	this.model = new StoreGroupsModel();
//	this.model.items = IShopRest.getAllStoreGroups();

    this.model.items = [{id: 23001,
    is_archived: false,
    name: "Europe",
    stores: [],
    stores_id: []},
        {id: 25001,
    is_archived: false,
    name: "North America",
    stores: [],
    stores_id: []}];

	this.model.updateItems();
	this.model.stores = IShopRest.getAllStores();
	this.model.items.sort(sortByNameAsc);
	this.model.filterItems();
	this.viewer = new StoreGroupsView();
}

StoreGroupsController.prototype.index = function(){
	if(this.permissions.store_groups.indexOf('R')>-1)
		this.viewer.renderIndex(this.model);
};

StoreGroupsController.prototype.save = function(item){
	var result = IShopRest.saveStoreGroup(item);
	var storeGroup = eval(result);
	if(storeGroup.id){
		//update model.stores
		this.model.save(storeGroup);
		//reload the page, 
		this.viewer.removeAllActiveRows();
		this.viewer.reloadIndex(this.model);
	}
	else {
		alert("Cannot save store group.");
	}
};

StoreGroupsController.prototype.remove = function(storegroupId){
	this.viewer.removeAllActiveRows();
	//remove from model
	var storegroup = this.model.items.getObjectById(storegroupId);
	storegroup.is_archived = true;
	this.model.remove(storegroupId);
	var result = IShopRest.saveStoreGroup(storegroup);
	this.viewer.reloadIndex(this.model);
};
