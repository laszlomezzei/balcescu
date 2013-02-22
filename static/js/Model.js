Model.prototype = new Object;
//constructor definition
Model.prototype.constructor = Model;

function Model() {
	this.filterText = "";
	this.items = [];
	this.filteredItems = [];
}


Model.prototype.getIndexById = function (obj) {
  var i = this.items.length;
  while (i--) {
      if (this.items[i].id + "" == obj + "") {
          return i;
      }
  }
  return -1;
};

Model.prototype.getItemById = function(id){
	var found = this.items.filter(function (el) {
		  return el.id == id;
	});
	if (found.length == 1) return found;
	return null;
};

Model.prototype.remove = function(itemid){
	var index = this.getIndexById(itemid);
	if(index >-1) 
		this.items.splice(index,1);
};

Model.prototype.save = function(item){
	if(item.id==""){
		//set temporary fake-id (should be the id of item after save)
		item.id = this.items.length+1;
		this.items.push(item);
	}
};

Model.prototype.filterItems = function(filter){
	if(filter){	
		filter = filter.toLowerCase();
		this.filterText = filter;
		this.filteredItems =  this.items.filter(function (el) {
			  return el.name.toLowerCase().indexOf(filter) > -1;
			});
	}
	else{
		this.filteredItems =  this.items;
	}
}

function sortByNameAsc(a,b)
{
	if(a.name>b.name) return 1;
	if(a.name<b.name) return -1;
	return 0;
}

function sortByNameDesc(a,b)
{
	if(a.name>b.name) return -1;
	if(a.name<b.name) return 1;
	return 0;
}

function sortByAddressAsc(a,b)
{
	if(a.address>b.address) return 1;
	if(a.address<b.address) return -1;
	return 0;
}

function sortByAddressDesc(a,b)
{
	if(a.address>b.address) return -1;
	if(a.address<b.address) return 1;
	return 0;
}