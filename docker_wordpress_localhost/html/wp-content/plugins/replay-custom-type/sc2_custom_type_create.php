<?php
/*
Plugin Name: Register Sc2Repalys as Custom Post Types
Plugin URI: http://oranbar.com/sry_doesnt_exist
Description: Plugin to register a custom type for Sc2 Replay Analysis powered by
Version: 1.0
Author: Oran Bar
Author URI:http://oranbar.com
*/
require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
require_once(ABSPATH . 'wp-admin/includes/file.php');

$project_prefix = 'Sc2Sensei_'; #Make customizable parameter
$version = '1';

add_action('init', 'initialize_sc2_db_structures');
// add_action('init', 'create_plugin_database_tables');

function initialize_sc2_db_structures(){
	create_replay_posttype();
	create_plugin_database_tables();
	register_rest_api();
}

function create_replay_posttype()
{
	
	register_post_type(
		'replay',
		// CPT Options
		array(
			'labels' => array(
				'name' => __('Replays'),
				'singular_name' => __('Replay'),
				'view_item' => __('View Replays'),
				'search_items' => __('Search Replays'),
				'not_found' =>  __('No Replays Found')
			),
			'has_archive' => true,
			'hierarchical' => false,
			'rewrite' => array('slug' => 'replays'),
			'show_in_rest' => true,
			'public' => true,
			// 'supports' => array(
			// 	'title',
			// 	'editor',
			// 	'excerpt',
			// 	'custom-fields',
			// 	'thumbnail',
			// 	'page-attributes'
			// ),
			// 'taxonomies' => 'category',
		)
	);
}
// Hooking up our function to theme setup
// Working Rest URL Link for LocalHost wordpress
// http://localhost:8000/wp-json/sc2_sensei/replays_api/v1/test_get
// http://localhost:8000/?rest_route=/sc2_sensei/replays_api/v1/test_get
function register_rest_api(){
	add_action(
		'rest_api_init',
		function () {
			global $version;
			$namespace = 'sc2_sensei/replays_api/v' . $version;

			register_rest_route($namespace, 'test_get', [
				'methods' => 'GET',
				'callback' => 'test_get',
			]);

			register_rest_route($namespace, 'test_post', [
				'methods' => 'POST',
				'callback' => 'test_post',
			]);

			register_rest_route($namespace, 'upload_analyzed_replay', [
				'methods' => 'POST',
				'callback' => 'upload_analyzed_replay',
			]);
		}
	);
}

function create_plugin_database_tables()
{
	create_replays_table();
	create_replay_macro_timelines_table();
}

function add_prefixes($tableFullName){
	global $wpdb;
	global $project_prefix;

	return 'ob_' . $project_prefix . "$tableFullName";
}

# Tables Creation ##################

function table_doesnt_exist($tableFullName){
	global $wpdb;

	return $wpdb->get_var( "show tables like '$tableFullName'" ) != $tableFullName;
}

function create_replays_table(){
	global $wpdb;
	$table_name = add_prefixes('replays');

	$charset_collate = $wpdb->get_charset_collate();

	#Check to see if the table exists already, if not, then create it
	if(table_doesnt_exist($table_name)){

		$sql = "CREATE TABLE $table_name (
			replay_index INT NOT NULL AUTO_INCREMENT,
			upload_time DATETIME NOT null,
			owner_user_id INT,
			
			PRIMARY KEY( replay_index )

		)    $charset_collate;";

		dbDelta($sql);
	}
}

function create_replay_macro_timelines_table()
{
	global $wpdb;
	$table_name = add_prefixes('replay_macro_timelines');

	$charset_collate = $wpdb->get_charset_collate();

	#Check to see if the table exists already, if not, then create it
	if (table_doesnt_exist($table_name)) {

		$sql = "CREATE TABLE $table_name (
			replay_index INT NOT NULL AUTO_INCREMENT,
			event_name VARCHAR(70) NOT NULL ,
			start_time_seconds INT NOT NULL ,
			end_time_seconds INT NOT NULL ,
			building_name VARCHAR(50) NOT NULL ,

			PRIMARY KEY( replay_index, building_name, end_time_seconds )

		)    $charset_collate;";

		dbDelta($sql);
	}
}

# Tables Add Entry ##################

function upload_analyzed_replay()
{
	global $wpdb;
	$table_name = add_prefixes('replay_macro_timelines');
	if(isset($_POST)){
		$post_data = json_decode(stripcslashes($_POST['data']));

		print_r( json_decode(stripcslashes($_POST['data']))[0][0]->end_time );
	} else {
		echo "Goddamn, I shouldn't be here! I'm ufficially lost....";
	}
}

function add_replay_macro_timelines(){
	//TODO
	global $wpdb;
	$table_name = add_prefixes('replay_macro_timelines');

	$entityBody = file_get_contents('php://input');
	// error_log($entityBody);

	$data = [];
	$data = json_decode($entityBody);
	$errors = false;
	foreach($data->notesData->notesList as $note) {
		// print_r(json_encode($note));

		$insert_successful = insert_note_in_developer_notes_table($note, $data->deviceId);

		if($insert_successful == false){
			$errors = true;
			echo "Failed to insert note";
			print_r($note);
		}
		// echo $noteJson;
		// print_r($note);
		//print_r("----------------");
	}
	if($errors == false){
		echo "Success: All notes inserted";
	}
}

function insert_note_in_developer_notes_table($note, $sending_device_id){
	global $wpdb;
	$table_name = add_prefixes('developer_notes');
	$current_time = current_time('mysql', 1);

	$encoded_note_json = json_encode($note);
	$note_content_hash = hash('md5', $encoded_note_json);

	$data = array(
		'note' => $encoded_note_json, 
		'note_id' => $note->note_id, 
		'last_updated_time' => $current_time,
		'updated_by' => $sending_device_id,
		'note_content_hash' => $note_content_hash,
		'content' => $note->content
	);


	$duplicate_note_hash = $wpdb->get_var(
		"SELECT note_content_hash FROM $table_name
			WHERE note_id = '$note->note_id';"
	);

	$success = 0;
	if(!$duplicate_note_hash){
		$data['creation_time'] = $current_time;
		$data['created_by'] = $sending_device_id;
		$success = $wpdb->insert($table_name, $data);
	} else if( $duplicate_note_hash != $note_content_hash ){
		$where = [ 'note_id' => $note->note_id ];
		$success = $wpdb->update($table_name, $data, $where);
	} else {
		//No update needed because hash matches the one in DB
		$success = true;
	}

	return $success;
}

##################################

# Queries ##################

function get_developer_notes(){
	global $wpdb;
	$table_name = add_prefixes('developer_notes');
	
	$sql = "SELECT note FROM $table_name;"; 
	
	$query_rslt = $wpdb->get_results( $sql );
	
	$data = [];
	foreach($query_rslt as $key =>$entry){
		$data['notesList'][$key] = json_decode($entry->note);
		// $data['notesList'][$key]['note'] = json_decode($entry->note);
	}
	print_r(json_encode($data));
	// return json_encode($data);
}
##################################




function test_get()
{
	return rest_ensure_response('Hello World, this is the WordPress REST API');
}

function test_post()
{
	print_r($_POST);
	echo 'success (post)';
}
