<?php
/*
Template Name: Login-Page
*/


get_header(); ?>
<div class="container text-center">
	<div class="row justify-content-center">
		<div class="col-md-6">
			<!--

				<img class="rounded mb-3 mt-5" src="splash-page-logo.png" class="img-fluid" /></div>
</div>
-->
			<!-- <img class="mb-4" src="https://www.oranbar.com/wp/wp-content/uploads/2020/09/dda8s6m-4091f1f2-5e8e-46a7-b3c5-610b060bbe28.png" alt="" width="172" height="172"> -->

			<form class="form-signin needs-validation" name="loginform" id="loginform" action="<?php echo esc_url( site_url( 'wp-login.php', 'login_post' ) ); ?>" method="post" novalidate>
			 	<img class="rounded mb-3 mt-5 img-fluid mx-auto d-block"
					src="<?php echo esc_url( site_url() ); ?>/wp-content/uploads/2020/09/yorha.jpg" style="max-width:325px;">
				<!--
<h1 class="h3 mb-3 font-weight-normal">Please sign in</h1>
-->

				<!-- <a href="file:///C:/Users/Oran/Downloads/bootstrap-4.0.0/bootstrap-4.0.0/docs/4.0/examples/floating-labels/index.html" class="btn btn-outline-primary mr-1">Sign up</a> -->
				<!--
<h4 class="card-title mb-4 mt-1 ml-1 float-left">Sign in</h4>
-->	
				
				<label for="user_login" class="sr-only">E-mail</label>
				<input type="text" name="log" id="user_login" class="form-control mb-2" placeholder="E-mail" required
					autofocus="" value="<?php echo esc_attr( $user_login ); ?>" autocapitalize="off" pattern="[A-Za-z]{3,}@[A-Za-z]{3,}[.][A-Za-z]{2,}"/>
				<h2 class="invalid-feedback mb-1" style="text-align:left;">
					Inserire una e-mail valida
				</h2>
			
				<label for="user_pass" class="sr-only">Password</label>
				<input type="password" name="pwd" id="user_pass" class="form-control" placeholder="Password" required value="" pattern="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"/>
				<h2 class="invalid-feedback mb-1" style="text-align:left;">
					La password deve contenere almeno 8 caratteri, di cui una lettera ed un numero
				</h2>

				<p class="submit">
					<p class="forgetmenot"><input name="rememberme" type="hidden" id="rememberme" value="forever"> </p>
					<input type="hidden" name="redirect_to" value="<?php echo esc_attr( admin_url() ); ?>" />
					
					<input type="hidden" name="testcookie" value="1" />
				</p>
				
				<!--
<div class="checkbox mb-3">
			<label>
			<input type="checkbox" value="remember-me"> Remember me
			</label></div>
-->
				<!--
<div class="container"> -->
				<div class="row">
					<div class="col-6 pr-1">
						<button class="btn btn-lg btn-primary btn-block mt-3 pr-3" type="submit" name="wp-submit" id="wp-submit" >Accedi</button></div>
					<div class="col-6">
						<class="btn btn-lg btn btn-block mt-3 border-success" >Registrati</class=>
					</div>
				</div>
				<!--</div>
-->

				<hr>

				<button class="btn btn-lg btn-block border-danger" type="submit"><i class="fab fa-google mr-2"
						style="color:#ea4335"></i>Continua con Google</button>
				<button class="btn btn-lg btn-block border-primary" type="submit"><i class="fab fa-facebook-f mr-2"
						style="color:#3b5998"></i>Continua con Facebook</button>

				<hr>

				<a href=""> Non ricordi la password? Nessun problema, clicca qui!</a>
				<p class="mt-5 mb-3 text-muted">© BarbarO 2020</p>

			</form>
		</div>
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