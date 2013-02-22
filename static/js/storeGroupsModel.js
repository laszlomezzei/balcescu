StoreGroupsModel.prototype = new Model;
//constructor definition
StoreGroupsModel.prototype.constructor = StoreGroupsModel;

function StoreGroupsModel() {
	this.filterText = "";
	this.items = [{id:2, name:"Region 2"}, {id:1, name:"Region 1"}, {id:3, name:"Region 3", stores:[4,5,6]} ];
	this.stores = [{id:1, name:"Store 1_1"}, {id:2, name:"Store 1_2"}, {id:3, name:"Store 2"}, {id:4, name:"Store 3.1"}, {id:5, name:"Store 3.2"}, {id:6, name:"Store 3.3"} ];
}
