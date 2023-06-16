let select = document.getElementById("select");
select.addEventListener("change", doSelect);

$('.image').hide();
//$('.zoomIn').hide();
//$('.zoomOut').hide();

$('.search').on('click', doSearch);

/*$('.zoomIn').on('click', function(e)
{
  var image = document.getElementById("image");
  var width = image.clientWidth;

  if(width+50 < document.body.clientWidth)
  {
    image.style.width = (width + 50) + "px";
    window.scrollBy(0, 50);
  }
});*/

/*$('.zoomOut').on('click', function(e)
{
  var image = document.getElementById("image");
  var width = image.clientWidth;

  if(width-50 > document.body.clientWidth/3)
  {
    image.style.width = (width - 50) + "px";
  }
});*/

function doSearch()
{
  //$('.zoomIn').show();
  //$('.zoomOut').show();

  var select = document.getElementById("select");
  var month = document.getElementById("month");
  var date = document.getElementById("date");

  console.log("sent to py");
  console.log(select.value);
  console.log(month.value);
  console.log(date.value);

  $.getJSON('/pythonScript', {
    type: select.value,
    dataOne: month.value,
    dataTwo: date.value
  }, function(data) {
      console.log(data);

      $('.image').show();
      var image = document.getElementById("image");

      switch(select)
      {
        case "1":
          image.src = "../static/image/" + date + "_hour.png";
          break;
        case "2":
          image.src = "../static/image/hour.png";
          break;
        case "3":
          image.src = "../static/image/month.png";
          break;
        case "4":
          image.src = "../static/image/month_hour.png";
          break;
        case "5":
          image.src = "../static/image/" + date + "_pickup.png";
          break;
        case "6":
          image.src = "../static/image/" + date + "_dropoff.png";
          break;
        default:
          return;
      }
  });
}

function doSelect()
{
  temp = document.getElementById("month");
  temp.value = 0;
  temp = document.getElementById("date");
  temp.value = 0;
}
