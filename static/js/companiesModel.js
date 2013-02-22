CompaniesModel.prototype = new Model;
//constructor definition
CompaniesModel.prototype.constructor = CompaniesModel;

function CompaniesModel() {
	this.filterText = "";
	this.items = [{id:1, name:"Puma"}, {id:2, name:"Nike"}, {id:3, name:"Adidas"}, {id:4, name:"Columbia Sportswear"} ];
}
