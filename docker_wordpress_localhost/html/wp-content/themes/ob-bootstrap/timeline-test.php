<?php
/*
Template Name: Timeline
*/


get_header(); ?>
<div class="container text-center">
	<div class="row justify-content-center">
		<div id="chart">
		</div>
	</div>
</div>


<script>
	(function() {
		'use strict';
		window.addEventListener('load', function() {
			var options = {
				series: [
					// SCV
					{
						name: 'SCV',
						data: [{
								x: 'Main CC',
								y: [0, 12]
							},
							{
								x: 'Main CC',
								y: [12, 24]
							},
							{
								x: 'Main CC',
								y: [24, 36]
							},
							{
								x: 'Main CC',
								y: [42, 54]
							},

							{
								x: 'Natural CC',
								y: [0, 12]
							},
							{
								x: 'Natural CC',
								y: [16, 28]
							},
							{
								x: 'Natural CC',
								y: [42, 54]
							},
						]
					},
					//Idle
					{
						name: 'Idle',
						data: [{
								x: 'Main CC',
								y: [36, 42]
							},
							{
								x: 'Main CC',
								y: [54, 64]
							},

							{
								x: 'Natural CC',
								y: [12, 16]
							},
							{
								x: 'Natural CC',
								y: [28, 42]
							},
						]
					},

				],
				chart: {
					height: 350,
					width: 800,
					type: 'rangeBar'
				},
				plotOptions: {
					bar: {
						horizontal: true,
						barHeight: '50%',
						distributed: false,
						// startingShape: 'rounded',
						// endingShape: 	'rounded',
						// barWidth: '55%',
						// columnWidth: '50%',
						rangeBarGroupRows: true
						
					}
				},
				colors: [
					"#008FFB", "#D7263D", "#FEB019", "#00E396", "#775DD0",
					"#3F51B5", "#546E7A", "#D4526E", "#8D5B4C", "#F86624",
					"#FF4560", "#1B998B", "#2E294E", "#F46036", "#E2C044"
				],
				fill: {
					type: 'solid'
				},
				xaxis: {
					type: 'datetime'
				},
				legend: {
					position: 'right'
				},
				grid: {
					show : true,
					padding: {
						top: 5,
						right: 5,
						bottom: 5,
						left: 5
					},
				}
				
				// tooltip: {
				// 	custom: function(opts) {
				// 		const fromYear = new Date(opts.y1).getFullYear()
				// 		const toYear = new Date(opts.y2).getFullYear()
				// 		const values = opts.ctx.rangeBar.getTooltipValues(opts)

				// 		return (
				// 			''
				// 		)
				// 	}
				// }
			};

			var chart = new ApexCharts(document.querySelector("#chart"), options);
			chart.render();
		}, false);
	})();
</script>
</body>

</html>