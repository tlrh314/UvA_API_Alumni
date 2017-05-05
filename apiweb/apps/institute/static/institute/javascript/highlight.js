function highlight_anchor(event)
/* Highlights an anchored link 
   This is so the link jumped to can more easily be spotted
   Does not work across pages */
{

  /* set active menu item */
  anchor = event.target.href.split("#")[1];
  path = event.target.pathname + "#" + anchor;
  $("a[href*='#']").removeClass("active");
  $("a[href='" + path + "']").addClass("active");

  /* highlight corresponding subheading */
  el = $("a[name='" + anchor + "']+*");
  el.css("background-color", "#fff");
  /* fade in */
  el.animate({ backgroundColor: "#ffa"}, 300);
  /* fade out (slower) after 1 second */
  setTimeout(function() {el.animate({backgroundColor: "#fff"}, 1500)}, 500);
}

$(
  function()
  {
    $("div#sidemenu a[href*='#']").bind("click", highlight_anchor);
  }
  );
