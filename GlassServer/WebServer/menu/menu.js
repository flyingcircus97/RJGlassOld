	
	function create_menubar(names, func) {
		//Creates the Dom Elements for the Menubar
		var ul = new Element('ul', {'id': 'tablist'});
		ul.clear = function() {
				this.getElements('li').each(function(item,index) {
					item.selected = false;
					item.removeClass('selected');
				});
			}
		names.each(function(item, index) {
			var li = new Element('li',{'text': item});
			li.func = func[index];
			li.index = index;
			li.selected = false;			
			li.inject(ul);
			li.addEvent('mouseover', function(event) {
				if (this.selected == false) {
					this.addClass('hover');
				} // end if
			}); // s.addEvent mouseover
			li.addEvent('mouseout', function(event) {
				this.removeClass('hover');
			}); // s.addEvent mouseout
			// Click logic
			li.addEvent('click', function(event) {
				this.getParent().clear();
				this.selected = true;
				this.addClass('selected');
				$('content').set('opacity', 0);
				load_content(this.func);
				$('content').tween('opacity',0,1);
				
				
					
				});



			});

		





		return ul;
		}
	
	function load_content(func) {
		$('content').empty(); //Empty content div.
		func($('content'));
		}
	function load_variable() {
		alert('variable_init');
		}
	
	function load_guages() {
		alert('Guages init');
		}

	function load_connection() {
		alert('Connection init');
		}
		
	function load_server() {
		alert('Server init');
		}

	window.addEvent('domready', function() {
	
	//Globals
	menu_selected = 0;	
	var names = ['Variables','Guages','Connection','Server','Scripts'];
	var func = [load_variable, load_guages, load_connection, load_server, load_scripts];
	create_menubar(names, func).inject($('menu'));

	});


