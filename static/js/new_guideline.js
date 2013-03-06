Cufon.replace('.cuf, #main-nav li a',{
    hover:  true
});

jQuery(window).load( function() {
	
	IShopHelper.initLogoffBox();
	IShopHelper.addPublishButtonState();
	IShopNewGuideline.init();
	
	var filterAssetsByTags = function(asset_collection) {
		/*
		if ( $($('#mbs-assets-selector li').get(0)).hasClass('active')) {
			IShopNewGuideline.feedProductsList(asset_collection);
		} 
		else {
			IShopNewGuideline.feedFixturesList(asset_collection);
		}
		*/
		
		IShopNewGuideline.feedProductsList(asset_collection);
		IShopNewGuideline.feedFixturesList(asset_collection);
		
		IShopNewGuideline.markUsedAssets();
		IShopNewGuideline.initDragAndDrop();
	};
	
	var filterAllAssetsByTags = function(pro_coll, fix_coll) {
		IShopNewGuideline.feedProductsList(pro_coll);
		IShopNewGuideline.feedFixturesList(fix_coll);
		IShopNewGuideline.markUsedAssets();
	};	
	
	$("#demo-input-facebook-theme").tokenInput(IShopRest.getAllTags(),{
		theme: "facebook",
		onAdd: function(item) {
			var pro_coll = IShopRest.getAssetsByTagsAndType( $(this).tokenInput('get'), 'product' );
			var fix_coll = IShopRest.getAssetsByTagsAndType( $(this).tokenInput('get'), 'fixture');
			filterAllAssetsByTags(pro_coll, fix_coll);
			IShopNewGuideline.initDragAndDrop();
			IShopNewGuideline.addCursorsAtOld();
		},
		onDelete: function(item) {
			var pro_coll = IShopRest.getAssetsByTagsAndType( $(this).tokenInput('get'), 'product' );
			var fix_coll = IShopRest.getAssetsByTagsAndType( $(this).tokenInput('get'), 'fixture');
			filterAllAssetsByTags(pro_coll, fix_coll);
			IShopNewGuideline.initDragAndDrop();
			IShopNewGuideline.addCursorsAtOld();
			//IShopNewGuideline.initDragAndDrop();
			
		},		
		preventDuplicates: false
	});
	
	$('.pl-canvas').guidelineAccordion();
	//$($('#mbs-assets-selector li').get(1)).trigger('click');
});
