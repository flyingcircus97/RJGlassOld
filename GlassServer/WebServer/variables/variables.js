	function send_var(value_td) {
		reset_value_td(old_target);
		old_target.childNodes[0].nodeValue = value_td.value; // reset it to most up to date value.
		old_target.replaces(edit_row);
		var sendvarRequest = new Request({
		url: '/ajax/set_var',
		method: 'get',
		onSuccess: function(responseText, responseXML) {
			var h = JSON.decode(responseText);
			//alert(h);
			if (h[0] == null) { // Error in setting value.
				redFx.set('background-color', '#f00'); // fade to red
				redFx.start('background-color', '#f00', '#fff'); // then fade to white
				
				
				}
			else {
				//greenFx.start('background-color', '#ff0', '#adff44'); // fade to green
				greenFx.set('background-color', '#adff44'); // fade to green
				greenFx.start('background-color', '#adff44', '#fff'); // then fade to white
				
		  		} // end else
			td_parent.getElements('td')[td_value_col].childNodes[0].nodeValue = h[1]; //set td value to response.
			}
		});
		//td_parent.addClass('submit');
		td_parent.removeClass('delta');
		edit_row = null;
		// tween it from yellow to white.
		var greenFx = new Fx.Tween(td_parent, {'duration' : 2000, 'link':'chain'});
		var redFx = new Fx.Tween(td_parent, {'duration' : 4000, 'link':'chain'});
		//myFx.start('background-color', '#ff0', '#fff');
		//Send addr and value
		// - Get address
		var addr = td_parent.getElements('td')[td_addr_col].childNodes[0].nodeValue;
		sendvarRequest.send('addr='+addr+';value='+value_td.value);
		}
	
	
	function reset_var_timer() {
		//Resets timer. Clears timeout to make sure not multiple timers are going at once.
		if (typeof(var_timer) != "undefined") {
					clearTimeout(var_timer); }  // end if typeof(var_time)
				var_timer = setTimeout("window.fireEvent('updatevar');", var_refresh_rate.value* 1000); //Stop request
				}
  function refresh_flash() {
		//Flashes Rest Text and Table border, to show vars are being updated.
			 $('refresh_text').refreshFx.start('background-color','#adff44', '#fff');
			 //$('refresh_text').highlight('#adff44');
			 tableFx.start('border-color','#adff44', '#000');
		}

	function reset_value_td(value_td) {
	//	value_td.addEvent('click', function(event) {
	//		 edit_td_click(event.target);});
				value_td.editing = false;
		
		}	

	function reset_row(row) {
		row.addEvent('click', function(event) {
			
			edit_td_click(this.getElements('td')[td_value_col]);
//			alert(event.target.getElements('td'));
//			alert(this);
			});
		}

	function create_refresh_selector(refresh_rate) {
		//Creates the Dom Elements for the Refresh Rate: 1 2 5 10 sec
		main_div = new Element('div', {'id': 'refresh'});
		
		var p = new Element('p');
		
		p.style.MozUserSelect="none";
			p.addEvent('clear', function() {
				this.getElements('span').each(function(item,index) {
					item.selected= false;
					item.removeClass('selected');
				});//end this.getElements('span')
			}); // end p.addEvent('clear')
		
		var s = new Element('span', {'text' : 'Refresh Rate:', 'id' : 'refresh_text'});
		s.refreshFx = new Fx.Tween(s, {'duration' : 800});
		s.inject(p);
		
			
		[1,2,5,10].each(function(item,index) {
			var s = new Element('span', {'text' : item.toString(), 'UNSELECTABLE' : "on"});
			
			if (refresh_rate.value == item) { // select one that is currently active.
				s.selected = true;
				s.addClass('selected');
				 }
			else {
				s.selected = false; // start off as not selected.
			     }
			s.value = item;
			s.refresh_rate = refresh_rate;
			if (item>=10) { //if two digit refresh rate. Add class for padding.
				s.addClass('duce');
				}
			//Hover logic
			s.addEvent('mouseover', function(event) {
				if (this.selected == false) {
				this.addClass('hover');
				} // end if
			}); // s.addEvent mouseover
			s.addEvent('mouseout', function(event) {
				this.removeClass('hover');
			}); // s.addEvent mouseout
			// Click logic
			s.addEvent('click', function(event) {
				this.getParent().fireEvent('clear');
				this.selected = true;
				this.addClass('selected');
				this.refresh_rate.value = this.value;
				
				if (typeof(var_timer) != "undefined") {
					clearTimeout(var_timer); }  // end if typeof(var_time)
				var_timer = setTimeout("window.fireEvent('updatevar');", var_refresh_rate.value* 1000); //Stop request if 
				
				});
				
			s.inject(p);
			});
		var s = new Element('span', {'text' : 'sec'});
		s.inject(p);
		p.inject(main_div);		
		return main_div;
		}
	
	function reset_edit_row() {
		if (edit_row != null) { //If other row being edited. Restore that one back to normal.
			reset_value_td(old_target);
			old_target.childNodes[0].nodeValue = current_value; // reset it to most up to date value.
			old_target.replaces(edit_row);
			old_target.getParent().setStyle('background-color','white');
	
		}
	}

	function edit_td_click(target) {
		
		td_parent = target.getParent();
		td_parent.setStyle('background-color','yellow');
		if (edit_row != target) {
			reset_edit_row();
		}
		// Get current value
		current_value = target.childNodes[0].nodeValue;
		// Save last value
		old_target = target.clone();
		
		// Delete textnode
		edit_row = target;
		target.empty();
		target.editing = true;
		
		//Make new input box.
		var box = new Element('input', {
			'id':'var_input'
		});
		box.addEvent('click', function(event) { event.stop();}); // Prohibits click event to go to row event.
		box.addEvent('keydown', function(event) { 
			if (event.key == 'enter') {
				send_var($('var_input'));
				}
			
			});
		box.inject(target);
		$('var_input').value = current_value.trim();
		$('var_input').focus();
		$('var_input').select();
	}	

	var load_tree = function(div) {
	
		var myRequest = new Request({
		url: '/ajax/var_tree',
		method: 'get',
		onSuccess: function(responseText, responseXML) {
			j = JSON.decode(responseText);
			$('tree_container').tree.load({json: j});
			$('tree_container').tree.restoreChecked();
		
		}
	});	
	
	myRequest.send();
	
	} // load_tree
	
	var varRequest = new Request({
		url: '/ajax/get_var',
		method: 'get',
		onSuccess: function(responseText, responseXML) {
			reset_edit_row();
			$('the_table').destroy();	
			var myTable = new HtmlTable({
				properties: {
						border: 1,
						cellspacing: 3,
						id: 'the_table'
				},
			rows: [
							]
			});
		
		myTable.inject($('var_table'));
		j = JSON.decode(responseText);
		j.each(function(item, index) {
			if (item.length == 1) {
				//alert('SPAN');
				myTable.push([{ content: item[0], properties:{colspan:"7"}}]);
				//Add group_row class to this item.
				var rows = $('var_table').getElements('tr');
				var last_row = rows[rows.length-1]
				var header_td = last_row.getElements('td')[0];
				header_td.addClass('group_row');
			}
			else {
			var first_item = item[0];
			item[0] = ' '
			myTable.push(item);
			
			//alert(first_item);
			// if writeable add code for td to make it editable.
			var rows = $('var_table').getElements('tr');
			var last_row = rows[rows.length-1]
			var value_td = last_row.getElements('td')[td_value_col];
			value_td.addClass('value');
			tableFx = new Fx.Tween('the_table', {'duration' : 800});
			reset_value_td(value_td);
			var img_td = last_row.getElements('td')[img_td_col];
			if (first_item == true) {
				var img = new Element('img', {'src' : 'images/edit.png'});
				img.inject(img_td);
				reset_row(last_row); // only reset row click if variable is editable.
				}


			//value_td.addEvent('click', function(event) {
			// edit_td_click(event.target);});
			//value_td.editing = false;

			
			
			}
			});
		
		//window.fireEvent('updatevar', null, var_refresh_rate.value* 1000);
	
	if (j.length > 1) {
		//Don't call for refresh if table has no data in it. (Other than "No Variable Group Selected row")
		//var_timer = setTimeout("window.fireEvent('updatevar');", var_refresh_rate.value* 1000); //Stop request if table is
		reset_var_timer();
		} // if j.length>1
		
		} // onSuccess
	}); 
	var updateRequest = new Request({
		url: '/ajax/var_values',
		method: 'get',
		onSuccess: function(responseText, responseXML) {
		if ($defined($('var_table'))) {
		var rows = $('var_table').getElements('tr');
		//myTable.inject($('var_table'));
		j = JSON.decode(responseText);
		j.each(function(item, index) {
			//Go through each line of table looking for changes.
			var row = rows[index];
			//Check to make sure row still exists.
			if ($defined(row)) {
			// Get current value
			var value_td = row.getElements('td')[td_value_col];
			if ($defined(value_td)) {
				if (value_td.editing == false) { 
					if (value_td.childNodes[0].nodeValue != item) {
						value_td.childNodes[0].nodeValue = item;
						row.addClass('delta'); // Add value changed class
						row.removeClass('submit');
					}
					else { // Remove class - value didn't class
						row.removeClass('delta');
						row.removeClass('submit');
					     }
				} // if (value_td.editing = false)
				else { // value_td.editing == true
					if (current_value != item) {
						current_value = item;
						row.addClass('delta'); // Add value changed class
						
					}
					else { // Remove class - value didn't class
						row.removeClass('delta');
						
					     }
					} // else	

				
			} // if($defined(value_td)
			} // if($defined(row)
			});
		if (j.length > 0) {
//			var_timer = setTimeout("alert('EARSHIT')", var_refresh_rate.value* 1000); //Stop request if table 
			reset_var_timer();
			refresh_flash();
			} // if j.length
		} // if $defined('var_table')
		} // onSuccess
	}); 

	

	// Event called to update variables in table.
	window.addEvent('updatevar', function() {
		updateRequest.send('var='+checked.join(","));

	 });
	function updateRequest_send() {
		updateRequest.send('var='+checked.join(","));

	 }

/*	<div id="tree_container"></div>
	<div id="var_table">
	
	<table id="the_table"></table>
	</div>*/


	function load_variable(div) {
		
		var tree = new Element('div', {'id':'tree_container'});
		var var_table = new Element('div', {'id':'var_table'});
		var the_table = new Element('table', {'id':'the_table'});
		
		the_table.inject(var_table);
		tree.inject(div);
		var_table.inject(div);

		init_tree();
		load_tree($('var_tree'));
		create_refresh_selector(var_refresh_rate).inject($('var_table'), 'top');
		varRequest.send('var='+checked.join(","));

	}

	window.addEvent('domready', function() {
	
	//Globals
	edit_row = null; //The row that is being edited.
	td_value_col = 4;
	td_addr_col = 1;
	img_td_col = 0;
	var_refresh_rate = new Object();
	var_refresh_rate.value = 5;
	});



