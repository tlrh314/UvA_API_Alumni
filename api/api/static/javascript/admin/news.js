function update_date_off(element)
/* automatically update the date_off when changing the date field */
{
    var date = $(element).attr("value").split("-");
    date = new Date(parseInt(date[0])+1, parseInt(date[1])-1, date[2]);
    month = parseInt(date.getMonth()) + 1;
    strdate = new String(date.getFullYear() + "-" + 
			 month + "-" + 
			 date.getDate());
    $("#id_date_off").attr("value", strdate);
}

$(function ()
  {
      $("#id_date").bind("change", function() { update_date_off(this) });
      $("#id_date").bind("focus", function() { update_date_off(this) });
  });
