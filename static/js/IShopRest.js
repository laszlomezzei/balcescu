/**
 * Rest methods for IShopShape
 * @author Jan Nosul, jan.nosul@strawberries.nl
 */


IShopRest	=	{
	tmp_data:	null
};


IShopRest.getJSON	=	function(_url, successCallback, errorCallback) {
	var sync = false;
	if(successCallback){
		sync=true;
	}
	$.ajax({
		async: sync,
		dataType: "json",
		url: _url,
		success:    function(data) {
			if(successCallback) {
				successCallback(data);
			} else {
				IShopRest.tmp_data	=	data;
			}
		},
		error: function(error)
		{
			if(errorCallback) 
				errorCallback(data);
			else {
				console.log("ERROR:"+error);
			}
		}
	});
	return IShopRest.tmp_data;
};

IShopRest.sendJSON	=	function(_url, _object, _method, successCallback, errorCallback) {
	var sync = false;
	if(successCallback){
		sync=true;
	}
	_j = JSON.stringify(_object);
	$.ajax({
		async: sync,
		type: _method,
		url: _url,
		data: _j,
		dataType: 'json',
		contentType:    'application/json',
		success:    function(data) {
			if(successCallback) {
				successCallback(data);
			} else {
				IShopRest.tmp_data	=	data;
			}
		},
		error: function(error)
		{
			if(errorCallback) {
				errorCallback(data);
			} else {
				console.log("ERROR:"+error);
			}
		}
	});
	return IShopRest.tmp_data;
};

IShopRest.sendEmptyJSON	=	function(_url, _method) {
	$.ajax({
		async: false,
		type: _method,
		url: _url,
		dataType: 'json',
		contentType:    'application/json',
		success:    function(data) {
			IShopRest.tmp_data	=	data;
		}
	});
	return IShopRest.tmp_data;
};

IShopRest.sendString	=	function(_url, _string, _method) {
	$.ajax({
		type: _method,
		url: _url,
		data: _string,
		dataType: 'json',
		contentType:    'application/json'
	});
	
};

IShopRest.getNewGuideline	=	function() {
	return this.getJSON('/service/guideline/new');
};

IShopRest.saveGuideline	=	function() {
	var _g	=	{};
	_g.id	=	IShopModel.guideline.id;
	_g.name	=	IShopModel.guideline.name;
	_g.description	=	IShopModel.guideline.description;
	_g.due_date	=	IShopModel.guideline.due_date;
	_g.photo_required	=	IShopModel.guideline.photo_required;
	
	IShopRest.sendJSON('/service/guideline', _g, 'POST' );
	
};

IShopRest.deleteGuideline = function(guideline_id) {
	// console.log( '/service/tag-group/'+ tag_group_id );
	this.sendEmptyJSON('/service/guideline/delete/'+ guideline_id, 'DELETE' );
};

IShopRest.saveCanvas	=	function(_canvas_nr) {
	var _c	=	{};
	_c.id	=	IShopModel.guideline.canvases[_canvas_nr].id;
	_c.order	=	_canvas_nr;
	_c.background_id	=	IShopModel.guideline.canvases[_canvas_nr].background_id;
	IShopRest.sendJSON('/service/guideline/'+IShopModel.guideline.id+'/canvas', _c, 'POST' );
};

IShopRest.saveAsset	=	function(_canvas_nr, _asset_nr) {
	_canvas_nr --;
	_asset_nr --;
	var _a	=	{};
	_a.id = IShopModel.guideline.canvases[_canvas_nr].assets[_asset_nr].id;
	_a.quantity = IShopModel.guideline.canvases[_canvas_nr].assets[_asset_nr].quantity;
	_a.order = IShopModel.guideline.canvases[_canvas_nr].assets[_asset_nr].order;
	_a.product_number = IShopModel.guideline.canvases[_canvas_nr].assets[_asset_nr].product_number;
	_a.product_name = IShopModel.guideline.canvases[_canvas_nr].assets[_asset_nr].name;
	_a.product_image_name = IShopModel.guideline.canvases[_canvas_nr].assets[_asset_nr].image;
	_a.posx = IShopModel.guideline.canvases[_canvas_nr].assets[_asset_nr].posx;
	_a.posy = IShopModel.guideline.canvases[_canvas_nr].assets[_asset_nr].posy;
	IShopRest.sendJSON('/service/guideline/'+IShopModel.guideline.id+'/canvas/'+IShopModel.guideline.canvases[_canvas_nr].id+'/asset',_a,'POST');
};

IShopRest.deleteAsset	=	function(_canvas_nr, _asset_nr) {
	_canvas_nr --;
	_asset_nr --;
	var _url = '/service/guideline/'+IShopModel.guideline.id+'/canvas/'+IShopModel.guideline.canvases[_canvas_nr].id+'/asset/'+IShopModel.guideline.canvases[_canvas_nr].assets[_asset_nr].order;
	IShopRest.sendEmptyJSON(_url, 'DELETE');
};

IShopRest.clearCanvas	=	function(_canvas_nr) {
	IShopRest.sendEmptyJSON('/service/guideline/'+IShopModel.guideline.id+'/canvas/'+IShopModel.guideline.canvases[_canvas_nr].id, 'DELETE');
};

IShopRest.getUploadUrl	=	function() {
	return this.getJSON('/service/asset/uploadurl');
};

IShopRest.getAllTagGroups = function(criteria) {
	var g = [];
	var groups = this.getJSON('/service/tag-group/all');
	if (criteria) {
		$.each(groups.tag_groups, function(idx, group) {
			if( group[criteria]) {
				g.push(group);
			}
		});
		groups.tag_groups = g;
	}
	return groups;
};

IShopRest.getAllGuidelines = function() {
	return this.getJSON('/service/guideline/all');
};

IShopRest.test = function() {
	//return this.getJSON('/service/asset/new');
	IShopRest.sendJSON('/service/fixture/name/asc', '', 'POST');
};

/* This is not used now. waiting for nicos input */
IShopRest.getAllAssets = function() {
	return this.getJSON('/service/fixture/all');
};

IShopRest.getAllFixtures = function(sort_criteria) {
	//return this.sendJSON('/service/fixture/'+sort_criteria.sort_by+'/'+sort_criteria.order, [], 'POST');
    return this.sendJSON('/service/fixtures/all');
};

IShopRest.getAllProducts = function(sort_criteria) {
	//return this.sendJSON('/service/product/'+sort_criteria.sort_by+'/'+sort_criteria.order, [], 'POST');
    return this.sendJSON('/service/products/all');
};

IShopRest.createAssets = function(assets) {
	this.sendJSON(' /service/asset', assets, 'PUT' );
};

IShopRest.createTagGroup = function(tag_group) {
	//console.log(tag_group);
	return this.sendJSON('/service/tag-group', tag_group, 'PUT' );
};

IShopRest.saveTagGroup = function(tag_group) {
	this.sendJSON('/service/tag-group', tag_group, 'POST' );
};

IShopRest.deleteTagGroup = function(tag_group_id) {
	// console.log( '/service/tag-group/'+ tag_group_id );
	this.sendEmptyJSON('/service/tag-group/'+ tag_group_id, 'DELETE' );
};

IShopRest.deleteTag = function(tag_id) {
	//console.log( '/service/tag/'+ tag_id );
	this.sendEmptyJSON('/service/tag/'+ tag_id, 'DELETE' );
};

IShopRest.saveTag = function(tag) {
	this.sendJSON('/service/tag', tag, 'POST' );
};

IShopRest.moveTagToGroup = function(tag_id, old_group_id, new_group_id) {
	//console.log('/service/tag/'+tag_id+'/'+old_group_id+'/'+new_group_id);
	this.sendJSON('/service/tag/'+tag_id+'/'+old_group_id+'/'+new_group_id, '', 'POST' );
}

IShopRest.createTag = function(tag, tag_group_id) {
	//console.log('/service/tag/'+tag_group_id);
	return this.sendJSON('/service/tag/'+tag_group_id, tag, 'PUT' );
};

IShopRest.updateAsset = function(asset) {
	this.sendJSON('/service/asset', asset, 'POST' );
};

IShopRest.removeAsset = function(asset_id) {
	this.sendEmptyJSON('/service/asset/'+asset_id, 'DELETE' );
};

IShopRest.authenticateDevice = function() {
	var device = {"device_id":"427d95dfe260607e6a6e98694618e82e","token_id":"46f2634fc39cdc341257ce48910966d085c1f3e6194783f159ef8b183e214412"};
	console.log(this.sendJSON('/service/device', device, 'POST' ));
};

IShopRest.createManual = function(manual, group_id) {
	return this.sendJSON('/service/manual/'+group_id, manual, 'PUT' );
};

IShopRest.createManualGroup = function(name) {
	// temporary...
	var man_group = {
                "id" : 0,
                "name" : name,
                "manuals" : []
}
	return this.sendJSON('/service/manual-group', man_group, 'PUT' );
};

IShopRest.getAllManualGroups = function() {
	return this.getJSON('/service/manual-group/all');
};

IShopRest.deleteManualGroup = function(manual_group_id) {
	this.sendEmptyJSON('/service/manual-group/'+ manual_group_id, 'DELETE' );
};

IShopRest.new_saveCanvas	=	function(canvas) {
	IShopRest.sendJSON('/service/guideline/'+IShopNewGuideline.guideline.id+'/canvas', canvas, 'POST' );
};

IShopRest.new_saveAsset	=	function(canvas, hotspot) {
	var asset = jQuery.extend(true, {}, hotspot.asset);
	asset.posx = hotspot.posx;
	asset.posy = hotspot.posy;
	asset.quantity = hotspot.quantity;
	asset.order = hotspot.order;
	IShopRest.sendJSON('/service/guideline/'+IShopNewGuideline.guideline.id+'/canvas/'+canvas.id+'/asset',asset,'POST');
};

IShopRest.new_deleteAsset = function(canvas, hotspot) {
	var _url = '/service/guideline/'+IShopNewGuideline.guideline.id+'/canvas/'+canvas.id+'/asset/'+hotspot.order;
	IShopRest.sendEmptyJSON(_url,'DELETE');	
	
};

IShopRest.updateManualGroup = function(manual_group) {
	this.sendJSON('/service/manual-group', manual_group, 'POST' );
};

IShopRest.saveManual = function(manual) {
	this.sendJSON('/service/manual', manual, 'POST' );
};

IShopRest.moveManualToGroup = function(manual_id, old_group_id, new_group_id) {
	this.sendJSON('/service/manual/'+manual_id+'/'+old_group_id+'/'+new_group_id, '', 'POST' );
	//console.log('/service/manual/'+manual_id+'/'+old_group_id+'/'+new_group_id);
}

IShopRest.new_saveGuideline = function(guideline) {
	IShopRest.sendJSON('/service/guideline/'+guideline.id, guideline, 'POST' );
};

IShopRest.publishGuideline = function(guideline) {
	if (guideline.due_date == null) {
		alert('Please, fill up due date');
	}
	else {
	
		IShopRest.sendJSON('/service/guideline/'+guideline.id, '', 'PUT' );
		alert('Guideline sent.');
		window.location = '/static/guidelines.html';
	}
};

IShopRest.getAllTags = function() {
	//return this.getJSON('/service/tag/all');
    return [];
};

IShopRest.getAssetsByTags = function(tags) {
	var tag_ids = [];
	
	$.each(tags, function(id, tag) {
		tag_ids.push(tag.id);
	});
	var assets_collection;
	if ( $($('#mbs-assets-selector li').get(0)).hasClass('active')) {
		assets_collection = IShopRest.sendJSON('/service/product/name/asc', tag_ids, 'POST' );
	} 
	else {
		assets_collection = IShopRest.sendJSON('/service/fixture/name/asc', tag_ids, 'POST' );
	}
	return assets_collection;
	//console.log( assets_collection );
};

IShopRest.getAssetsByTagsAndType = function(tags, type) {
	var tag_ids = [];
	$.each(tags, function(id, tag) {
		tag_ids.push(tag.id);
	});
	if (type == 'product') {
		return IShopRest.sendJSON('/service/product/name/asc', tag_ids, 'POST' );	
	} else {
		return IShopRest.sendJSON('/service/fixture/name/asc', tag_ids, 'POST' );
	}
};

IShopRest.deleteManual = function(manual) {
	this.sendEmptyJSON('/service/manual/'+ manual.id,'DELETE');
};

IShopRest.getDashboardByGuidelines = function(callback) {
	this.getJSON('/service/dashboard/guidelines', function (data){ callback( data); });
};

IShopRest.getDashboardByDate = function(callback) {
	 this.getJSON('/service/dashboard/newest', function (data){callback( data); });
};

IShopRest.getDashboardConversations = function(guideline) {
	return this.getJSON('/service/dashboard/conversation/' + guideline.guideline_id + '/' + guideline.store_id);
};

IShopRest.new_saveGuidelineFeedback = function(feedback) {

	IShopRest.sendJSON('/service/dashboard/feedback/' + feedback.guideline_id + '/' +
			feedback.store_id, feedback, 'POST' );
};

IShopRest.new_clearCanvas	=	function(canvas) {
	IShopRest.sendEmptyJSON('/service/guideline/'+IShopNewGuideline.guideline.id+'/canvas/'+canvas.id, 'DELETE');
};

/** Super search related **/

IShopRest.getTagsAutocomplete = function(query_string) {
	return this.getJSON('/service/search/tag/' + query_string );
};

IShopRest.getManualsAutocomplete = function(query_string) {
	return this.getJSON('/service/search/manual/' + query_string );
};

IShopRest.getProductsAutocomplete = function(query_string) {
	return this.getJSON('/service/search/product/' + query_string );
};

IShopRest.getFixturesAutocomplete = function(query_string) {
	return this.getJSON('/service/search/fixture/' + query_string );
};

IShopRest.getGuidelinesAutocomplete = function(query_string) {
	return this.getJSON('/service/search/feedback/' + query_string );
};

IShopRest.getSuperSearchTagOutcomes = function(criterias) {
	return IShopRest.sendJSON('/service/search/tag/', criterias, 'POST' );
};

IShopRest.getSuperSearchProductOutcomes = function(criterias) {
	return IShopRest.sendJSON('/service/search/product/', criterias, 'POST' );
};

IShopRest.getSuperSearchFixtureOutcomes = function(criterias) {
	return IShopRest.sendJSON('/service/search/fixture/', criterias, 'POST' );
};

IShopRest.getSuperSearchGuidelineOutcomes = function(criterias) {
	return IShopRest.sendJSON('/service/search/feedback/', criterias, 'POST' );
};

IShopRest.getSuperSearchManualOutcomes = function(criterias) {
	return IShopRest.sendJSON('/service/search/manual/', criterias, 'POST' );
};

IShopRest.getSuperSearchGuidelineLatestOutcomes = function(criterias) {
	return IShopRest.sendJSON('/service/search/latest-feedback/', criterias, 'POST' );
};

IShopRest.getGuidelineById = function(guideline_id) {
	return IShopRest.getJSON('/service/guideline/'+guideline_id);
};



IShopRest.getAllStores = function(filter) {
	return IShopRest.getJSON('/service/stores/all');
};

IShopRest.saveStore = function(store) {
	return IShopRest.sendJSON('/service/save_store', store, 'PUT');
};

IShopRest.getAllUsers = function(filter) {
	return IShopRest.getJSON('/service/users/all');
};

IShopRest.saveUser = function(user) {
	return IShopRest.sendJSON('/service/save_user', user, 'POST');
};

