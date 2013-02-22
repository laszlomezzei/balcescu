StoreGroupsController.prototype = new Controller;
//constructor definition
StoreGroupsController.prototype.constructor = StoreGroupsController;

function StoreGroupsController() {
	this.model = new StoreGroupsModel();
//	this.model.items = IShopRest.getStoreGroups();
	this.model.items.sort(sortByNameAsc);
	this.model.filterItems();
	this.viewer = new StoreGroupsView();
}

