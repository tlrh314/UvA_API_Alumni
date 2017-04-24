function highlightnames(id)
{
	matches = id.match(/(\-?\d{2,3})([a-z]?)/);
	id = parseInt(matches[1]);
	postfix = matches[2];
	if (id < 0)
	{
		$("."+(-id)+postfix).css('background-color', '#fff');
		$("#"+(-id)+postfix).attr('fill', '#fff');
	}
	else
	{
		$("."+id+postfix).css('background-color', '#ccf');
		$("#"+id+postfix).attr('fill', '#ccf');
	}
}

function highlightoffices(id)
{
	matches = id.match(/(\-?\d{2,3})([a-z]?)/);
	id = parseInt(matches[1]);
	postfix = matches[2];
	if (id < 0)
	{
                /* background-color is handled by map.css */
		$("#"+(-id)+postfix).attr('fill', '#fff');
	}
	else
	{
                /* background-color is handled by map.css */
		$("#"+id+postfix).attr('fill', '#ccf');
	}
}

$(function(){ $(".hover").tooltip({ 
  delay: 0, 
  bodyHandler: function()
  {
      tip = $("ul#tip_" +  $(this).attr("id")).html();
      if (tip === null)
      {
	  $("#tooltip").css('display', 'none');
	  return '';
      }
      tip = '<ul class="hovertip">' + tip + '</ul>';
      return tip;
  } 
  })
});

$(function()
  {
    if (Modernizr.svg)
    {
      $("div#map").css('display', 'block');
    }
    else
    {
      $("div#nomap").css('display', 'block');
    }
  }
);

function enlarge()
{
    scale = $(window).width() / $('#svgmap').width() * 0.95;
    translate = $('#svgmap').height() / 2. * scale;
    var properties = 
    {
        'border': '1px solid #333',
        'padding': '0.2em',
        'z-index': '150',
	'-webkit-box-shadow': '6px 6px 5px #666',
	'-moz-box-shadow': '6px 6px 5px #666',
	'-o-box-shadow': '6px 6px 5px #666',
	'box-shadow': '6px 6px 5px #666',
	'-webkit-border-radius': '5px',
	'-moz-border-radius': '5px',
        '-o-border-radius': '5px',
        'border-radius': '5px',
	'-webkit-transform': 'scale(' + scale + ') translate(-2.5em, 0)', // + translate + 'px)',
	'-moz-transform': 'scale(' + scale + ') translate(-2.5em, 0)', // + translate + 'px)',
	'-o-transform': 'scale(' + scale + ') translate(-2.5em, 0)', // + translate + 'px)',
	'-webkit-transition': '-webkit-transform 1s ease',
	'-moz-transition': '-moz-transform 1s ease',
	'-o-transition': '-o-transform 1s ease',
    };
    $('#svgmap').css(properties);
    $('#svgmap').attr('onclick', 'reduce(); return true;');
    $('#resize').attr('onclick', 'reduce(); return true;');
}


function reduce()
{
    var properties = 
    {
        'border': 'none',
        'padding': 'inherit',
        'z-index': 'inherit',
	'-webkit-box-shadow': '0 0 0 0',
	'-moz-box-shadow': '0 0 0 0',
	'-o-box-shadow': '0 0 0 0',
	'box-shadow': '0 0 0 0',
	'-webkit-border-radius': '0px',
	'-moz-border-radius': '0px',
        '-o-border-radius': '0px',
        'border-radius': '0px',
	'-webkit-transform': 'scale(1) translate(0, 0)',
	'-moz-transform': 'scale(1) translate(0, 0)',
	'-o-transform': 'scale(1) translate(0, 0)',
        'border': 'none',
	'-webkit-transition': '-webkit-transform 1s ease',
	'-moz-transition': '-moz-transform 1s ease',
	'-o-transition': '-o-transform 1s ease'
    };
    $('#svgmap').css(properties);
    $('#svgmap').attr('onclick', 'enlarge(); return true;');
    $('#resize').attr('onclick', 'enlarge(); return true;');
    $('#resize').html('Click to enlarge');
}
