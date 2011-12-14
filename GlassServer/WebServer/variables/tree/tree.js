//Globals 
checked = []; //initialize checked as none
expanded = ['All','Main'];
init_tree = function() {
		
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
		},
		onToggle: function(node){
			updateExpanded();
		},


		});
		
	tree.restoreChecked = function() {
			var t_checked = checked;
			var t_expanded = expanded;
			this.root.recursive(function() {
			if (t_checked.indexOf(this.key) != -1) {
			  //if this.key in checked then toggle it.
			   this['switch']('checked'); // Weird syntax is for Chrome compatability.
				}
			if (t_expanded.indexOf(this.key) != -1) {
			  //if this.key in checked then toggle it.
			   this.toggle(true);
				}

			//alert(states);
			});
	}
	//tree.root.recursive(function() {
//		this.toggle(null,flase);
//	});
//	states = new Mif.Tree.CookieStorage(tree);	*/
	$('tree_container').tree = tree;
	
  } //end init_tree

	var updateExpanded = function() {
		expanded = [];
		$('tree_container').tree.root.recursive(function() {
			if (this.state.open) {
			expanded.include(this.key);
			}
		});
	
		} // updatedExpanded

	var sendChecked = function() {
		edit_row = null; //Reset edit row.
		checked = [];
		$('tree_container').tree.getChecked().each(function(node) {
			checked.include(node.key);
			//node.toggle(true);
			 });
		
		//alert(JSON.encode(checked));
		//varRequest.get('var='+checked);
		
		varRequest.send('var='+checked.join(","));
		}

	
	//alert(json2);
	// load tree from json.
	//tree.load({
	//	json: json2
	//});
	


