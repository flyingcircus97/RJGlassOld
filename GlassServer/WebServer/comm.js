	var statusUpdate = new Request({	
		//Used just to change Disconnect, Connect
		url: '/ajax/comm_update',
		method: 'get',
		onSuccess: function(responseText, responseXML) {
			}
			});

	var img_status_load = function() {
		$('img_status').set('src','../images/ajax-loader.gif');
		}

	var commRequest = new Request({
	url: '/ajax/comm_status',
	method: 'get',
	onSuccess: function(responseText, responseXML) {
		var j = JSON.decode(responseText);
		var mode=j[0]
		var status = j[1]
		var IOCP_status = j[2][0]
		
		// If sim name changes then update src of img
		if (mode != prev_mode) {
			var f_name = 'images/modes/' + mode.toLowerCase() + '.png';
			$('img_mode').set('src',f_name);
			$('img_mode').set('title',mode);
			$('img_mode').set('alt',mode);
			prev_mode = mode;
			}
		if (status != prev_status) {
			//Set Status image correctly
			var f_name = 'images/status/' + status.toLowerCase() + '.png';
			$('img_status').set('src',f_name);
			$('img_status').set('title',status);
			$('img_status').set('alt',status);						
			prev_status = status;
			
			//Set button to either disconnect or connect
			//  Reset comm button
			//$('comm_button').empty();
			//$('comm_button').selected = false;
			//$('comm_button').removeClass('selected');
			
			if (status == 'Disconnected') { //Then make connect button
				var f_name = 'images/status/connect.png';
				$('img_status').command = 'Connect';
				}
			else  { // Make disconnect button, if mode is not disconnect.
				var f_name = 'images/status/disconnect.png';
				$('img_status').command = 'Disconnect';
				}
				
		/*IOCP Status */
		if (IOCP_status != prev_IOCP_status) {
			//Set Status image correctly
			var f_name = 'images/status/' + IOCP_status.toLowerCase() + '.png';
			$('IOCP_status').set('src',f_name);
			$('IOCP_status').set('title',IOCP_status);
			$('IOCP_status').set('alt',IOCP_status);						
			prev_IOCP_status = IOCP_status;
			}
			//Create button image				
			/*var button_img = new Element('img', {
				'id': 'comm_img',
				'src': f_name,
				'title' : 'Click to ' + button_name,
				'alt' : button_name,
				});

			button_img.inject($('comm_button'));
			$('comm_button').appendText(button_name);
			$('comm_button').removeClass('empty');*/
			} // end if status != prev_status
	
		//Set timer for refresh.
		comm_timer = setTimeout("commRequest.send();", 2500);
		},
	onFailure: function(xhr) { //On failure of comm status, put up error image, and blank status.
		$('img_mode').set('src','images/modes/error.png');
		$('img_mode').set('title','No Comm with GlassServer');
		$('img_mode').set('alt','No Comm');	
		$('img_status').set('src','images/modes/blank.png');
		$('img_status').erase('title');
		$('img_status').erase('alt');
		//Empty comm_button
		//$('comm_button').empty;
		//$('comm_button').addClass('empty');
		prev_mode = 'error';
		prev_status = 'error';
		comm_timer = setTimeout("commRequest.send();", 5000);
		}
	});	
	
	
	window.addEvent('domready', function() {

	//$('comm_button').selected = false;
	//Hover logic
	//$('comm_button').addEvent('mouseover', function(event) {
	//			if (this.selected == false) {
	//			this.addClass('hover');
	//			} // end if
	//		}); // s.addEvent mouseover
	//$('comm_button').addEvent('mouseout', function(event) {
	//			this.removeClass('hover');
	//		}); // s.addEvent mouseout
			// Click logic
	$('img_status').addEvent('click', function(event) {
				clearTimeout(comm_timer);				
				//Send request to change status.
				//$('comm_img').set('src','images/ajax-loader.gif');
				statusUpdate.send('status='+$('img_status').command);
				comm_timer = setTimeout("commRequest.send();", 1000);
				this.selected = true; //Will be reset when status changes.
				this.addClass('selected');
				});
				
				

	//Globals
	prev_mode = '';
	prev_status = '';
	prev_IOCP_status = '';
	comm_timer = setTimeout("commRequest.send();", 2000);
	});


