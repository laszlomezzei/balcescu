//fix IE8 Array issues
//Add ECMA262-5 Array methods if not supported natively
//http://stackoverflow.com/questions/2790001/fixing-javascript-array-functions-in-internet-explorer-indexof-foreach-etc
if (!('indexOf' in Array.prototype)) {
    Array.prototype.indexOf= function(find, i /*opt*/) {
        if (i===undefined) i= 0;
        if (i<0) i+= this.length;
        if (i<0) i= 0;
        for (var n= this.length; i<n; i++)
            if (i in this && this[i]===find)
                return i;
        return -1;
    };
}

var IShopGuidelines = {};

IShopGuidelines.init = function(guidelines) {
	// ==================> we are @ by guideline dashboard page <=============
	//console.log(guidelines);
	if ($('#page-type').val() == 'by_guideline') {
	
		$.each( guidelines, function(id, guideline) {
			IShopGuidelines.createAccordionRowHtml(guideline);
		});
		
		// add accordion events
		$('.gol-row-header').bind('click', function(ev) {
			$(this).next().slideToggle(function() {
				$(this).prev().toggleClass('active');
			});
		});
		
		IShopGuidelines.openAllAccordionRows();
		
		// add clicks to grid-list views
		
		$('#vs-grid').click(function() {
			$('#vs-grid, #vs-list').removeClass('active');
			$(this).addClass('active');
			IShopGuidelines.openAllAccordionRows();
		});
		
		$('#vs-list').click(function() {
			$('#vs-grid, #vs-list').removeClass('active');
			$(this).addClass('active');
			IShopGuidelines.closeAllAccordionRows();
		});		
		
		
		
		// open first accordion section
		//$($('.gol-row-center').get(0)).show();
		//$($('.gol-row-header').get(0)).addClass('active');
		
	}
	// ==================> we are @ by date dashboard page <==================
	else {
		var dl_row;
		var label;
		
		$.each( guidelines, function(id, guideline) {
			dl_row = IShopGuidelines.getRowDlHtml(guideline);
			
			label = $('<div class="grc-label"><div class="grcl-gutter"><h2>'+guideline.guideline_name+'</h2><h3>'+(guideline.update_date == null ? '' : guideline.update_date)+'</h3></div></div>').hide();
			//console.log(dl_row);
			
			// add progressive hover functionality
			$(dl_row).data('IShopFeedbackStory', guideline).append(label).appendTo('.gol-row-center');
			// add mouseover for showing labels
		});
		
		$('.progressive-hover-overlay').die('mouseover');
		$('.progressive-hover-overlay').die('mouseout');
		$('.progressive-hover-overlay').live({
			"mouseover": function() {
				$(this).closest('dl').find('.grc-label').show();
			},
			"mouseout": function() {
				$(this).closest('dl').find('.grc-label').hide();
			}
		});
		$('.gol-row-center dl').progressiveHover();
	}

	
	
	// this is small hack for setting on setting dl's rel corresponding with the 
	// onhovered image offset. used to set the carousel active image within the popup
	//
	$('.progressive-hover-overlay').die('mouseover');
	$('.progressive-hover-overlay').live('mouseover', function() {
		$(this).closest('dl').attr('rel', $(this).attr('rel'));
	});
	
	$('.gol-row-center dl.no-empty').die('click');

	$('.gol-row-center dl.no-empty').live('click', function() {
		IShopGuidelines.openDashboardDialogPopup( $(this).data('IShopFeedbackStory'), this );
	});
	

	$('#ddp-close').die('click');
	$('#ddp-close').live('click', function() {
		IShopGuidelines.removeDashboardDialogPopup();
	});
	
	//delete Guideline click
	$('.view_guideline').die('click');
	$('.view_guideline').live('click', function(event) {
		event.stopPropagation();
		var guideline_id = $(this).data('id');
		IShopGuidelines.openGuidelinePopup( $(this).data('id'), this );
		//IShopRest.deleteGuideline(guideline_id);
		//window.location = window.location.href;
	});
	
	
	//delete Guideline click
	$('.delete_guideline').die('click');
	$('.delete_guideline').live('click', function() {
		if(confirm("Delete guideline?"))
			{
				
				var guideline_id = $(this).data('id');
				
				IShopRest.deleteGuideline(guideline_id);
				$(this).closest('.gol-row').remove();
			}
	});

    $('.gl-delete input').die('click');
	$('.gl-delete input').live('click', function(ev) {
		var asset = $('.gl-delete input').closest('li').prev().data('IShopAsset');
		// remove asset from database
		IShopRest.removeAsset(asset.id);
		// remove asset from list
		$('.gl-delete input').closest('li').prev().remove();
		IShopGuidelines.removeAllActiveRows();
	});
	
	$('.gl-cancel').die('click');
	$('.gl-cancel').live('click', function(ev) {
		IShopGuidelines.removeAllActiveRows();
	});	

	//reply to conversation
    $('#btnGuidelineReply').die('click');
	$('#btnGuidelineReply').live('click',function() {
		
		var id = $(this).data('id');
		var storeid = $(this).data('storeid');
		var feedback = {"id":id,
			"creation_date":new Date(),
			"guideline_id":id,
			"store_id":storeid,
			"feedback":$('#txtGuidelineMessage').val()
			};
		//send to be saved
		IShopRest.new_saveGuidelineFeedback(feedback);
		//refresh conversations
		var chat_section = $('#ddpg-chat');
		var conversations = IShopRest.getDashboardConversations({guideline_id:id,store_id:storeid})["data"];
		IShopGuidelines.prepareConversationImages(conversations);
		chat_section.html($('#templateGuidelineFeedbacksChats').render({conversations:conversations}));
		IShopGuidelines.updateImagesPosition();
		//IShopGuidelines.renderDashboardPopupChat(chat_section,conversations);
		//empty box
		$('#txtGuidelineMessage').val("");
		
	});
	$('#loading').hide();
};

IShopGuidelines.getRowDlHtml = function(guideline) {
	//console.log(guideline);
	var clazz = guideline.unread ? 'class="read-mark unread"' : 'class="read-mark"';
	var _em;
	//var _empty_class = guideline.images.length == 0 ? '' : ' class="no-empty" ';
	//Laci Issue #40
	var _empty_class = guideline.message_count == 0 ? '' : ' class="no-empty" ';
	if (guideline.message_count !== 0) {
		_em = '<em '+clazz+'><span>'+guideline.message_count+'</span></em>';
	}
	else {
		_em = '';
	}
	var row = '<dl'+_empty_class+'><dt>'+guideline.store_name+'</dt>'+IShopGuidelines.getRowImagesHtml(guideline)+_em+'</dl>';
	return row;
};

IShopGuidelines.getRowImagesHtml = function(guideline) {
	var html = '';
	//console.log(guideline.images.length);
	$.each(guideline.images, function(id, image) {
		var img_path = image.url + '=s' + IShopHelper.determineImageSize(image, 210, 160);
		html += '<dd class="off"><img src="' + img_path + '" /></dd>';
	});
	if (html == '') {
		html += '<dd><img src="/static/images/guidelines_back_emty_feedback.png" style="top: -7px !important; left: -5px;position: absolute;width:220px;height: 172px;"/></dd>';
	}
	return html;
};

IShopGuidelines.createAccordionRowHtml = function(guideline) {
	var response_color = 'red';
	if (guideline.response_rate > 50) {
		response_color = 'orange';
	}
	if (guideline.response_rate > 75) {
		response_color = 'green';
	}
	//<input class="delete_guideline" data-id="'+guideline.guideline_id+'" type="Button" value="Delete" >&nbsp;
	var row = $('<div class="gol-row"><div class="gol-row-header">'+
			'<h2>'+guideline.guideline_name+
			'&nbsp;<a data-id="'+guideline.guideline_id+'" href="#" class="gl-view view_guideline" style="margin-top:1px;"></a>'+//view link
			'&nbsp;<a data-id="'+guideline.guideline_id+'" href="#" class="gl-delete delete_guideline" style="margin-left:21px;"></a>'+//delete button
			'</h2>'+
			'<h3>'+guideline.guideline_due_date+'</h3><h4><span class="gol-row-header-rating-number '+response_color+'">'+guideline.response_rate+'%</span><span class="gol-row-header-rating-desc">RESPONSE<br />RATE</span></h4></div><!-- .gol-row-header --><div class="gol-row-center"></div><!-- .gol-row-center --></div><!-- .gol-row -->');
	
	$('.aola-delete').live('click', function(ev) {
		$('.aola-delete').removeClass('active');
		$(this).addClass('active');	
		li_element = $(this).closest('li');
		IShopGuidelines.createDeleteRow(li_element);
	});
	
	var dl_row;
	$.each(guideline.conversations, function(id, feedback_story) {
		var dl_row = IShopGuidelines.getRowDlHtml(feedback_story);
		$(dl_row).data('IShopFeedbackStory', feedback_story).appendTo($(row).find('.gol-row-center'));
	});
	$(row).find('.gol-row-center').hide();
	$(row).data('IShopGuideline', guideline).appendTo('#guideline-overview-list-gutter');
	$('.gol-row-center dl').progressiveHover();
};

IShopGuidelines.createDeleteRow = function(list_element) {
	this.removeAllActiveRows();
	var asset = $(list_element).data('IShopAsset');
	var html = $('<li class="aol-edit aactive red"><div class="aole-gutter"><p class="aole-info"><strong>Delete group and all its tags?</strong></p><p class="aole-cancel">Cancel</p> <p class="aole-button aole-delete"><input type="image" src="/database/images/button-red-delete.png" /></p></div></li>');
	$(html).hide();
	$(list_element).after($(html));
	$(html).slideDown();
};

IShopGuidelines.openGuidelinePopup = function(guideline_Id) {
	$('#screen-white-overlay').css({
		"opacity": 0,
		"display": "block"
	}).removeClass('hidden').animate({
		"opacity": 0.8
	}, {
		"duration": 300,
		"complete": function() {
			var guideline = IShopRest.getGuidelineById(guideline_Id)["data"][0];
			//console.log(guideline.name);
			//console.log(guideline.description);
			
			for(var i=0; i<guideline.canvases.length; i++){
				var asset={image_ratio:guideline.canvases[i]["image_ratio"], image_width:guideline.canvases[i]["background_width"], image_height:guideline.canvases[i]["background_height"]};
				
				var background_size = IShopHelper.getImageSize(asset, 640, 434);
				var th_background_size = IShopHelper.getImageSize(asset, 105, 68);
				background_size.width = background_size.width + 8;
				background_size.height = background_size.height + 8;
				var c_left = (640 - background_size.width)/2;
				var c_top = (434 - background_size.height)/2;
				var size = '=s' + IShopHelper.determineImageSize(asset, 640, 434);
				
				
				var th_size = '=s' + IShopHelper.determineImageSize(asset, 105, 68);
				var th_c_left = (105 - th_background_size.width)/2;
				var th_c_top = (68 - th_background_size.height)/2;
				
				guideline.canvases[i]["image_info"] = { width:background_size.width,
						height:background_size.height, 
						left:c_left, 
						top:c_top,
						size:size,
						thumb_width:th_background_size.width, 
						thumb_height:th_background_size.height, 
						thumb_left:th_c_left, 
						thumb_top:th_c_top,
						thumb_size:th_size
					};
			}
			
			IShopGuidelines.renderGuidelinePopup(guideline);
			IShopGuidelines.addEvents();
			IShopGuidelines.closeAllAccordionSections();
			IShopGuidelines.openAccordionSection(0);
		}
	});
	
	// add popup events
	
};


IShopGuidelines.renderGuidelinePopup=function(guideline)
{
	$('#main-content').append($('#templateGuidelinePopup').render({ guideline : guideline }));
	IShopGuidelines.slidePopupToScrollTop();
}


IShopGuidelines.openDashboardDialogPopup = function(guideline, dl_elem) {
	
	
	$('#screen-white-overlay').css({
		"opacity": 0,
		"display": "block"
	}).removeClass('hidden').animate({
		"opacity": 0.8
	}, {
		"duration": 300,
		"complete": function() {
			IShopGuidelines.renderDashboardDialogPopup(guideline, dl_elem);
		}
	});
	
	$(dl_elem).find('.read-mark').removeClass('unread');
};

IShopGuidelines.prepareConversationImages = function(conversations){
	for(var i = 0; i<conversations.length; i++){
		var conversation = conversations[i];
		for(var j=0; j<conversation.images.length; j++){
			var image = conversation.images[j];
			image["url"] += '=s' + IShopHelper.determineImageSize(image, 790, 460);
		}
		conversation["userrole"] = conversation.user_roles.indexOf('STORE')>-1 ? 'store' : 'hq';
	}
}

IShopGuidelines.renderDashboardDialogPopup=function(guideline, dl_elem)
{
	var conversations = IShopRest.getDashboardConversations(guideline)["data"];
	IShopGuidelines.prepareConversationImages(conversations);
	//var popup_wrapper = IShopGuidelines.createDashboardPopupWrapper(guideline);
	
	$($('#templateGuidelineFeedbacksPopup').render({guideline:guideline, conversations:conversations})).appendTo('#main-content');

	IShopGuidelines.slidePopupToScrollTop();
	IShopGuidelines.updateImagesPosition();
	

	
}

IShopGuidelines.updateImagesPosition = function(){
	var popup_wrapper = '#dashboard-dialog-popup';
	

//	$(popup_wrapper).
//		find('#ddp-gutter')
//		.append(IShopGuidelines.createDashboardPopupTitle(guideline))
//		.append(IShopGuidelines.createDashboardPopupChat(conversations))
//		.append(IShopGuidelines.createDashboardPopupCarousel(guideline))
//		.append(IShopGuidelines.createDashboardPopupReply(guideline));
//		
	var carousel_states = [];
	
	$('div[id^="ddpg-photos"]').each(function(index, conv){
		var carousel_state = {
				"id":conv.id.replace("ddpg-photos",""),
				"active_item": 0,
				"items_total": $(conv).find('img').length - 1
			};
		carousel_states.push(carousel_state);
	})
	
	
	
	//$(popup_wrapper).find('.ddpg-photos img').hide();
	$(popup_wrapper).data('IShopCarouselState', carousel_states);
	

	// add popup events
	
	$('div[id^="ddpg-carousel-next"]').each(function(index, elem){
		$(elem).die('click');
		$(elem).live('click', function() {
			var carousel_state = $('#dashboard-dialog-popup').data('IShopCarouselState')[index];
			if (carousel_state.active_item < carousel_state.items_total) {
				carousel_state.active_item ++;
			}
			IShopGuidelines.showCarouselImage(carousel_state.id, carousel_state.active_item);
		})
	});
	
	$('div[id^="ddpg-carousel-prev"]').each(function(index, elem){
		$(elem).die('click');
		$(elem).live('click', function() {
			var carousel_state = $('#dashboard-dialog-popup').data('IShopCarouselState')[index];
			if (carousel_state.active_item > 0) {
				carousel_state.active_item --;
			}
			IShopGuidelines.showCarouselImage(carousel_state.id, carousel_state.active_item);
		})
	});
	
	// add pagination events
	$('ul[id^="ddpg-paginator"]').each(function(index, elem){
		$(elem).find('li').live('click', function() {
			$('#dashboard-dialog-popup').data('IShopCarouselState')[index].active_item = $(this).attr('rel');
			IShopGuidelines.showCarouselImage($('#dashboard-dialog-popup').data('IShopCarouselState')[index].id, $(this).attr('rel') );
		})
	});
	
	for(var i=0; i<carousel_states.length; i++){
		IShopGuidelines.showCarouselImage(carousel_states[i].id, 0);
	}
	
	var _top, _left, _w, _h;
	$(popup_wrapper).find('.ddpg-photos img').each(function() {
		$(this).load(function() {
			_w = $(this).width();
			_h = $(this).height();
			_t = (460 - _h) /2;
			_l = (790 - _w) /2;
			$(this).css({
				"top": _t,
				"left": _l
			});
		});
	});
	
	
}
IShopGuidelines.showCarouselImage = function(conversation_id, id) {

	var images = $('#ddpg-photos'+conversation_id+' img');
	var active = images.splice(id, 1);
	$(images).fadeOut();
	$(active).fadeIn();
	$('#ddpg-paginator'+conversation_id+' li').removeClass('active');
	$($('#ddpg-paginator'+conversation_id+' li').get(id)).addClass('active');
	
	$('#ddpg-carousel-prev'+conversation_id+',#.ddpg-carousel-next'+conversation_id+'').removeClass('inactive');
	if ( id == 0 ) {
		$('#ddpg-carousel-prev'+conversation_id+'').addClass('inactive');
	}
	
	var carousel_states = $('#dashboard-dialog-popup').data('IShopCarouselState');
	for(var i=0; i<carousel_states.length; i++){
		if (carousel_states[i].id==conversation_id && id == carousel_states[i].items_total ) {
			$('#ddpg-carousel-next'+conversation_id+'').addClass('inactive');
			break;
		}
	}
};


IShopGuidelines.removeDashboardDialogPopup = function() {
	$('#dashboard-dialog-popup').fadeOut().remove();
	$('#screen-white-overlay').fadeOut();
};

//
//IShopGuidelines.createDashboardPopupWrapper = function(guideline) {
//	var wrapper = $('<div id="dashboard-dialog-popup"><div id="ddp-gutter"></div><div id="ddp-footer"></div><br><br><img id="ddp-close" src="/images/ngd_button_close_canvas.png" alt="Close popup" /></div>');
//	return wrapper;
//};
//
//IShopGuidelines.createDashboardPopupTitle = function(guideline) {
//	return $('<div id="ddpg-title"><h2>'+guideline.guideline_name+'</h2></div><!-- ddpg-title -->');
//};
//
//IShopGuidelines.createDashboardPopupCarousel = function(guideline) {
//	var photos = $('<div id="ddpg-photos"></div>');
//	$.each(guideline.images, function(id, image) {
//		var img_path = image.url + '=s' + IShopHelper.determineImageSize(image, 790, 460);
//		$('<img src="' + img_path + '" alt="" />').appendTo($(photos));
//	});
//	$(photos)
//		.append($(IShopGuidelines.createDashboardPopupCarouselPaginator(guideline)))
//		.append($('<div id="ddpg-carousel-prev"></div><div id="ddpg-carousel-next"></div>'));
//	return $(photos);
//};
//
////dan
//IShopGuidelines.createDashboardPopupReply = function(guideline) {
//	var avatar = '/images/avatar_hq.png';
//	return $('#templateGuidelineReply').render({ avatar : avatar, id:guideline.guideline_id, storeid:guideline.store_id });
//};
//
//IShopGuidelines.createDashboardPopupCarouselPaginator = function(guideline) {
//	var paginator = $('<ul id="ddpg-paginator"></ul>');
//	$.each(guideline.images, function(id, image) {
//		$('<li rel="'+id+'"></li>').appendTo($(paginator));
//	});
//	$($(paginator).find('li').get(0)).addClass('active');
//	return $(paginator);
//};
//
//IShopGuidelines.createDashboardPopupChat = function(conversations) {
//	var chat_section = $('<div id="ddpg-chat"></div>');
//	return IShopGuidelines.renderDashboardPopupChat(chat_section,conversations);
//};

//
//IShopGuidelines.renderDashboardPopupChat = function(chat_section,conversations) {
//	
//	var row;
//	$.each(conversations, function(id, comment) {
//		/*
//		row = IShopGuidelines.createDashboardPopupChatRow('in', comment);
//		*/
//		
//		if (comment.user_roles.indexOf('STORE')>-1) {
//			//row = IShopGuidelines.createDashboardPopupChatRow('in', comment);
//			row = $('#templateGuidelineReplySTORE').render({comment:comment});
//		}
//		else {
//			//row = IShopGuidelines.createDashboardPopupChatRow('out', comment);
//			row = $('#templateGuidelineReplyHQ').render({comment:comment});
//		}
//		
//		$(chat_section).append($(row));
//	});
//	return chat_section;
//};
//
//IShopGuidelines.createDashboardPopupChatRow = function(clazz, comment) {
//	var avatar = clazz == 'in' ? '/images/avatar_store.png' : '/images/avatar_hq.png';
//	var row = '<div class="ddpg-chat-row '+clazz+'"><div class="ddpgcr-title"><h3><strong>'+comment.store_name+'</strong>, '+comment.store_address+'</h3><em>'+comment.creation_date+'</em><p>'+comment.feedback+'</p></div><div class="ddpgcr-arrow"></div><div class="ddpgcr-avatar"><img src="'+avatar+'" /></div></div>';
//	return row;
//};


IShopGuidelines.openAllAccordionRows = function() {
	$('.gol-row-header').each(function() {
		$(this).next().slideDown(function() {
			$(this).prev().addClass('active');
		});
	});
};

IShopGuidelines.closeAllAccordionRows = function() {
	$('.gol-row-header').each(function() {
		$(this).next().slideUp(function() {
			$(this).prev().removeClass('active');
		});
	});
};

IShopGuidelines.slidePopupToScrollTop = function() {

	var _top = $(window).scrollTop() - 25 + 'px';
	$('#dashboard-dialog-popup').stop().animate(
			{'top': _top},
			1000,
			function(){ //on complete animation, bring into view the Reply area
				if($(window).height() < $('#dashboard-dialog-popup').height()) 
					{location.href = '#lnkReply';}
			}
	);
};
//
//IShopGuidelines.showHotspotPopup = function(hotspot_element) {
//	$('.hotspot-popup').remove();
//	var hotspot = $(hotspot_element).data('IShopHotspot');
//	var canvas = $(hotspot_element).parent();
//
//	var px = $(hotspot_element).position().left;
//	var py = $(hotspot_element).position().top;
//	
//	var dist_to_top	=	py;
//	var dist_to_bottom	=	$(canvas).height() - py;
//	var dist_to_left	=	px;
//	var dist_to_right	=	$(canvas).width() - px;
//	
//	var hor, vert, class_hor, class_vert, _class;
//	
//	if (dist_to_left > dist_to_right) {
//		hor = dist_to_left;
//		class_hor	=	'right';
//	}
//	else {
//		hor = dist_to_right;
//		class_hor	=	'left';
//	}
//	
//	if (dist_to_top > dist_to_bottom) {
//		vert = dist_to_top;
//		class_vert	=	'bottom';
//	}
//	else {
//		vert = dist_to_bottom;
//		class_vert	=	'top';
//	}
//	
//	if (hor < vert) {
//		_class = class_vert;
//	}
//	else {
//		_class = class_hor;
//	}
//	
//	
//	var slant_x, slant_y;
//	
//	if (_class == 'left') {
//		slant_x	=	30;
//		slant_y	=	-62;
//	}
//	else if (_class == 'right') {
//		slant_x	=	-320;
//		slant_y	=	-62;	
//	}
//	else if (_class == 'top') {
//		slant_x	=	-146;
//		slant_y	=	35;
//	}
//	else if (_class == 'bottom') {
//		slant_x	=	-147;
//		slant_y	=	-155;
//	}	
//	
//	px += slant_x;
//	py += slant_y;
//	
//	//console.log(hotspot);
//	
//	var product_number = hotspot.asset.type == 'Product' ? hotspot.asset.product_number : '';
//	var image_src = $(this).data("imgsrc") + '=s' + IShopHelper.determineImageSize(hotspot.asset, 65, 70);
//	/*
//	var popup = $('<div class="hotspot-popup '+_class+'"><div class="hp-gutter"><dl class="asset-box"><dt>'+hotspot.asset.name+'</dt><dd class="ab-date">'+product_number+'<span>'+hotspot.asset.creation_date+'</span></dd><dd class="ab-image"><div><img src="'+image_src+'"><em class=""></em></div></dd><dd class="ab-tags">'+IShopNewGuideline.getAssetTagsHtml(hotspot.asset)+'</dd><dd class="ab-quantity-changer"><span class="abqc-sbc qc-hp-sbc"></span><span class="abqc-value">'+hotspot.quantity+'</span><span class="abqc-add qc-hp-add"></span></dd></dl><p class="hp-close">x</p><p class="hp-delete">Delete</p></div></div>').css({"top": py, "left": px}).data('IShopHotspot', hotspot).appendTo($(canvas));
//	*/
//	
//	var popup = $('#templateHotspotPopup').render(class:_class, asset:asset).css({"top": py, "left": px}).data('IShopHotspot', hotspot).appendTo($(canvas));	
//	
//};
//
//IShopGuidelines.destroyHotspotPopup = function() {
//	$('.hotspot-popup').animate({
//		opacity: 0
//	}, {
//		duration: 300,
//		complete: function() {
//			$(this).remove();
//		}
//	});
//};


IShopGuidelines.addEvents = function() {
	$('.pl-canvas').guidelineAccordion();
	$('.guideline-canvas').css('opacity',0).removeClass('hidden');
	$($('.guideline-canvas').get(0)).css('opacity',1);
	
	
	$('#guideline-canvas-thumbs li').each(function(id) {
		$(this).bind('click', function() {
		
			IShopGuidelines.closeAllAccordionSections();
		
			$('#guideline-canvas-thumbs li').removeClass('active');
			$(this).addClass('active');
			var canvas_nr = $(this).attr('rel');
			
			IShopGuidelines.closeAllAccordionSections();
			IShopGuidelines.openAccordionSection(canvas_nr);
			
			$('.guideline-canvas')
			.css('z-index', 1000)
			.animate({
				opacity: 0
			}, {
				duration: 300,
				complete: function(a,b) {
					//console.log($(this).attr('rel'));
					$($('.guideline-canvas').get(canvas_nr))
					.css('opacity',1)
					.css('z-index', 1002);
				}
			});
		});
	});
	
	$('.pl-show-all').bind('click', function() {
		IShopGuidelines.openAllAccordionSections();
	});
	
	$('.canvas-hotspot').die("mouseover");
	$('.canvas-hotspot').die("mouseout");
	
	$('.canvas-hotspot').each(function(){
		$(this).live({
			"mouseover": function() {
				$(this).children('div.hotspot-popup').show();
			},
			"mouseout": function() {
				$(this).children('div.hotspot-popup').hide();
			}
		})
	});	
	
	$('.hp-close').live('click', function() {
		IShopNewGuideline.destroyHotspotPopup();
	});
//	
//	$('.hp-delete').live('click', function() {
//		console.log('deleting');
//		var hotspot = $(this).closest('.hotspot-popup').data('IShopHotspot');
//		var canvas_nr = $(this).closest('.guideline-canvas').attr('rel');
//		var canvas = $(this).closest('.guideline-canvas').data('IShopCanvas');
//		//var hotspot_element = $(this).closest('.guideline-canvas').find('.canvas-hotspot').get(hotspot.order - 1);
//		// remove hotspot element
//		$(this).closest('.guideline-canvas').find('.canvas-hotspot[rel='+hotspot.order+']').remove();
//		
//		$($('.pl-canvas').get(canvas_nr)).find('li[rel='+hotspot.order+']').remove();
//		
//		IShopNewGuideline.destroyHotspotPopup();
//		IShopRest.new_deleteAsset(canvas, hotspot);
//		IShopNewGuideline.markUsedAssets();
//		
//		/*
//		var canvas_nr = $(this).closest('.guideline-canvas').attr('rel');
//		var hotspot_element = $(this).closest('.guideline-canvas').find('.canvas-hotspot').get(hotspot.order - 1);
//		var product_list_element = $($('.pl-canvas').get(canvas_nr)).find('li').get(hotspot.order - 1);
//		$(hotspot_element).remove();
//		$(product_list_element).remove();
//		IShopNewGuideline.destroyHotspotPopup();
//		var canvas = $(this).closest('.guideline-canvas').data('IShopCanvas');
//		IShopRest.new_deleteAsset(canvas, hotspot);
//		IShopNewGuideline.markUsedAssets();
//		*/
//	});
//	
//	$('.qc-pl-sbc').live('click', function() {
//		var canvas = $($('.guideline-canvas').get($(this).closest('.pl-canvas').attr('rel'))).data('IShopCanvas');
//		IShopNewGuideline.destroyHotspotPopup();
//		var hotspot = $(this).closest('li').data('IShopHotspot');
//		hotspot.quantity = hotspot.quantity == 1 ? 1 : hotspot.quantity - 1;
//		$(this).next().text(hotspot.quantity);
//		IShopRest.new_saveAsset(canvas, hotspot);
//	});
//
//	$('.qc-pl-add').live('click', function() {
//		var canvas = $($('.guideline-canvas').get($(this).closest('.pl-canvas').attr('rel'))).data('IShopCanvas');
//		IShopNewGuideline.destroyHotspotPopup();
//		var hotspot = $(this).closest('li').data('IShopHotspot');
//		hotspot.quantity = hotspot.quantity + 1;
//		$(this).prev().text(hotspot.quantity);
//		IShopRest.new_saveAsset(canvas, hotspot);
//	});
//
//	$('.qc-hp-add').live('click', function() {
//		var hotspot = $(this).closest('.hotspot-popup').data('IShopHotspot');
//		hotspot.quantity = hotspot.quantity + 1;
//		$(this).prev().text(hotspot.quantity);
//		var canvas_nr = $(this).closest('.guideline-canvas').attr('rel');
//		var hotspot_nr = hotspot.order - 1;
//		$($($('.plc-list').get(canvas_nr)).find('.abqc-value').get(hotspot_nr)).text(hotspot.quantity);
//		var canvas = $(this).closest('.guideline-canvas').data('IShopCanvas');
//		IShopRest.new_saveAsset(canvas, hotspot);
//	});
//
//	$('.qc-hp-sbc').live('click', function() {
//		var hotspot = $(this).closest('.hotspot-popup').data('IShopHotspot');
//		hotspot.quantity = hotspot.quantity == 1 ? 1 : hotspot.quantity - 1;
//		$(this).next().text(hotspot.quantity);
//		var canvas_nr = $(this).closest('.guideline-canvas').attr('rel');
//		var hotspot_nr = hotspot.order - 1;
//		$($($('.plc-list').get(canvas_nr)).find('.abqc-value').get(hotspot_nr)).text(hotspot.quantity);
//		var canvas = $(this).closest('.guideline-canvas').data('IShopCanvas');
//		IShopRest.new_saveAsset(canvas, hotspot);
//	});	
//	

//	
//	$('#ga-publish-guideline').bind('click', function() {
//		IShopRest.publishGuideline(IShopNewGuideline.getGuideline());
//	});
//	
//	IShopNewGuideline.addGuidelineFormEvents();
//	
//	$('#mbss-name').click(function() {
//		var sort_criteria = $(this).data('IShopSortCriteria');
//		sort_criteria.order = sort_criteria.order == 'asc' ? 'desc' : 'asc';
//		if ( $($('#mbs-assets-selector li').get(0)).hasClass('active')) {
//			var asset_collection = IShopRest.getAllProducts(sort_criteria);
//			IShopNewGuideline.feedProductsList(asset_collection);
//		} 
//		else {
//			var asset_collection = IShopRest.getAllFixtures(sort_criteria);
//			IShopNewGuideline.feedFixturesList(asset_collection);
//		}
//		IShopNewGuideline.markUsedAssets();
//		IShopNewGuideline.initDragAndDrop();
//	});
//	
//	$('#mbss-date').click(function() {
//		var sort_criteria = $(this).data('IShopSortCriteria');
//		sort_criteria.order = sort_criteria.order == 'asc' ? 'desc' : 'asc';
//		if ( $($('#mbs-assets-selector li').get(0)).hasClass('active')) {
//			var asset_collection = IShopRest.getAllProducts(sort_criteria);
//			IShopNewGuideline.feedProductsList(asset_collection);
//		} 
//		else {
//			var asset_collection = IShopRest.getAllFixtures(sort_criteria);
//			IShopNewGuideline.feedFixturesList(asset_collection);
//		}
//		IShopNewGuideline.markUsedAssets();
//		IShopNewGuideline.initDragAndDrop();
//	});	
//	
//	$('.abqc-add').live({
//		"mousedown": function() {
//			$(this).css({
//				"background": "url(/images/ngd_back_asset_quantity_changer_hover.png) no-repeat -101px 0px"
//			});
//		},
//		"mouseup": function() {
//			$(this).css({
//				"background": "transparent"
//			});
//		}
//	});
//	
//	$('.abqc-sbc').live({
//		"mousedown": function() {
//			$(this).css({
//				"background": "url(/images/ngd_back_asset_quantity_changer_hover.png) no-repeat -40px 0px"
//			});
//		},
//		"mouseup": function() {
//			$(this).css({
//				"background": "transparent"
//			});
//		}
//	});

	
};





IShopGuidelines.toggleAccordionSection = function(id) {
	$($('.pl-canvas').get(id)).guidelineAccordion('toggleSection');
};

IShopGuidelines.openAccordionSection = function(id) {
	$($('.pl-canvas').get(id)).guidelineAccordion('openSection');
};

IShopGuidelines.closeAccordionSection = function(id) {
	$($('.pl-canvas').get(id)).guidelineAccordion('closeSection');
};

IShopGuidelines.closeAllAccordionSections = function() {
	$('.pl-canvas').each(function() {
		$(this).guidelineAccordion('closeSection');
	});
};

IShopGuidelines.openAllAccordionSections = function() {
	$('.pl-canvas').each(function() {
		$(this).guidelineAccordion('openSection');
	});
};

























