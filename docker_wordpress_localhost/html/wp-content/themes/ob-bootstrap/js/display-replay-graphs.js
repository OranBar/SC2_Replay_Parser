

(function () {
	'use strict';
	window.addEventListener('load', function () {
		var replay_events_list = JSON.parse(replay_data.events);
		// document.getElementById('dbg').innerHTML = replay_events_list[0]['event_name'];
		var series_data = [];
		var labels_with_duplicates = replay_events_list.map(function (e) { return e.event_name; });
		// var labels_with_duplicates = replay_events_list.map(e => e['building_name']);
		var labels = [...new Set(labels_with_duplicates )]
		
		for (var i = 0; i < labels.length; i++){
			var label = labels[i];
			var building_events = replay_events_list.filter(e => e['event_name'] == label);
			var tmp = [];
			for (var j = 0; j < building_events.length; j++) {
				var b_event = building_events[j];
				var event_time = [b_event['start_time_seconds'], b_event['end_time_seconds']];
				
				var event_obj = { x: b_event['building_name'], y: event_time };
				
				tmp.push(event_obj);
			}
			series_data.push({ name: label, data: tmp });
			// debugger
		}
		
		

		var options = {
			series: series_data ,
			chart: {
				height: 450,
				width: 1400,
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

		var chart = new ApexCharts(document.querySelector("#chart"), options);
		chart.render();
	}, false);
})();