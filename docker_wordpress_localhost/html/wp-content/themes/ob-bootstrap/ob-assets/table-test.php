<?php
/*
Template Name: Table-Test
*/


get_header(); ?>
<div class="container text-center">
	<div class="row justify-content-center">
		<table id="myTable">
			<tr class="header">
				<th style="width:60%;">Name</th>
				<th style="width:40%;">Country</th>
			</tr>
			<tr>
				<td>
					<div class="card" style="width: 18rem;">
						<img class="card-img-top" src="..." alt="Card image cap">
						<div class="card-body">
							<h5 class="card-title">Card title</h5>
							<p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
							<a href="#" class="btn btn-primary">Go somewhere</a>
						</div>
					</div>
				</td>
				<td>
					<div class="card" style="width: 18rem;">
						<img class="card-img-top" src="..." alt="Card image cap">
						<div class="card-body">
							<h5 class="card-title">Card title</h5>
							<p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
							<a href="#" class="btn btn-primary">Go somewhere</a>
						</div>
					</div>
				</td>
			</tr>
			<tr>
				<td>Berglunds snabbkop</td>
				<td>Sweden</td>
			</tr>
			<tr>
				<td>Island Trading</td>
				<td>UK</td>
			</tr>
			<tr>
				<td>Koniglich Essen</td>
				<td>Germany</td>
			</tr>
		</table>
	</div>
</div>

<script>
	/*
jQuery('#user_login').on('change invalid', function() {
    var textfield = jQuery(this).get(0);
    
    // 'setCustomValidity not only sets the message, but also marks
    // the field as invalid. In order to see whether the field really is
    // invalid, we have to remove the message first
    textfield.setCustomValidity('');
    
    if (!textfield.validity.valid) {
    	textfield.setCustomValidity('Email Invalida');  
    } 
});
*/
</script>

<script>
	// Example starter JavaScript for disabling form submissions if there are invalid fields
	(function() {
		'use strict';
		window.addEventListener('load', function() {
			// Fetch all the forms we want to apply custom Bootstrap validation styles to
			var forms = document.getElementsByClassName('needs-validation');
			// Loop over them and prevent submission
			var validation = Array.prototype.filter.call(forms, function(form) {
				form.addEventListener('submit', function(event) {
					if (form.checkValidity() === false) {
						event.preventDefault();
						event.stopPropagation();
					}
					form.classList.add('was-validated');
				}, false);
			});
		}, false);
	})();
</script>
</body>

</html>