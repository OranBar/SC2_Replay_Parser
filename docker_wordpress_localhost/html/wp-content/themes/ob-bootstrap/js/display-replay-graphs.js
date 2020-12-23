

(function () {
	'use strict';
	window.addEventListener('load', function () {
		var replay_events_list = JSON.parse(replay_data.events);
		// document.getElementById('dbg').innerHTML = JSON.parse(replay_data.events)[10]['event_id'];
		// series_data = []
		// labels = replay_events_list.map(function (e) { return replay_events_list['event_name']; });
		var labels = replay_events_list.map(e => e['event_name']);
		let uniqueItems = [...new Set(labels)]
		document.getElementById('dbg').innerHTML = uniqueItems;
		

		var options = {
			series: [] ,
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
				show: true,
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

		// var chart = new ApexCharts(document.querySelector("#chart"), options);
		// chart.render();
	}, false);
})();