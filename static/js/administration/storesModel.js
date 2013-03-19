StoresModel.prototype = new Model;
//constructor definition
StoresModel.prototype.constructor = StoresModel;

function StoresModel() {
}


StoresModel.prototype.saveStore = function(item){
	var exist_store = this.getItemById(item.id);
	if(exist_store!=null){
		exist_store.name = item.name;
		exist_store.address = item.address;
	}
	else{
		this.items.push(store);
	}
};

StoresModel.prototype.filterStores = function(filter){
	if(filter){	
		filter = filter.toLowerCase();
		this.filterText = filter;
		this.filteredItems =  this.items.filter(function (el) {
			  return (el.name.toLowerCase().indexOf(filter) > -1 || el.address.toLowerCase().indexOf(filter) > -1);
			});
	}
	else{
		this.filteredItems =  this.items;
	}
}
