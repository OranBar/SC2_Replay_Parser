<?php
/*
Template Name: Main-Page
*/
get_header();
?>

<!-- Page Content -->
<div class="container-fluid">

  <!-- Page Heading -->
  <h1 class="my-4">Oran Bar
    <small>Projects</small>
  </h1>

  <div class="row">
    <div class="col-lg-4 mb-4">
      <div class="card h-100">
        <div class="card-header">
          <a href="#">
            <h3 class="text-center">Auto</h3>
        </div>
        <a href="#"><img class="card-img-top" src="<?php echo esc_url(site_url()); ?>/wp-content/uploads/2020/09/autoattribute_cover_img.png" alt=""></a>
        <div class="card-body" style="display: flex;">
          <!-- <h4 class="card-title">
            <a href="#">Auto</a>
          </h4> -->
          <div class="align-self-end">

            <p class="card-text">A small tool for Unity3D development. [Auto] is a set of attributes applicable to Unity Scripts, which will automatically fetch component variables and assign their value.</p>
          </div>
        </div>
      </div>
    </div>
    <div class="col-lg-4 mb-4">
      <div class="card h-100">
        <div class="card-header">
          <a href="#">
            <h3 class="text-center">Pac-man MCTS</h3>
        </div>
        <a href="#"><img class="card-img-top" src="<?php echo esc_url(site_url()); ?>/wp-content/uploads/2020/10/mrspacman.jpg" alt=""></a>
        <div class="card-body" style="display: flex;">
          <!-- <h4 class="card-title">
            <a href="#">Pac-man MCTS</a>
          </h4> -->
          <div class="align-self-end">
            <p class="card-text">An AI that plays Mrs. Pacman (Java) using a Monte Carlo Tree Search for its decision making process. Some of the parameters of the MCTS were further optimized using a Genetic Algorithm</p>
          </div>
        </div>
      </div>
    </div>
    <div class="col-lg-4 mb-4">
      <div class="card h-100">
        <div class="card-header">
          <a href="#">
            <h3 class="text-center">Wallpaper Changer</h3>
        </div>
        <a href="#"><img class="card-img-top" src="<?php echo esc_url(site_url()); ?>/wp-content/uploads/2020/10/WallpaperChanger.jpg" alt=""></a>
        <div class="card-body" style="display: flex;">
          <!-- <h4 class="card-title">
            <a href="#">Wallpaper Changer</a>
          </h4> -->
          <div class="align-self-end">
            <p class="card-text">Android app that changes wallpaper every x minutes. The next wallpaper will be chosen at random. The app takes as input parameter any number of directories where the wallpapers are stored, and will automatically add new images to the cycle.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- /.row -->

    <!-- Pagination -->
    <ul class="pagination justify-content-center">
      <li class="page-item">
        <a class="page-link" href="#" aria-label="Previous">
          <span aria-hidden="true">&laquo;</span>
          <span class="sr-only">Previous</span>
        </a>
      </li>
      <li class="page-item">
        <a class="page-link" href="#">1</a>
      </li>
      <li class="page-item">
        <a class="page-link" href="#">2</a>
      </li>
      <li class="page-item">
        <a class="page-link" href="#">3</a>
      </li>
      <li class="page-item">
        <a class="page-link" href="#" aria-label="Next">
          <span aria-hidden="true">&raquo;</span>
          <span class="sr-only">Next</span>
        </a>
      </li>
    </ul>

  </div>
  <!-- /.container -->

  <?php
  get_footer();
