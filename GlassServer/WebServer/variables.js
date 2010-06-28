	var load_tree = function(div) {
	
		var myRequest = new Request({
		url: '/ajax/var_tree',
		method: 'get',
		onSuccess: function(responseText, responseXML) {
			j = JSON.decode(responseText);
			$('tree_container').tree.load({json: j});
		
		
		}
	});	
	
	myRequest.send();
	
	} // load_tree
	
	var varRequest = new Request({
		url: '/ajax/get_var',
		method: 'get',
		onSuccess: function(responseText, responseXML) {
		
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
				myTable.push([{ content: item[0], properties:{colspan:"6", class:"group_row"}}]);
			}
			else {
			myTable.push(item);
			}
			});
		window.fireEvent('updatevar', null, 2500);
		} // onSuccess
	}); 
	var updateRequest = new Request({
		url: '/ajax/var_values',
		method: 'get',
		onSuccess: function(responseText, responseXML) {
		var rows = $('var_table').getElements('tr');
		//myTable.inject($('var_table'));
		j = JSON.decode(responseText);
		j.each(function(item, index) {
			//Go through each line of table looking for changes.
			var row = rows[index];
			// Get current value
			var value_td = row.getElements('td')[3];
			if ($defined(value_td)) {
				if (value_td.childNodes[0].nodeValue != item) {
					value_td.childNodes[0].nodeValue = item;
					row.addClass('delta'); // Add value changed class
				}
				else { // Remove class - value didn't class
					row.removeClass('delta');
				     }
			}
			
			});
		if (j.length > 0) {window.fireEvent('updatevar', null, 2500);} //Stop request if table is empty.
		} // onSuccess
	}); 



	// Event called to update variables in table.
	window.addEvent('updatevar', function() {
		updateRequest.send('var='+checked.join(","));

	 });


	window.addEvent('domready', function() {
	

	load_tree($('var_tree'));
	
	
/*	$('FS_Connect').addEvent('click', function(){
    	out_JSON.connect = 1;
	});

	$('FS_DisConnect').addEvent('click', function(){
    	out_JSON.disconnect = 1;
	});

	}); // addEvent 'domready'

	window.addEvent('ajax', function() {
		jsonRequest.get(out_JSON);
		out_JSON = {};
	 });


	var myRequest = new Request({
		url: '/jomama.php',
		method: 'post',
		onSuccess: function(responseText, responseXML) {
			alert(responseText);
		
		}
	});
	var jsonRequest = new Request.JSON({
		url: '/ajax/json.php',
		
		onSuccess: function(data) {
			//alert(data.age.test);
			$('IAS').innerHTML = data.age.test;
			//$('FS_Connect').innerHTML = data.FSComm.status;
			window.fireEvent('ajax', null, 2500);
		} */
	});

	//	myRequest.send('username=johndoe&first=john&last=doe')
	//jsonRequest.get({'eat':'5'});
	//jsonRequest.get(JSON.encode(out_JSON));
	//jsonRequest.startTimer({'name':'William'});
	//jsonRequest.get(out_JSON);
	//out_JSON = {};
	//alert(JSON.encode(out_JSON));
