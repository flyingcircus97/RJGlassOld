	function load_script_table(id, list) {
		id.empty();
		var tr = new Element('tr');
		['Active','Name','Filename','Message'].each(function(item,index) {
			var td = new Element('td', {'text': item});
			td.inject(tr);
			});
		tr.addClass('header');
		tr.inject(id);
		list.each(function(item, index) {
			var tr = new Element('tr');
			item.each(function(item,index) {
				if (index == 0) { //First element active (True or False)
					var td = new Element('td');
					var input  = new Element('input',{'type':'checkbox'});
					input.addEvent("change", function(event) {
						clearTimeout(script_timer);
						script_timer = setTimeout("send_scriptRequest();", 50); });
					input.checked = item;
					input.inject(td);
					td.inject(tr);
					}
				else { 
				var td = new Element('td', {'text':item});
				if (index>=3) {
            td.addClass('desc'); }
				td.inject(tr);
				}
				
			 }); //item.each
//			tr.addEvent('click',function(click) {
			tr.inject(id);
			});
		
		}
	function script_table_c(title) {
		var div = new Element('div', {'id':'script_conn'});
				var h3 = new Element('h3', {'text': title});
		h3.inject(div);
		var table = new Element('table', {'id':'script_table'});
		table.inject(div);
		this.div = div;

		return this.div;
		}

	function send_scriptRequest() {
		//Send list of requests that are active.
		list = [];
		if ($chk($('script_table'))) { // If script table doesn't exist then stop sending requests.
			var checkboxes = $('script_table').getElements('input');
			checkboxes.each(function(item,index) {
				if (item.checked == true) {
					list.push(index); }
				}); // end checkboxes each
			scriptRequest.send('active='+JSON.encode(list));
			} // end if chk script_table
		}

	var scriptRequest = new Request({
		url: '/ajax/script',
		method: 'get',
		onSuccess: function(responseText, responseXML) {
			var j = JSON.decode(responseText);
			if ($chk($('script_table'))) { // If server_table doesn't exist, then stop requests.
			load_script_table($('script_table'), j);

		script_timer = setTimeout("send_scriptRequest();", 3000);
		} // end if server_table exists
		}, // onSuccess
		onFailure: function(xhr) {
		script_timer = setTimeout("scriptRequest.send('action=none');", 5000);
		}
	}); 


	function load_scripts(div) {
		
		var script_table = new script_table_c('Script List');
		//config_param = new config_parameters_c('Connection Parameters');
		script_table.inject(div);
		scriptRequest.send('active=');
	}

	window.addEvent('domready', function() {
	//Globals
	
	});


/*td.addEvent('click', function(event) {
          if (raw_hex == false) {
              raw_hex = true; }
          else {
              raw_hex = false;
              }
           load_log_table($('conn_log_table'), j_comm);
           });
*/
