Cufon.replace('.cuf, #main-nav li a',{
    hover:  true
});

jQuery(window).load( function() {
	$('#loading').show();
	// test
	IShopHelper.initLogoffBox();
	var guidelines;
	if ($('#page-type').val() == 'by_guideline') {
		guidelines = IShopRest.getDashboardByGuidelines(function(data) {IShopGuidelines.init(data["data"])});
	}
	else {
		guidelines = IShopRest.getDashboardByDate(function(data) {IShopGuidelines.init(data["data"])});
	}
	
	renderData();
	
});



function renderData(){
	
	//IShopGuidelines.init(guidelines);
	
	$('#als-input').supersearchtokenInput([], {
		theme: "supersearch",
		preventDuplicates: false,
		onAdd: function() {
			$('#loading').show();
			if ($('#page-type').val() == 'by_guideline') {
				var groups = IShopRest.getSuperSearchGuidelineOutcomes( this.supersearchtokenInput('get') );
				$('#guideline-overview-list-gutter').empty();
			} else {
				var groups = IShopRest.getSuperSearchGuidelineLatestOutcomes( this.supersearchtokenInput('get') );
				$('.gol-row-center').empty();
			}
			IShopGuidelines.init(groups);
			$('#loading').hide();
			//console.log(groups);
		},
		onDelete: function() {
			$('#loading').show();
			if ($('#page-type').val() == 'by_guideline') {
				var groups = IShopRest.getSuperSearchGuidelineOutcomes( this.supersearchtokenInput('get') );
				$('#guideline-overview-list-gutter').empty();

			} else {
				var groups = IShopRest.getSuperSearchGuidelineLatestOutcomes( this.supersearchtokenInput('get') );
				$('.gol-row-center').empty();
			}
			IShopGuidelines.init(groups);
			$('#loading').hide();
		},
		getAutocomplete: function(value) {
			return IShopRest.getGuidelinesAutocomplete(value);
		}
	});

}