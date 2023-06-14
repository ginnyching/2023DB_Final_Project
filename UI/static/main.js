let select = document.getElementById("select");
select.addEventListener("change", doSelect);

$('.location').hide();
$('.date').hide();
$('.hour').hide();
$('.slider').hide();
$('.sliderValue').hide();
$('.search').hide();
$('.image').hide();

document.getElementById("slider").oninput = function(e)
{
    var hour = document.getElementById("slider").value;
    document.getElementById('sliderValue').innerHTML = hour + " o'clock";

    var image = document.getElementById("image");
    image.src = "../static/image/image (" + hour + ").png";

    console.log(hour);
};

$('.search').on('click', function(e)
{
  const selectValue = select.options[select.selectedIndex].value;

  switch(selectValue)
  {
    case "1":
      locationDate();
      break;
    case "2":
      dateHour();
      break;
    case "3":
      hour();
      break;
    default:
      return;
  }

  console.log(selectValue);
});

function doSelect()
{
  const selectValue = select.options[select.selectedIndex].value;

  reset();

  switch(selectValue)
  {
    case "1":
      $('.location').show();
      $('.date').show();
      $('.hour').hide();
      $('.slider').hide();
      $('.sliderValue').hide();
      break;
    case "2":
      $('.location').hide();
      $('.date').show();
      $('.hour').show();
      $('.slider').hide();
      $('.sliderValue').hide();
      break;
    case "3":
      $('.location').hide();
      $('.date').show();
      $('.hour').hide();
      break;
    default:
      return;
  }

  $('.search').show();
}

function locationDate()
{
  var location = document.getElementById("location").value;
  var date = document.getElementById("date").value;

  console.log("locationDate");
  console.log(location);
  console.log(date);

  $.getJSON('/pythonScript', {
    type: "1",
    dataOne: location,
    dataTwo: date
  }, function(data) {
      console.log(data);

      $('.image').show();
      var image = document.getElementById("image");
      image.src = "../static/image/image (25).png";
  });
}

function dateHour()
{
  var date = document.getElementById("date").value;
  var hour = document.getElementById("hour").value;

  console.log("dateHour");
  console.log(date);
  console.log(hour);

  $.getJSON('/pythonScript', {
    type: "2",
    dataOne: date,
    dataTwo: hour
  }, function(data) {
      console.log(data);

      $('.image').show();
      var image = document.getElementById("image");
      image.src = "../static/image/image (26).png";
  });
}

function hour()
{
  $('.slider').show();
  $('.sliderValue').show();

  var date = document.getElementById("date").value;
  var slider = document.getElementById("slider").value;

  console.log("date");
  console.log(date);
  console.log(slider);

  $.getJSON('/pythonScript', {
    type: "3",
    dataOne: date,
    dataTwo: slider
  }, function(data) {
      console.log(data);

      $('.image').show();
      var image = document.getElementById("image");
      image.src = "../static/image/image (12).png";
  });
}

function reset()
{
  console.log("reset");
  var temp = document.getElementById("location");
  temp.value = "";
  temp = document.getElementById("date");
  temp.value = "";
  temp = document.getElementById("hour");
  temp.value = "";
  temp = document.getElementById("slider");
  temp.value = 12;
  document.getElementById('sliderValue').innerHTML = "12 o'clock";
}
