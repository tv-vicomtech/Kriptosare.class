<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Landing Page - Start Bootstrap Theme</title>

  <!-- Bootstrap core CSS -->
  <link rel=stylesheet type=text/css href="{{ url_for('static', filename='vendor/bootstrap/css/bootstrap.min.css') }}">

  <!-- Custom fonts for this template -->
  <link rel=stylesheet type=text/css href="{{ url_for('static', filename='vendor/fontawesome-free/css/all.min.css') }}">
  <link rel=stylesheet type=text/css href="{{ url_for('static', filename='vendor/simple-line-icons/css/simple-line-icons.css') }}">

  <link rel=stylesheet type=text/css href="{{ url_for('static', filename='css/landing-page.min.css') }}">
  <script type="text/javascript" src="http://code.jquery.com/jquery.min.js"></script>
  <script type="text/javascript">
  $(document).ready(function(){
  	$("#class").hide();
	$("#address").show();
	$("#confidence").hide();
	$("#label_opt").val("first");
  $('input[name="optradio"]').click(function(){
    val=$(this).val();
    if(val=="first"){
      $("#class").hide();
      $("#address").show();
      $("#confidence").hide();
      $("#label_opt").val("first");
    }
    if(val=="second"){
      $("#class").hide();
      $("#address").hide();
      $("#confidence").hide();
      $("#label_opt").val("second");

    }
    if(val=="third"){
      $("#class").show();
      $("#address").show();
      $("#confidence").show();
      $("#label_opt").val("third");
    }

  });
});
</script>
</head>
<body>

  <!-- Navigation -->
<table class="table table-dark">
  <thead>
  <th scope="col" style="width:15%">
      <img src="../static/img/shield.png" class="rounded" style="margin-left:30px;width:40%" alt="Titanium img">
      </th>
     <th scope="col"><center>
      <h2 class="h2">Kriptosare: Bitcoin Entity Classifier</h2></center>
      </th>
      <th scope="col" style="width:15%">
      <img src="../static/img/logo.png" class="rounded" style="width:100%" alt="Vicomtech img">
     </th>
  </thead>
</table>

  <!-- Masthead -->
  <header class="masthead text-white text-center pt-5 pb-5">
    <div class="overlay"></div>
    <div class="container">
      <div class="row">
      <div class="col-md-10 col-lg-8 col-xl-7 mx-auto">
      <div class="radio form-check-inline" style="float:left; margin-left:10px">
      <label><input type="radio"  id="optradio1" name="optradio" value="first" checked>CLASSIFIER</label>
      </div>
      <div class="radio form-check-inline" style="float:left; margin-left:10px">
      <label><input type="radio"  id="optradio2" name="optradio" value="second">LIST CLASS</label>
      </div>
      <div class="radio form-check-inline" style="float:left; margin-left:10px">
      <label><input type="radio"  id="optradio3" name="optradio" value="third">CONFIDENCE</label>
      </div>
    </div>
  </div>
  <div class="container" style="min-height: 250px;">
      <div class="row">
        <div class="col-md-10 col-lg-8 col-xl-7 mx-auto">
          <form action = "/test" method = "POST">
            <input type="hidden" id="label_opt" name="label_opt" value="first">
              <div class="col-12 col-md-3">
                <button type="submit" class="btn btn-block btn-lg btn-primary">Start!</button>
              </div>
            <div class="form-row">
              <div class="col-12 col-md-9 mb-2 mt-2 mb-md-2">
                <input type="text" name="address" id="address" class="form-control form-control-lg" placeholder="Bitcoin Address">
              </div>
              <div class="col-12 col-md-9 mb-2 mb-md-2">
                <input type="text" name="class" id="class" class="form-control form-control-lg" placeholder="class">
              </div>
                <div class="col-12 col-md-9 mb-2 mb-md-2">
                <input type="text" name="confidence" id="confidence"  class="form-control form-control-lg" placeholder="confidence">
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
   </div>
  </header>
  <div style="margin-left: 10px;"><p><a href="#">Here</a> is possible find information about the accuracy of the classifier and implementation notes<br>Updated until February 5th 2019, 08:13:31 AM, blocks=561.620, Total number addresses in cluster 16.134.407, Total number entities in cluster 311</p></div>
   <!-- result search -->
<br><br>
<div id="content">{% block content %}{% endblock %}</div>

  <!-- Bootstrap core JavaScript -->
  <script type="text/javascript" src="{{ url_for('static', filename='vendor/jquery/jquery.min.js') }}"></script>
  <script type="text/javascript" src="{{ url_for('static', filename='vendor/bootstrap/js/bootstrap.bundle.min.js') }}"></script>

</body>
</html>