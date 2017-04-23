
// run task cocurrently in js, like gevent in python.
// but js is much more simple cause it support correntency originlly.
function main(){
    	var request = require('request');

	console.log('----------------[start] in task 1---------------');	
	request.get('https://github.com/yxzoro/', function (err,data,a1,a2){console.log('-------[end] in task 1--------')} ); 

	console.log('----------------[start] in task 2---------------');	
	request.get('https://github.com/qdsh2016/', function (err,data,a1,a2){console.log('-------[end] in task 2-------')} ); 

	console.log('----------------[start] in task 3---------------');	
	request.get('https://github.com/mshubian/', function (err,data,a1,a2){console.log('-------[end] in task 3-------')} ); 

	console.log('----------------[start] in task 4---------------');	
	request.get('https://github.com/tobymao/', function (err,data,a1,a2){console.log('-------[end] in task 4-------')} ); 
}

main()
