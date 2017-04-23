// 
function f(i){
	console.log('----------------[start] in task'+ i +'---------------');	
	var mysql = require('mysql');
	var connection = mysql.createConnection({
	    host     : '192.168.56.101',
	    user     : 'test',
	    password : 'test',
	    database : 'test'
	});
	connection.connect(); // start connection
	connection.query("select id from B limit " + i + "," + (i+10000), function (err, data){
	  ids = data.map(function (i){return i.id}).toString();
	  ids = ids.substring(0, ids.length);
	  connection.query("update B set test2=replace(concat('-start-',test2,'-end-'),'-','=') where id in ("+ids+")",function (err,data){ 
	      if (err){
		 console.log('----------[err] because connection already closed---------');
		 // console.log(err)
		};
	      console.log('------------------[end] in task -----------------------');
	   })	  
	})
    console.log('-----------------connection ready to close-----------------');
    connection.end();  // nodejs will execute this before update !!!! and so update will raise a connection-closed-error...
    console.log('-----------------connection already close------------------');
}

function main(){
    f(0);
    f(10000);
    f(20000);
    f(30000);
    f(40000);
    f(50000);
    f(60000);
    f(70000);
    f(80000);
    f(90000);
}

main()





