<?php
/**
 * Template Name: Login-Custom-2
 */

get_header();
?>
    <section id="primary" class="content-area">
        <main id="main" class="site-main" role="main">
            <div class="container">
                <!-- THIS IS THE BODY/CONTENT-->
<div class="container text-center">
	<form class="form-signin">
		<div class="container text-center">
			<img class="rounded mb-3 mt-3 img-fluid mx-auto d-block"
				src="https://login.paper2app.it/wp-content/uploads/2020/08/splash-page-logo-cropped.png"></div>
		<div class="form-group m-0">
			&nbsp;</div>
		<div class="form-group input-group">
			<div class="input-group-prepend">
				<span class="input-group-text"> <i class="fa fa-user"></i> </span></div>
			<label for="inputEmail" class="sr-only">E-mail</label>
			<input type="email" id="inputEmail" class="form-control form-control-lg" placeholder="E-mail" required=""
				autofocus="">

		</div>
		<div class="form-group input-group">
			<div class="input-group-prepend">
				<span class="input-group-text"> <i class="fa fa-key"></i> </span></div>
			<label for="inputPassword" class="sr-only">Password</label>
			<input type="password" id="inputPassword" class="form-control form-control-lg" placeholder="Password"
				required="">

		</div>
		<div class="row mt-4">
			<div class="col-6 pr-1">
				<button class="btn btn-lg btn-primary btn-block pr-3" type="submit">Accedi</button></div>
			<div class="col-6">
				<!-- <button class="btn btn-lg btn-block border-primary" href="https://login.paper2app.it/registrazione/">Registrati</button> -->
				<a class="btn btn-lg btn-block border-primary" href="https://login.paper2app.it/registrazione/"
					role="button">Registrati</a>

			</div>
		</div>

		<hr>

		<!-- 

			<button class="btn btn-lg btn-block border-danger" type="submit"><i class="fab fa-google mr-2"
					style="color:#ea4335"></i>Continua con
				Google</button>
			<button class="btn btn-lg btn-block border" type="submit" style="border-color: #3b5998!important;"><i
					class="fab fa-facebook-f mr-2" style="color:#3b5998"></i>Continua con
				Facebook</button>

<hr>

-->

		<a href=""> Non ricordi la password? Nessun problema, clicca qui!</a>
		<p class="mt-5 mb-3 text-muted">© BarbarO 2020</p>

	</form>
</div>
<!-- .entry-content -->
            </div>
        </main><!-- #main -->
    </section><!-- #primary -->

<?php
get_footer();
