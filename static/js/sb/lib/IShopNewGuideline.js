/**
 * New Guideline manager for IShopShape
 * @author Jan Nosul, jan.nosul@strawberries.nl
 */
 
IShopNewGuideline = {};

IShopNewGuideline.init = function() {
	//device autenticate
	//IShopRest.authenticateDevice();
	// set datepicker
	$( "#gdf-due_date" ).datepicker({ dateFormat: 'dd-mm-yy', minDate: '0' });
	
	IShopNewGuideline.guideline = IShopRest.getNewGuideline();
	this.initCanvases();
	
	var asset_collection = IShopRest.getAllProducts({
		"sort_by": "name",
		"order": "asc"
	});
	this.feedProductsList(asset_collection);
	
	var asset_collection = IShopRest.getAllFixtures({
		"sort_by": "name",
		"order": "asc"
	});
	this.feedFixturesList(asset_collection);
	this.addCriteriasToSorter();
	this.addEvents();
	this.initDragAndDrop();
	this.setActiveCanvas(0);
	
	this.addCursorsAtOld();
	
	$($('#mbalg-fixtures li').get($('#mbalg-fixtures li').length - 1)).css('border-bottom', 0);
	$($('#mbalg-products li').get($('#mbalg-products li').length - 1)).css('border-bottom', 0);
	// custom slider
	$('#mbal-gutter nav').jScrollPane();

};

IShopNewGuideline.addCriteriasToSorter = function() {
	$('#mbss-name').data('IShopSortCriteria', {
		"sort_by": "name",
		"order": "asc"
	});
	$('#mbss-date').data('IShopSortCriteria', {
		"sort_by": "creation-date",
		"order": "desc"
	});	
};

IShopNewGuideline.addGuidelineFormEvents	=	function() {
	$('#guideline-details-form input, textarea').change(function() {
		var value;
		var key;
		key = $(this).attr('id').replace('gdf-','');
		
		if ($(this).get(0).type == 'checkbox') {
			value = $(this).attr('checked') == 'checked' ? true : false;
		}
		else {
			value = $(this).val();
		}

		// store in model
		IShopNewGuideline.guideline[key] = value;
		// send model
		IShopNewGuideline.sendGuidelineToServer();
	});
};

IShopNewGuideline.initCanvases = function() {
	// bind server empty canvases to empty html shopshape canvases and its thumbs
	$.each( IShopNewGuideline.guideline.canvases, function(id, canvas) {
		$($('.guideline-canvas').get(id)).data('IShopCanvas', canvas);
		$($('#guideline-canvas-thumbs li').get(id)).data('IShopCanvas', canvas);
	});
};

IShopNewGuideline.addEvents = function() {
	// media browser tabs
	$('#mbs-assets-selector li').bind('click', function() {
	
//		console.log($(this));
	
		$('#mbs-assets-selector li').removeClass('active');
		$(this).addClass('active');
		$('#mbalg-products, #mbalg-fixtures').addClass('hidden');
		$('#mbalg-'+$(this).text().toLowerCase()).removeClass('hidden');
		$('#mbal-gutter nav').jScrollPane();
		IShopNewGuideline.addCursorsAtNew();
	});
		
	// reset canvas
	$('.clear-canvas').live('click', function() {
		IShopNewGuideline.resetCanvas($(this).closest('.guideline-canvas'));
		IShopNewGuideline.resetCanvasThumb( $('#guideline-canvas-thumbs li.active'));
		// remove background from model
		$(this).closest('.guideline-canvas').data('IShopCanvas').background_id = 0;
		var canvas = $(this).closest('.guideline-canvas').data('IShopCanvas');
		IShopRest.new_clearCanvas(canvas);
	});
	
	// canvas navigation
		//$('.guideline-canvas').css('z-index', 1000).droppable( "option", "disabled", true );
	//$($('.guideline-canvas').get(id)).css('z-index', 1002).droppable( "option", "disabled", false );
	
	$('.guideline-canvas').css('opacity',0).removeClass('hidden');
	$($('.guideline-canvas').get(0)).css('opacity',1);
	
	$('#guideline-canvas-thumbs li').each(function(id) {
		$(this).bind('click', function() {
		
			IShopNewGuideline.closeAllAccordionSections();
		
			$('#guideline-canvas-thumbs li').removeClass('active');
			$(this).addClass('active');
			var canvas_nr = $(this).attr('rel');
			
			IShopNewGuideline.closeAllAccordionSections();
			IShopNewGuideline.openAccordionSection(canvas_nr);
			
			$('.guideline-canvas')
			.css('z-index', 1000)
			.droppable( "option", "disabled", true )
			.animate({
				opacity: 0
			}, {
				duration: 300,
				complete: function(a,b) {
					//console.log($(this).attr('rel'));
					$($('.guideline-canvas').get(canvas_nr))
					.css('opacity',1)
					.css('z-index', 1002)
					.droppable( "option", "disabled", false );
				}
			});
		});
	});
	
	$('.canvas-hotspot').live({
		"click": function() {
			//console.log( $(this).data('IShopHotspot') );
			IShopNewGuideline.showHotspotPopup(this);
		},
		"mouseover": function() {
		//	$(this).draggable();
			if ($('#media-browser').length != 0) {
				//$(this).draggable({ containment: $(this).closest('.guideline-canvas'), scroll: false });
				$(this).draggable({ 
					containment: $(this).closest('.guideline-canvas'), 
					scroll: false 
				});
			}
		}
	});	
	
	$('.hp-close').live('click', function() {
		IShopNewGuideline.destroyHotspotPopup();
	});
	
	$('.hp-delete').live('click', function() {
		console.log('deleting');
		var hotspot = $(this).closest('.hotspot-popup').data('IShopHotspot');
		var canvas_nr = $(this).closest('.guideline-canvas').attr('rel');
		var canvas = $(this).closest('.guideline-canvas').data('IShopCanvas');
		//var hotspot_element = $(this).closest('.guideline-canvas').find('.canvas-hotspot').get(hotspot.order - 1);
		// remove hotspot element
		$(this).closest('.guideline-canvas').find('.canvas-hotspot[rel='+hotspot.order+']').remove();
		
		$($('.pl-canvas').get(canvas_nr)).find('li[rel='+hotspot.order+']').remove();
		
		IShopNewGuideline.destroyHotspotPopup();
		IShopRest.new_deleteAsset(canvas, hotspot);
		IShopNewGuideline.markUsedAssets();
		
		/*
		var canvas_nr = $(this).closest('.guideline-canvas').attr('rel');
		var hotspot_element = $(this).closest('.guideline-canvas').find('.canvas-hotspot').get(hotspot.order - 1);
		var product_list_element = $($('.pl-canvas').get(canvas_nr)).find('li').get(hotspot.order - 1);
		$(hotspot_element).remove();
		$(product_list_element).remove();
		IShopNewGuideline.destroyHotspotPopup();
		var canvas = $(this).closest('.guideline-canvas').data('IShopCanvas');
		IShopRest.new_deleteAsset(canvas, hotspot);
		IShopNewGuideline.markUsedAssets();
		*/
	});
	
	$('.qc-pl-sbc').live('click', function() {
		var canvas = $($('.guideline-canvas').get($(this).closest('.pl-canvas').attr('rel'))).data('IShopCanvas');
		IShopNewGuideline.destroyHotspotPopup();
		var hotspot = $(this).closest('li').data('IShopHotspot');
		hotspot.quantity = hotspot.quantity == 1 ? 1 : hotspot.quantity - 1;
		$(this).next().text(hotspot.quantity);
		IShopRest.new_saveAsset(canvas, hotspot);
	});

	$('.qc-pl-add').live('click', function() {
		var canvas = $($('.guideline-canvas').get($(this).closest('.pl-canvas').attr('rel'))).data('IShopCanvas');
		IShopNewGuideline.destroyHotspotPopup();
		var hotspot = $(this).closest('li').data('IShopHotspot');
		hotspot.quantity = hotspot.quantity + 1;
		$(this).prev().text(hotspot.quantity);
		IShopRest.new_saveAsset(canvas, hotspot);
	});

	$('.qc-hp-add').live('click', function() {
		var hotspot = $(this).closest('.hotspot-popup').data('IShopHotspot');
		hotspot.quantity = hotspot.quantity + 1;
		$(this).prev().text(hotspot.quantity);
		var canvas_nr = $(this).closest('.guideline-canvas').attr('rel');
		var hotspot_nr = hotspot.order - 1;
		$($($('.plc-list').get(canvas_nr)).find('.abqc-value').get(hotspot_nr)).text(hotspot.quantity);
		var canvas = $(this).closest('.guideline-canvas').data('IShopCanvas');
		IShopRest.new_saveAsset(canvas, hotspot);
	});

	$('.qc-hp-sbc').live('click', function() {
		var hotspot = $(this).closest('.hotspot-popup').data('IShopHotspot');
		hotspot.quantity = hotspot.quantity == 1 ? 1 : hotspot.quantity - 1;
		$(this).next().text(hotspot.quantity);
		var canvas_nr = $(this).closest('.guideline-canvas').attr('rel');
		var hotspot_nr = hotspot.order - 1;
		$($($('.plc-list').get(canvas_nr)).find('.abqc-value').get(hotspot_nr)).text(hotspot.quantity);
		var canvas = $(this).closest('.guideline-canvas').data('IShopCanvas');
		IShopRest.new_saveAsset(canvas, hotspot);
	});	
	
	$('.pl-show-all').bind('click', function() {
		IShopNewGuideline.openAllAccordionSections();
	});
	
	$('#ga-publish-guideline').bind('click', function() {
		IShopRest.publishGuideline(IShopNewGuideline.getGuideline());
	});
	
	IShopNewGuideline.addGuidelineFormEvents();
	
	$('#mbss-name').click(function() {
		var sort_criteria = $(this).data('IShopSortCriteria');
		sort_criteria.order = sort_criteria.order == 'asc' ? 'desc' : 'asc';
		if ( $($('#mbs-assets-selector li').get(0)).hasClass('active')) {
			var asset_collection = IShopRest.getAllProducts(sort_criteria);
			IShopNewGuideline.feedProductsList(asset_collection);
		} 
		else {
			var asset_collection = IShopRest.getAllFixtures(sort_criteria);
			IShopNewGuideline.feedFixturesList(asset_collection);
		}
		IShopNewGuideline.markUsedAssets();
		IShopNewGuideline.initDragAndDrop();
	});
	
	$('#mbss-date').click(function() {
		var sort_criteria = $(this).data('IShopSortCriteria');
		sort_criteria.order = sort_criteria.order == 'asc' ? 'desc' : 'asc';
		if ( $($('#mbs-assets-selector li').get(0)).hasClass('active')) {
			var asset_collection = IShopRest.getAllProducts(sort_criteria);
			IShopNewGuideline.feedProductsList(asset_collection);
		} 
		else {
			var asset_collection = IShopRest.getAllFixtures(sort_criteria);
			IShopNewGuideline.feedFixturesList(asset_collection);
		}
		IShopNewGuideline.markUsedAssets();
		IShopNewGuideline.initDragAndDrop();
	});	
	
	$('.abqc-add').live({
		"mousedown": function() {
			$(this).css({
				"background": "url(/images/ngd_back_asset_quantity_changer_hover.png) no-repeat -101px 0px"
			});
		},
		"mouseup": function() {
			$(this).css({
				"background": "transparent"
			});
		}
	});
	
	$('.abqc-sbc').live({
		"mousedown": function() {
			$(this).css({
				"background": "url(/images/ngd_back_asset_quantity_changer_hover.png) no-repeat -40px 0px"
			});
		},
		"mouseup": function() {
			$(this).css({
				"background": "transparent"
			});
		}
	});

	
};

IShopNewGuideline.destroyHotspotPopup = function() {
	$('.hotspot-popup').animate({
		opacity: 0
	}, {
		duration: 300,
		complete: function() {
			$(this).remove();
		}
	});
};

IShopNewGuideline.feedFixturesList = function(asset_collection) {
	$('#mbalg-fixtures').find('li').remove();
	this.generateAssetList($('#mbalg-fixtures'), asset_collection);
	$('#mbal-gutter nav').jScrollPane();
};

IShopNewGuideline.feedProductsList = function(asset_collection) {
	$('#mbalg-products').find('li').remove();
	this.generateAssetList($('#mbalg-products'), asset_collection);
	$('#mbal-gutter nav').jScrollPane();
};

IShopNewGuideline.generateAssetList = function(list_wrapper, asset_collection) {
	var asset_box;
	var product_number;
	var date_style;
	var image_src;
	$.each(asset_collection, function(id, asset) {
		var image_src = asset.image_name + '=s' + IShopHelper.determineImageSize(asset, 70, 70);
		product_number = asset.type == 'Products' ? asset.product_number : '';
		if (asset.type == 'Products') {
			product_number = asset.product_number;
		}
		
		//console.log(asset);
        asset_box = $('<li><dl class="asset-box media-browser"><dt>'+asset.name+'</dt><dd class="ab-date">'+product_number+'<span>'+asset.creation_date+'</span></dd><dd class="ab-image ab-draggable"><div><img src="'+image_src+'"><em class="hidden"></em></div></dd><dd class="ab-tags">'+IShopNewGuideline.getAssetTagsHtml(asset)+'</dd><dd class="ab-quantity-changer"><span class="abqc-sbc"></span><span class="abqc-value">2</span><span class="abqc-add"></span></dd></dl></li>').data('IShopAsset', asset);
		$(list_wrapper).append(asset_box);
		
		
	});
};

IShopNewGuideline.getAssetTagsHtml = function(asset) {

	if ($('#media-browser').length == 0) {
		return '';
	}

	var _class;
	var tags = '';
    if(asset.tag_groups)
        $.each(asset.tag_groups, function(id, tag_group) {
            $.each(tag_group.tags, function(id, tag) {
                _class = tag_group.name == 'Optional' ? ' class="optional" ' : '';
                tags += '<span'+_class+'>'+tag.name+'</span>';
            });
        });
	return tags;
};

IShopNewGuideline.applyNewCanvasBackground = function(canvas, asset) {

	//console.log(canvas);
	//console.log(asset);

	var empty_canvas_hint = $('.empty-canvas-hint').get($(canvas).attr('rel'));
	$(empty_canvas_hint).addClass('hidden');

	var background_size = IShopHelper.getImageSize(asset, 640, 434);
	var image_src = asset.image_name + '=s' + IShopHelper.determineImageSize(asset, 640, 434);
	background_size.width = background_size.width + 8;
	background_size.height = background_size.height + 8;
	var c_left = (640 - background_size.width)/2;
	var c_top = (434 - background_size.height)/2;
	$(canvas).find('.clear-canvas').addClass('hidden');
	
	// block thumbs
	
	$('#canvas-thumbs-blocker').removeClass('hidden');
	
	$(canvas).animate({
		"width": background_size.width,
		"height": background_size.height,
		"top": c_top,
		"left": c_left
	}, {
		duration: 800,
		complete: function() {
			//$(this).css('background', '#fff url('+image_src+') no-repeat 4px 4px');
			$(this).animate({
				opacity: 0
			}, {
				duration: 300,
				complete: function() {
					$(this).css('background', '#fff url('+image_src+') no-repeat 4px 4px').animate({
						opacity: 1
					}, {
						duration: 300,
						complete: function() {
							$(canvas).find('.clear-canvas').removeClass('hidden');
							IShopNewGuideline.markUsedAssets();
							$('#canvas-thumbs-blocker').addClass('hidden');
						}
					});
				}
			});
		}
	});
	
	//add canvas size object used for calculate offset for hotspots coords.
	$(canvas).data('IShopCanvasSize', background_size);
	
	var px = (14/background_size.width)*100;
	var py = (14/background_size.height)*100;
	
	$(canvas).data('IShopCanvasHotspotOffset', {
		"offset_x": px,
		"offset_y": py
	});
					
};

IShopNewGuideline.applyNewCanvasThumbBackground = function(canvas_thumb, asset) {
	var background_size = IShopHelper.getImageSize(asset, 105, 68);
	var image_src = asset.image_name + '=s' + IShopHelper.determineImageSize(asset, 105, 68);
	var c_left = (105 - background_size.width)/2;
	var c_top = (68 - background_size.height)/2;
	$(canvas_thumb).removeClass('empty').find('.small-canvas').css('background', '#ffffff').animate({
			"width": background_size.width,
			"height": background_size.height,
			"top": c_top,
			"left": c_left
		}, {
			duration: 300,
			complete: function() {
				$(this).animate({
					opacity: 0
				}, {
					duration: 300,
					complete: function() {
						$(this).css('background', '#fff url('+image_src+') no-repeat 4px 4px').animate({
							opacity: 1
						}, {
							duration: 300
						});
					}
				});
			}
	});
};

IShopNewGuideline.resetCanvas = function(canvas) {
	IShopNewGuideline.destroyHotspotPopup();
	var empty_canvas_hint = $('.empty-canvas-hint').get($(canvas).attr('rel'));
	$(empty_canvas_hint).removeClass('hidden');

	// remove hotspots
	$(canvas).find('.canvas-hotspot').fadeOut().remove();

	// remove accordion list
	
	$($('.plc-list ul').get($(canvas).attr('rel'))).find('li').fadeOut().remove();
	
	// reset canvas
	$(canvas).find('.clear-canvas').addClass('hidden');
	$(canvas).animate({
		opacity: 0
	}, {
		duration: 300,
		complete: function() {
			$(this)
			.css('background', 'url(/static/images/ngd_back_empty_canvas.png) no-repeat 0 0')
			.delay(300)
			.animate({
				opacity: 1
			}, {
				duration: 300,
				complete: function() {
					$(this).animate({
						"width": 648,
						"height": 434,
						"top": 0,
						"left": 0
					}, {
						duration: 800,
						complete: function() {
							$(canvas).find('.clear-canvas').removeClass('hidden');
							IShopNewGuideline.markUsedAssets();
						}
					});
				}
			});
		}
	});
};

IShopNewGuideline.resetCanvasThumb = function(canvas_thumb) {
	$(canvas_thumb).animate({
		opacity: 0
	}, {
		duration: 300,
		complete: function() {
			$(canvas_thumb).addClass('empty').animate({
				opacity: 1
			}, {
				duration: 300,
				complete: function() {
					
				}
			});
		}
	});
};

IShopNewGuideline.initDragAndDrop = function() {
		
	// Draggables
	$( '.ab-draggable div' ).draggable({
		appendTo: 'body',
		helper: 'clone',
		cursorAt: { 
			top: 0,
			left: 0
		},
		revert: 'invalid',
		zIndex: '1005',
		start: function(event, ui) {
			$(ui.helper).css({ 
				opacity: 0.5,
			});
		}
	});
	
	// Droppables
	$('.guideline-canvas').droppable({
		over: function( event, ui ) {
			if (!$(ui.draggable).hasClass('canvas-hotspot')) {
				var cursor_at = $(ui.draggable).data('IShopCursorAt')['cursorAt'];
				$(ui.helper).css({
					"z-index":1005,
					"opacity": 1
				}).append('<span style="display: block;width: 31px;height: 31px;background: url(\'images/icon-ready-to-drop.png\') no-repeat 0 0;color: #fff;position:	absolute;top: '+(cursor_at.top - 14)+'px;left: '+(cursor_at.left-14)+'px;z-index: 1006;"></span>');
			}
		},
		tolerance: "pointer",
		out: function( event, ui ) {
			$(ui.helper).css({ 
				opacity: 0.5,
				"border":	0
			});
			$(ui.helper).find('span').remove();
		},
		drop: function( event, ui ) {
			var canvas = $(this).data('IShopCanvas');
			if (canvas.background_id == undefined || canvas.background_id == 0) {
				// here we are sure we set canvas background
				var asset = $(ui.helper.context).closest('li').data('IShopAsset');
				canvas.background_id = asset.id;
				IShopRest.new_saveCanvas(canvas);
				IShopNewGuideline.applyNewCanvasBackground( this, asset );
				IShopNewGuideline.applyNewCanvasThumbBackground( $('#guideline-canvas-thumbs li.active'), asset );
			}
			else {
				// either we are dragging hotspot or asset
				if ($(ui.draggable).hasClass('canvas-hotspot')) {
					//we are dragging hotspot
					var hotspot = $(ui.draggable).data('IShopHotspot');
					var background_size = $(this).data('IShopCanvasSize');
					var hotspot_slant = $(this).data('IShopCanvasHotspotOffset');
					var base = $(this).offset();
					var mx = ui.offset.left - base.left + 12;
					var my = ui.offset.top - base.top + 12;
					var px = (100*mx/$(this).width());
					var py = (100*my/$(this).height());
					var cursor_at = $(ui.draggable).data('IShopCursorAt');
					hotspot.posx = px;
					hotspot.posy = py;
					IShopRest.new_saveAsset($(this).data('IShopCanvas'), hotspot);
				}
				else {
					var hotspot_slant = $(this).data('IShopCanvasHotspotOffset');
					var background_size = $(this).data('IShopCanvasSize');
					var cursor_at = $(ui.draggable).data('IShopCursorAt').cursorAt;
					var base = $(this).offset();
					var mx  = ui.offset.left - base.left + cursor_at.left;
					var my  = ui.offset.top - base.top + cursor_at.top;
					var px  = 100*mx/$(this).width();
					var py  = 100*my/$(this).height();
					var asset = $(ui.helper.context).closest('li').data('IShopAsset');
					var order = parseInt($(this).find('.canvas-hotspot').length) + 1;
					var hotspot = {
						"asset": asset,
						"order": order,
						"quantity": 8,
						"posx": px,
						"posy": py
					};
					
					IShopRest.new_saveAsset($(this).data('IShopCanvas'), hotspot);
					var spot = $('<div rel="'+hotspot.order+'" class="canvas-hotspot" style="top: ' + (py - hotspot_slant.offset_y) + '%; left: '+(px - hotspot_slant.offset_x) +'%;"><span></span></div>');
					$(spot).data('IShopHotspot', hotspot);
					$(spot).data('IShopCursorAt', cursor_at);
					$(this).append(spot);
					IShopNewGuideline.MapHotspotOnProductList($(this).data('IShopCanvas'), hotspot);
				}
			}
		}
	});
};

IShopNewGuideline.MapHotspotOnProductList = function(canvas, hotspot) {
	IShopNewGuideline.markUsedAssets();
	var accordion_body = $('.plc-list ul').get(canvas.order);
	
	var product_number = hotspot.asset.type == 'Product' ? hotspot.asset.product_number : '';
	var image_src = hotspot.asset.image_name + '=s' + IShopHelper.determineImageSize(hotspot.asset, 65, 70);

	var asset_box = $('<li rel="'+hotspot.order+'"><dl class="asset-box"><dt>'+hotspot.asset.name+'</dt><dd class="ab-date">'+product_number+'<span>'+hotspot.asset.creation_date+'</span></dd><dd class="ab-image"><div><img src="'+image_src+'"><em class=""></em></div></dd><dd class="ab-tags">'+IShopNewGuideline.getAssetTagsHtml(hotspot.asset)+'</dd><dd class="ab-quantity-changer"><span class="abqc-sbc qc-pl-sbc"></span><span class="abqc-value">'+hotspot.quantity+'</span><span class="abqc-add qc-pl-add"></span></dd></dl></li>')
	.data('IShopHotspot', hotspot)
	.appendTo($(accordion_body));
	
};

IShopNewGuideline.setActiveCanvas = function(id) {
	$('.guideline-canvas').css('z-index', 1000).droppable( "option", "disabled", true );
	$($('.guideline-canvas').get(id)).css('z-index', 1002).droppable( "option", "disabled", false );
};

IShopNewGuideline.showHotspotPopup = function(hotspot_element) {
	$('.hotspot-popup').remove();
	var hotspot = $(hotspot_element).data('IShopHotspot');
	var canvas = $(hotspot_element).parent();

	var px = $(hotspot_element).position().left;
	var py = $(hotspot_element).position().top;
	
	var dist_to_top	=	py;
	var dist_to_bottom	=	$(canvas).height() - py;
	var dist_to_left	=	px;
	var dist_to_right	=	$(canvas).width() - px;
	
	var hor, vert, class_hor, class_vert, _class;
	
	if (dist_to_left > dist_to_right) {
		hor = dist_to_left;
		class_hor	=	'right';
	}
	else {
		hor = dist_to_right;
		class_hor	=	'left';
	}
	
	if (dist_to_top > dist_to_bottom) {
		vert = dist_to_top;
		class_vert	=	'bottom';
	}
	else {
		vert = dist_to_bottom;
		class_vert	=	'top';
	}
	
	if (hor < vert) {
		_class = class_vert;
	}
	else {
		_class = class_hor;
	}
	
	
	var slant_x, slant_y;
	
	if (_class == 'left') {
		slant_x	=	30;
		slant_y	=	-62;
	}
	else if (_class == 'right') {
		slant_x	=	-320;
		slant_y	=	-62;	
	}
	else if (_class == 'top') {
		slant_x	=	-146;
		slant_y	=	35;
	}
	else if (_class == 'bottom') {
		slant_x	=	-147;
		slant_y	=	-155;
	}	
	
	px += slant_x;
	py += slant_y;
	
	//console.log(hotspot);
	
	var product_number = hotspot.asset.type == 'Product' ? hotspot.asset.product_number : '';
	var image_src = hotspot.asset.image_name + '=s' + IShopHelper.determineImageSize(hotspot.asset, 65, 70);
	/*
	var popup = $('<div class="hotspot-popup '+_class+'"><div class="hp-gutter"><dl class="asset-box"><dt>'+hotspot.asset.name+'</dt><dd class="ab-date">'+product_number+'<span>'+hotspot.asset.creation_date+'</span></dd><dd class="ab-image"><div><img src="'+image_src+'"><em class=""></em></div></dd><dd class="ab-tags">'+IShopNewGuideline.getAssetTagsHtml(hotspot.asset)+'</dd><dd class="ab-quantity-changer"><span class="abqc-sbc qc-hp-sbc"></span><span class="abqc-value">'+hotspot.quantity+'</span><span class="abqc-add qc-hp-add"></span></dd></dl><p class="hp-close">x</p><p class="hp-delete">Delete</p></div></div>').css({"top": py, "left": px}).data('IShopHotspot', hotspot).appendTo($(canvas));
	*/
	
	var popup = $('<div class="hotspot-popup '+_class+'"><div class="hp-gutter"><dl class="asset-box"><dt>'+hotspot.asset.name+'</dt><dd class="ab-date">'+product_number+'<span>'+hotspot.asset.creation_date+'</span></dd><dd class="ab-image"><div><img src="'+image_src+'"><em class=""></em></div></dd><dd class="ab-tags"></dd><dd class="ab-quantity-changer"><span class="abqc-sbc qc-hp-sbc"></span><span class="abqc-value">'+hotspot.quantity+'</span><span class="abqc-add qc-hp-add"></span></dd></dl><p class="hp-close">x</p><p class="hp-delete">Delete</p></div></div>').css({"top": py, "left": px}).data('IShopHotspot', hotspot).appendTo($(canvas));	
	
	
};

IShopNewGuideline.toggleAccordionSection = function(id) {
	$($('.pl-canvas').get(id)).guidelineAccordion('toggleSection');
};

IShopNewGuideline.openAccordionSection = function(id) {
	$($('.pl-canvas').get(id)).guidelineAccordion('openSection');
};

IShopNewGuideline.closeAccordionSection = function(id) {
	$($('.pl-canvas').get(id)).guidelineAccordion('closeSection');
};

IShopNewGuideline.closeAllAccordionSections = function() {
	$('.pl-canvas').each(function() {
		$(this).guidelineAccordion('closeSection');
	});
};

IShopNewGuideline.openAllAccordionSections = function() {
	$('.pl-canvas').each(function() {
		$(this).guidelineAccordion('openSection');
	});
};

IShopNewGuideline.sendGuidelineToServer = function() {
	IShopRest.new_saveGuideline(IShopNewGuideline.getGuideline());
};

IShopNewGuideline.getGuideline = function() {
	var guideline = jQuery.extend(true, {}, this.guideline);
	var hotspot;
	var asset;
	$.each(guideline.canvases, function(canvas_nr, canvas) {
		$($('.guideline-canvas').get(canvas_nr)).find('.canvas-hotspot').each(function() {
			hotspot = $(this).data('IShopHotspot');
			asset = jQuery.extend(true, {}, hotspot.asset);
			asset.posx = hotspot.posx;
			asset.posy = hotspot.posy;
			asset.order = hotspot.order;
			asset.quantity = hotspot.quantity;
			canvas.assets.push(asset);
		});
	});
	return guideline;
};

IShopNewGuideline.getUsedAssetsIds = function() {
	var used_ids = {};
	$.each(IShopNewGuideline.getGuideline().canvases, function(canvas_nr, canvas) {
		if (canvas.background_id != 0 ) {
			// add background_id to used ids
			used_ids[canvas.background_id] = 1;
			$.each(canvas.assets, function(asset_nr, asset) {
				used_ids[asset.id] = 1;
			});
		}
	});
	return used_ids;
};

IShopNewGuideline.markUsedAssets = function() {

	if ($('#media-browser').length == 0) {
		return false;
	}

	var used_ids = IShopNewGuideline.getUsedAssetsIds();
	$('.ab-image em').addClass('hidden');
	var asset;
	var elem;
	$('#mbal-gutter li').each(function() {
		asset = $(this).data('IShopAsset');
		elem = this;
		$.each(used_ids, function(used_id, value) {
			if (used_id == asset.id) {
				$(elem).find('em').removeClass('hidden');
			}
		});
	});
};

/** 						05.03.2011						   **/

IShopNewGuideline.initGuidelineView = function(guideline_id) {
	this.addEvents();
	
	$('#canvas-wrapper').css('opacity', 0);
	
	// get guideline id from html element.
	var guideline = IShopRest.getGuidelineById($('#guideline-id').attr('rel'));
	this.prepareViewForm(guideline);
	this.prepareViewBackgrounds(guideline);
	window.setTimeout(function() {
		$($('#guideline-canvas-thumbs li').get(0)).trigger('click');
		IShopNewGuideline.prepareViewCanvasHotspots(guideline);
		window.setTimeout(function() {
			$('#canvas-wrapper').animate({
				"opacity": 1
			}, {
				"duration": 500,
				"complete": function() {
					IShopNewGuideline.toggleAccordionSection(0);
				}
			});
		}, 1000);
	}, 2000);
	

};

IShopNewGuideline.prepareViewForm = function(guideline) {
	$('#gdf-name').val(guideline.name).attr('disabled', true);
	$('#gdf-due_date').val(guideline.due_date).attr('disabled', true);
	$('#gdf-description').val(guideline.description).attr('disabled', true);
	$('#gdf-photo_required').attr('disabled', true);
	if (guideline.photo_required === true) {
		$('#gdf-photo_required').attr('checked', 'checked');
	} 
};

IShopNewGuideline.prepareViewBackgrounds = function(guideline) {
	$.each(guideline.canvases, function(id, _g) {
		//console.log(_g);
		var asset = {
			"image_name": _g.background_name,
			"image_ratio": _g.image_ratio,
			"image_width": _g.image_width,
			"image_heigth": _g.image_heigth
		};
		
		IShopNewGuideline.applyNewCanvasBackground( ($('.guideline-canvas').get(_g.order)), asset );
		IShopNewGuideline.applyNewCanvasThumbBackground( ($('#guideline-canvas-thumbs li').get(_g.order)), asset );
	});
	
	
};

IShopNewGuideline.prepareViewCanvasHotspots = function(guideline) {
	var canvas_element;
	var spot, hotspot, ppx, ppy;
	$.each(guideline.canvases, function(canvas_nr, canvas) {
		
		canvas_element = $('.guideline-canvas').get(canvas.order);
		ppx = 14/($(canvas_element).width()) * 100;
		ppy = 14/($(canvas_element).height()) * 100;

		$.each(canvas.assets, function(asset_nr, asset) {
			
			asset.creation_date = "";
			asset.image_name = asset.product_image_name;
			asset.name = asset.product_name;
			asset.type = 'Product';
			
			//console.log(hotspot);
			
			hotspot = {
				"posx": asset.posx,
				"posy": asset.posy,
				"quantity": asset.quantity,
				"asset": asset
			};
			
			spot = $('<div class="canvas-hotspot" style="top: '+(asset.posy - ppy)+'%; left: '+(asset.posx - ppx)+'%;"><span></span></div>').data('IShopHotspot', hotspot);
			$(canvas_element).append(spot);
			
			IShopNewGuideline.MapHotspotOnProductList(canvas, hotspot);
			
		});
		
		
	});
};

IShopNewGuideline.addCursorsAt = function() {
};


IShopNewGuideline.addCursorsAtOld = function() {
	var active = $('#mbs-assets-selector li.active').text().toLowerCase();
	//mbalg-fixtures
	var w, h, optionz;
	
	$('#mbalg-' + active + ' li img').each(function() {
		$(this).load(function() {
			IShopNewGuideline.getCursorAt(this);
			w = Math.round(($(this).width())/2);
			h = Math.round(($(this).height())/2);
			var optionz = IShopNewGuideline.getCursorAt(this);
			//console.log($(this).parent());
			$(this).parent().data('IShopCursorAt', optionz).draggable(optionz);
		});
	});
	
	IShopNewGuideline.addCursorsAt = IShopNewGuideline.addCursorsAtNew;
};

IShopNewGuideline.addCursorsAtNew = function() {
	var active = $('#mbs-assets-selector li.active').text().toLowerCase();
	var w, h;
	$('#mbalg-' + active + ' li img').each(function() {
		var optionz = IShopNewGuideline.getCursorAt(this);
		$(this).parent().data('IShopCursorAt', optionz).draggable(optionz);
	});
};







IShopNewGuideline.getCursorAt = function(t) {
	w = Math.round(($(t).width())/2);
	h = Math.round(($(t).height())/2);
	return {
		"cursorAt": {
			"top": h,
			"left": w
		}
	};
};








