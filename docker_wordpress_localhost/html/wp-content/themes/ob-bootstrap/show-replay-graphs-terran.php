<?php
/*
Template Name: Replay Terran
*/

// Check authentification

// Fetch requested replay
// if (isset($_GET['replay_id'])) {
// 	$replay_id = $_GET['replay_id'];

	$events = $wpdb->get_results( "SELECT * FROM `ob_Sc2Sensei_replay_macro_timelines`" );
	// echo print_r($events);

	wp_enqueue_script('display_replay_graphs', get_template_directory_uri() . '/js/display-replay-graphs.js');

	$dataToBePassed = array(
		'events' => json_encode($events)
	);
	wp_localize_script('display_replay_graphs', 'replay_data', $dataToBePassed);

// }

// $timeline_events = sql query

get_header(); ?>

<div class='container'>
	<h1 id='dbg'>Random Blabla </h1>

</div>

<!-- <div class="container text-center">
	<div class="row justify-content-center">
		<div id="chart">
		</div>
	</div>
</div> -->


<?php get_footer(); ?>