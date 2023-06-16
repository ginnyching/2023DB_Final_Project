let select = document.getElementById("select");
select.addEventListener("change", doSelect);

$('.image').hide();
$('.month').hide();
$('.date').hide();
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

  if(month.value==2 && date.value>28)
  {
    alert(month.value + "-" + date.value + " is an invalid date");
  }else if((month.value==4 || month.value==6 || month.value==8 || month.value==10) && (date.value==31))
  {
    alert(month.value + "-" + date.value + " is an invalid date");
  }else
  {
    $.getJSON('/pythonScript', {
      type: select.value,
      dataOne: month.value,
      dataTwo: date.value
    }, function(data) {
        console.log(data);

        $('.image').show();
        var image = document.getElementById("image");

        switch(select.value)
        {
          case "1":
            if(date.value == 0)
            {
              image.src = "../static/image/" + month.value + "_hour.png";
            }else {
              image.src = "../static/image/" + month.value + "_" + date.value + "_hour.png";
            }
            break;
          case "2":
            image.src = "../static/image/hour.png";
            break;
          case "3":
            image.src = "../static/image/month.png";
            break;
          case "4":
            if(date.value == 0)
            {
              image.src = "../static/image/" + month.value + "_pickup.png";
            }else {
              image.src = "../static/image/" + month.value + "_" + date.value+ "_pickup.png";
            }
            break;
          case "5":
            if(date.value == 0)
            {
              image.src = "../static/image/" + month.value + "_dropoff.png";
            }else {
              image.src = "../static/image/" + month.value + "_" + date.value + "_dropoff.png";
            }
            break;
          default:
            return;
        }
    });
  }
}

function doSelect()
{
  var month = document.getElementById("month");
  month.value = 0;
  var date = document.getElementById("date");
  date.value = 0;

  var select = document.getElementById("select");

  if(select.value==1 || select.value==4 || select.value==5)
  {
    $('.month').show();
    $('.date').show();
  }else
  {
    $('.month').hide();
    $('.date').hide();
  }
}
