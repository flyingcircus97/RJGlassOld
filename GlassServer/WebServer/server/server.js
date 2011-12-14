	function reset_server_table(id) {
		id.getElements('tr').each(function(item,index) {
			item.selected = false;
			item.removeClass('select');
			
			});
		}

	
	function load_connection_table(id, list) {
		id.empty();
		var active_conn = 0;
		//Create header row.
		var tr = new Element('tr');
		['Name','IP Addr','Port','TX B','RX B'].each(function(item,index) {
			var td = new Element('td', {'text': item});
			td.inject(tr);});
		tr.addClass('header');
		tr.inject(id);
		
		list.each(function(item, index) {
			var tr = new Element('tr');
			tr.num = index;
			if (server_row_selected == index) {
        tr.selected = true;
        tr.addClass('select'); 
        }
      else {
        tr.selected = false;
        }
      
			item.each(function(item,index) {
				if (index == 0) { //First element active (True or False)
					if (item == true) {
						active_conn = active_conn +1	}
					else {
						tr.addClass('inactive');
						}
					}
				else if (index ==1) { //Number of connection, don't display but load.
					tr.num == item;
					}
				else {
				var td = new Element('td', {'text':item});
				td.inject(tr);
			
				}
			 }); //item.each
      tr.addEvent('mouseover', function(event) {
				if (this.selected == false) {
				this.addClass('hover');
				}
			}); // tr.addEvent mouseover
			tr.addEvent('mouseout', function(event) {
				this.removeClass('hover');
			}); // tr.addEvent mouseout	
			tr.addEvent('click', function(event) {
        reset_server_table($('server_table'));
				//load_parameters(config_param,conn_data[this.num], this.num);
				this.selected = true;
				this.addClass('select');
				this.removeClass('hover');
				server_row_selected = this.num;
				conn_request();
          });
			tr.inject(id);
			});
		return active_conn;
		}
	
	function load_log_table(id, list) {
		id.empty();
		var tr = new Element('tr');
		if (raw_hex == true) {
      var col_name = 'Data (Raw Hex)';
      }
      else {
      var col_name = 'Data (Decoded)';
      }
		['Dir','Time (s)','Cmd',col_name].each(function(item,index) {
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
					var img  = new Element('img',{'src':'images/' + item + '.gif'});
					img.inject(td);
					td.inject(tr);
					}
				else if (((index==4) && (raw_hex == true)) || ((index==3) && (raw_hex==false))) { 
				     // in these combinations do not load data from list to table.
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

	function server_textbox_c(title) {
		var div = new Element('div', {'id':'server_status'});
				var h3 = new Element('h3', {'text': title});
		h3.inject(div);
		var div2 = new Element('div', {'id':'server_param'});
		var p1 = new Element('p', {'text':'Status: Running'});
		var img = new Element('img',{'id': 'server_status_img'});
		img.inject(p1);
		p1.inject(div2);
		var p3a = new Element('p', {'text':'Server Port:', 'id':'server_port'});
		p3a.inject(div2);
		var p2a = new Element('p', {'text':'Active Conn:', 'id':'active_conn'});
		//		p2b.addClass('inline');
		p2a.inject(div2);
	

		

		div2.inject(div);
		this.div = div;

		return this
		
	}

	function server_connection_table_c(title) {
		var div = new Element('div', {'id':'server_conn'});
				var h3 = new Element('h3', {'text': title});
		h3.inject(div);
		var table = new Element('table', {'id':'server_table'});
		table.inject(div);
		this.div = div;

		return this.div;
		}

  function hex_click() {
      
      if (raw_hex == true) {
          raw_hex = false;
          $('conn_hex').removeClass('selected'); }
      else {
          raw_hex = true;
          $('conn_hex').addClass('selected');
          }
     load_log_table($('conn_log_table'), j_comm); // refresh table.     
     }
  
  function conn_request() {
      $('conn_log').tween('border-color','#ff0000','#ffff00');
			//refreshFx.start('background-color','green','red');
      if (server_row_selected >=0) {
      conn_logRequest.send('index='+server_row_selected);
        }
      } // end conn_request
      

	function connection_log_table_c(title) {
		var div = new Element('div', {'id':'conn_log'});
				var h3 = new Element('h3', {'text': title});
				var p = new Element('p', {'id': 'conn_refresh','text':'Refresh'});
				//p.addEvent('mouseover',function(event) { this.addClass('hover'); });
				//p.addEvent('mouseout',function(event) { this.removeClass('hover'); });
				p.addEvent('click', conn_request);
				//p.addEvent('mousedown',function(event) {refreshFx.set('background-color','green');});
				//p.addEvent('mouseup',function(event) {refreshFx.start('background-color','green','red');});
				var p2 = new Element('p', {'id': 'conn_hex','text':'Hex'});
				p2.selected = false;
				p2.addEvent('mouseover',function(event) { 
            if (raw_hex == false) { this.addClass('hover'); }});
        p2.addEvent('mouseout',function(event) { this.removeClass('hover'); });
        p2.addEvent('click', hex_click);
            
				
		
		h3.inject(div);
		p.inject(div);
		p2.inject(div);
		
		var table = new Element('table', {'id':'conn_log_table'});
		table.inject(div);
		this.div = div;

		return this.div;
		}

	var serverRequest = new Request({
		url: '/ajax/server',
		method: 'get',
		onSuccess: function(responseText, responseXML) {
			var j = JSON.decode(responseText);
			if ($chk($('server_table'))) { // If server_table doesn't exist, then stop requests.
			var active_conn = load_connection_table($('server_table'), j['connections']);
			$('active_conn').set('text', 'Active Conn: ' + active_conn);
			$('server_port').set('text', 'Server Port: ' + j['port']);

		server_timer = setTimeout("serverRequest.send('action=none');", 5000);
		} // end if server_table exists
		}, // onSuccess
		onFailure: function(xhr) {
		server_timer = setTimeout("serverRequest.send('action=none');", 5000);
		}
	}); 


var conn_logRequest = new Request({
		url: '/ajax/conn_log',
		method: 'get',
		onSuccess: function(responseText, responseXML) {
			j_comm = JSON.decode(responseText);
			load_log_table($('conn_log_table'), j_comm);
      $('conn_log_table').tween('opacity',0.25, 1.0);
      
		}, // onSuccess
		onFailure: function(xhr) {
		
		}
	}); 


	function load_server(div) {
		
		var server_textbox = new server_textbox_c('Server Status');
		//config_param = new config_parameters_c('Connection Parameters');
		server_textbox.div.inject(div);
		
		var server_connection_table = new server_connection_table_c('Server Connections');
		server_connection_table.inject(div);
		serverRequest.send('action=none');
		var connection_log_table = new connection_log_table_c('Connection Log');
		connection_log_table.inject(div);
		conn_request(); //Request update to comm log table, if someone returns to tab.
	}

	window.addEvent('domready', function() {
		server_row_selected = -1;
    raw_hex = false;
    
	
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