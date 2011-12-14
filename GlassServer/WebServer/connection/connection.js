
	function reset_config_table(id) {
		id.getElements('td').each(function(item,index) {
			item.selected = false;
			item.removeClass('select')
			});
		}

	function load_config_table(id, list, selected) {
		id.empty();
		list.each(function(item, index) {
			var tr = new Element('tr');
			var td = new Element('td', {'text':item});
			td.num = index;
			td.selected = false;
			td.addEvent('mouseover', function(event) {
				if (this.selected == false) {
				this.addClass('hover');
				} // end if
			}); // tr.addEvent mouseover
			td.addEvent('mouseout', function(event) {
				this.removeClass('hover');
			}); // tr.addEvent mouseout
			td.addEvent('click', function(event) {
				reset_config_table($('conn_table'));
				load_parameters(config_param,conn_data[this.num], this.num);
				this.selected = true;
				td.addClass('select');
				td.removeClass('hover');
			});


			//If to check if selected index is current one
			if (index == selected) {
				td.selected = true;
				td.addClass('select');
				td.removeClass('hover');
				}
			td.inject(tr);
			tr.inject(id);
			});
		}
	function config_textbox_c(title) {
		var div = new Element('div', {'id':'conn_config'});
		var conn_table = new Element('table', {'id':'conn_table'});
		var h3 = new Element('h3', {'text': title});
		h3.inject(div);
		conn_table.inject(div);
		this.div = div;

		return this
		
	}
		
	function text_input(div, heading, value) {

		var p = new Element('p', {'text': heading});
		if (heading == 'Name:') {
			p.addClass('first_p');
		}
		var input = new Element('input',{'type': 'text', 'id':heading+'field'});
		input.value = value;
		//input.disabled = true;
		input.inject(p);
		p.inject(div);
		return input;
		}
		
	function select_greyout(value) {
			if (value=='Test') {
				$('IP:field').disabled = true;
				$('Port:field').disabled = true;
				}
			else {
				$('IP:field').disabled = false;
				$('Port:field').disabled = false;
				}
		}
	
	function select_input(div, heading, values, selected) {
		var p = new Element('p', {'text': heading});
		var select = new Element('select',{'name': 'mode'});
		select.addEvent('change',function() {select_greyout(this.value)});
		values.each(function(item, index) {
			var opt = new Element('option', {'value':item});
			if (index == selected) {
				opt.set('selected', 'selected');
				}
			opt.appendText(item);
			opt.inject(select);
					
		
			});
		select.inject(p);
		p.inject(div);
		return select;
		}
	function checkbox_input(div, heading, selected) {
		var p = new Element('p', {'text': heading});

		var check = new Element('input',{'type': 'checkbox', 'name': heading});
		check.checked = selected;
		check.inject(p);
		p.inject(div);
		return check;
		}

	function button_input(div, heading, func) {
		var button = new Element('input', {'class': 'button', 'type': 'submit', 'value' : heading});
		button.inject(div);
		button.addEvent('click', func);
		return button;
		}

	function connect_input(div, heading, func) {
		var button = new Element('input', {'id': 'connect_button', 'type': 'submit', 'value' : heading});
		button.inject(div);
		button.addEvent('click', func);
		return button;
		}

	function save_click(event) {
		//Send new data to update config file.
		connectionRequest.send('action=save;' + compose_parameters(config_param));
		}

	function new_click(event) {
		//Create new connection in config file.
		connectionRequest.send('action=new;' + compose_parameters(config_param));
		}

	function delete_click(event) {
		//Create new connection in config file.
		connectionRequest.send('action=delete;' + compose_parameters(config_param));
		}

	function connect_click(event) {
		//Create new connection in config file.
		$('connect_button').addClass('load');
		connectionRequest.send('action=connect;' + compose_parameters(config_param));
		
		}


	function compose_parameters(obj) {
		s = 'index='+ obj.selected + ';';
		s += 'name='+ obj.config_name.value + ';';
		s += 'mode=' + obj.mode.value + ';';
		s += 'IP=' + obj.IP.value+ ';';
		s += 'port=' + obj.port.value
		return s
		}

	function config_parameters_c(title) {
		var div = new Element('div', {'id':'conn_parm'});
		var h3 = new Element('h3', {'text': title});
		h3.inject(div);
		var div2 = new Element('div', {'id':'conn_input'});
		//var form = new Element('form');
		
		this.config_name = text_input(div2, 'Name:', 'Test');
		this.mode = select_input(div2,'Mode:', ['Test','FSX SP2','X-Plane 9', 'FlightGear', 'ESP'], 0);
		this.IP = text_input(div2, 'IP:', '127.0.0.1');
		this.port = text_input(div2, 'Port:', '1500');
		//this.def = checkbox_input(div2, 'Default:', false);
		this.connect_button = connect_input(div2, 'Connect', connect_click);
		this.save_button = button_input(div2, 'Save', save_click);
		this.new_button = button_input(div2, 'New', new_click);
		this.delete_button = button_input(div2, 'Delete', delete_click);
//		form.inject(div);
		div2.inject(div);
		this.div = div;
		return this
		}

	function load_parameters(div, obj, selected) {
		//Load in the Connection Parameters after new connection config is selected.
		div.config_name.value = obj.name;
		div.IP.value = obj.IP;
		div.port.value = obj.port;
		div.selected = selected;
		
		div.mode.getChildren().each(function(item, index) {
			if (item.value == obj.mode) {
				div.mode.selectedIndex = index;}
			});
		select_greyout(obj.mode);
		//div.def.checked = def_check;
		}

	var connectionRequest = new Request({
		url: '/ajax/connection',
		method: 'get',
		onSuccess: function(responseText, responseXML) {
		if (responseText == 'ok_connect')  { //If ok_connect then just reset load gif on connect button.
			$('connect_button').removeClass('load');
		}
		else {
		j = JSON.decode(responseText);
			conn_data = j[1];
			//alert(conn_data);
			selected = parseInt(j[0]);
			load_config_table($('conn_table'),conn_data.map(function(item,index){ return item.name;}), selected);
			load_parameters(config_param,conn_data[selected], selected);
		} // else
		} // onSuccess
	}); 

	

	function load_connection(div) {
		
		var config_textbox = new config_textbox_c('Connection Configs');
		config_param = new config_parameters_c('Connection Parameters');
		config_textbox.div.inject(div);
		config_param.div.inject(div);
		connectionRequest.send('action=none');

	}

	window.addEvent('domready', function() {
		

	
	//Globals
	
	});



