

	function draw_AI(canvas) {
		
		function draw_line(angle, pitch, w, h) {

		context.beginPath();
		// calculate first point
		var tan_angle = Math.tan(angle/180*Math.PI)
		var right_y = -(tan_angle * w);
		var left_y = -right_y + pitch;
		var right_y = right_y + pitch;
		
		//alert(right_y);
		//alert(left_y);

		if (Math.abs(right_y) <= h) { //Horizon hits side of AI
			var x1=w;
			var y1=right_y;
		} //end if (y1<=h)
		else if  (right_y > h) { //Horizon hits top of AI
			var x1=w + ((right_y - h) / tan_angle);
			var y1=h;
		} //end elseif
 		else { // Horizon hits bottom of AI
			var x1=w+ ((right_y + h) / tan_angle);
			var y1=-h;
		     }
		if (Math.abs(left_y) <=h) {
			var x2=-w;
			var y2=left_y;
		}
		else if (left_y > h) {
			var x2= -w + ((left_y-h) / tan_angle);
			var y2=h;
			}
		else {
			var x2=-w + ((left_y +h) / tan_angle);
			var y2=-h;
			}
				

		context.moveTo(x2,y2);
		context.lineTo(x1,y1);
		context.stroke();	

		//Data
		$('message').empty();
		s = 'Tan' + tan_angle + ' ('+ x1.toString() +',' + y1 + ') ('+x2+','+ y2+')';
		$('message').appendText(s);
		}


		//draw_AI Main
		context = canvas.getContext("2d");
		//Save state
		context.save();
		//Make center of canvas 0,0
		var w = (context.canvas.width) /2
		var h = (context.canvas.height) /2 

		context.translate(w, h);
		//var w = 30;
		//var h = 30;
		//
		draw_line(0, 0, w, h);
		context.strokeStyle="#000";
		context.fillStyle="#F00";
		context.stroke();
		
		//context.fill();
		context.restore();

		
	}
		
	

	function load_guages(div) {
		
		var h1 = new Element('p', {'id':'message'});
		var canvas = new Element("canvas", {width:120, height:120, id:'b'});
		//If IE then init canvas per excanvas.
		if  (!(canvas.getContext)) {
			G_vmlCanvasManager.initElement(canvas);
			}
		h1.inject(div);
		canvas.inject(div);

		draw_AI(canvas);


	}

	window.addEvent('domready', function() {
	
	
	//Globals
	
	});



