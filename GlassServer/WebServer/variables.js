	var load_tree = function(div) {
	
		var myRequest = new Request({
		url: '/ajax/var_tree',
		method: 'get',
		onSuccess: function(responseText, responseXML) {
			j = JSON.decode(responseText);
			//alert(j);
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
				myTable.push([{ content: item[0], properties:{colspan:"4", class:"group_row"}}]);
			}
			else {
			myTable.push(item);
			}
			});
		
		}
	});
	
	out_JSON = {};
	out_JSON.eat = 5;
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