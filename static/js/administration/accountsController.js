AccountsController.prototype = new Controller;
//constructor definition
AccountsController.prototype.constructor = AccountsController;

function AccountsController() {
	this.model = new AccountsModel();
//	this.model.item = IShopRest.getStoreGroups();
	this.viewer = new AccountsView();
}


AccountsController.prototype.index = function(){
	if(this.permissions.accounts.indexOf('R')>-1)
		this.viewer.renderIndex(this.model);
};