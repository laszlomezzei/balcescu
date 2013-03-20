Controller.prototype = new Object;
//constructor definition
Controller.prototype.constructor = Controller;

function Controller() {
    this.permissions = {accounts: "",
        assets: "CRUD",
        feedback: "CRUD",
        guidelines: "CRUD",
        manuals: "CRUD",
        store_groups: "CRUD",
        store_users: "CRUD",
        stores: "CRUD",
        tags: "CRUD",
        users: "CRUD"};
	//this.permissions = IShopRest.getPermissions();
}

Controller.prototype.index = function(){
	this.viewer.renderIndex(this.model);
};

Controller.prototype.list = function(filter){
	this.model.filterItems(filter);
	this.viewer.removeAllActiveRows();
	this.viewer.reloadIndex(this.model);
};

Controller.prototype.add = function(){
	this.viewer.renderNew();
};

Controller.prototype.edit = function(itemid){
	this.viewer.renderEdit(this.model, itemid);
};

Controller.prototype.remove = function(itemid){
	this.viewer.removeAllActiveRows();
	this.model.remove(itemid);
	this.viewer.reloadIndex(this.model);
};

Controller.prototype.save = function(item){
	this.viewer.removeAllActiveRows();
	this.model.save(item);
	this.viewer.reloadIndex(this.model);
};
