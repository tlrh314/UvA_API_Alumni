function update_date_off(element)
/* automatically update the date_off when changing the date field */
{
    var date = $(element).attr("value").split("-");
    date = new Date(parseInt(date[0])+1, parseInt(date[1])-1, date[2]);
    /* set date_off 2 weeks after deadline */
    date.setTime(date.getTime() + 14 * 86400 * 1e3);
    month = parseInt(date.getMonth()) + 1;
    strdate = new String(date.getFullYear() + "-" + 
			 month + "-" + 
			 date.getDate());
    $("#id_date_off").attr("value", strdate);
}

$(function ()
  {
      $("#id_deadline").bind("change", function() { update_date_off(this) });
      $("#id_deadline").bind("focus", function() { update_date_off(this) });
  });
