window.addEvent('domready',function(){
	tree = new Mif.Tree({
		container: $('tree_container'),// tree container
		initialize: function() {
				this.initCheckbox('deps');
				},
		types: {// node types
			folder:{
				openIcon: 'mif-tree-open-icon',//css class open icon
				closeIcon: 'mif-tree-close-icon'// css class close icon
			}
		},
		dfltType:'folder',//default node type
		height: 18,//node height
		onCheck: function(node){
			sendChecked();
		},
		onUnCheck: function(node){
			sendChecked();
		}


		
	});
	$('tree_container').tree = tree;
	var sendChecked = function() {
		checked = [];
		$('tree_container').tree.getChecked().each(function(node) {
			checked.include(node.key);
			});
		//alert(JSON.encode(checked));
		//varRequest.get('var='+checked);
		
		varRequest.send('var='+checked.join(","));
		}
	var json=[
		{
			"property": {
				"name": "root"
			},
			"children": [
				{
					"property": {
						"name": "node1"
					}
				},
				{
					"property": {
						"name": "node2"
					},
					"state": {
						"open": true
					},
					"children":[
						{
							"property": {
								"name": "node2.1"
							}
						},
						{
							"property": {
								"name": "node2.2"
							}
						}
					]
				},
				{
					"property": {
						"name": "node4"
					}
				},
				{
					"property": {
						"name": "node3"
					}
				}
			]
		}
	];
	var json2=[
		{
			"property": {
				"name": "root"
			}
		}
	];
	
	//alert(json2);
	// load tree from json.
	//tree.load({
	//	json: json2
	//});
	
});
