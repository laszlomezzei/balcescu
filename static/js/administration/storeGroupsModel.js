StoreGroupsModel.prototype = new Model;
//constructor definition
StoreGroupsModel.prototype.constructor = StoreGroupsModel;

function StoreGroupsModel() {
	this.filterText = "";
//	this.items = [{id:97, name:'Europe', stores:[3,4]},{id:101,name:'North America', stores:[102]}];
//	this.stores = [{id:3, name:'VR Romania'},{id:4, name:'VR Nederland'},{id:102, name:'VR United States'},{id:106, name:'VR China'}];
}
StoreGroupsModel.prototype.updateItems = function(){
	for(var i=0; i<this.items.length; i++){
		this.items[i].stores_id=[];
		for(var j=0; j<this.items[i].stores.length; j++)
		{
			this.items[i].stores_id.push(this.items[i].stores[j].id);
		}
		console.log(this.items[i].stores_id);
	}	
};


StoreGroupsModel.prototype.save = function(storegroup){
	var exist_store = this.items.getObjectById(storegroup.id);
	if(exist_store!=null){
		exist_store.name = storegroup.name;
		exist_store.stores = storegroup.stores;
		console.log(exist_store.stores.length);
	}
	else{		
		this.items.push(storegroup);
	}
	this.updateItems();
};
