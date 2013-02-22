CompaniesController.prototype = new Controller;
//constructor definition
CompaniesController.prototype.constructor = CompaniesController;

function CompaniesController() {
	this.model = new CompaniesModel();
//	this.model.items = IShopRest.getStoreGroups();
	this.model.items.sort(sortByNameAsc);
	this.model.filterItems();
	this.viewer = new CompaniesView();
}

