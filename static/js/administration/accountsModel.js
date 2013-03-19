AccountsModel.prototype = new Object;
//constructor definition
AccountsModel.prototype.constructor = AccountsModel;

function AccountsModel() {
	this.item = {id:1, name:"Adidas", 
		stores_used:45, stores_max:50, stores_available:5, 
		storeusers_used:350, storeusers_max:400, storeusers_available:50,
		guidelines_sent:75, products_total:450, 
		licence_renew:true, licence_valid:"2014-01-01",
		contact_name:"Celine d'Ancourt", contact_email:"celinedancourt@adidas.com", contact_phone:"+35 56 98 34789934",
		contact_address:"Calle di Magio 4556, 34856 Barcelona", contact_billing_address:"Calle di Magio 4556, 34856 Barcelona"};
}
