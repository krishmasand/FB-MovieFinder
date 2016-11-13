var str = '';

var nameParents = document.getElementsByClassName('_17w2');
name = nameParents[0].childNodes[0].textContent;

var nameHeads = document.getElementsByClassName('_ih3 _-ne');

var names = []
names.push(name);

for(i = 0; i < nameHeads.length; i++){
//	console.log("pushing " + nameHeads[i].childNodes[0].textContent);
	names.push(nameHeads[i].childNodes[0].textContent);
}

var times = document.getElementsByClassName('_3oh-');
for(i = 0; i < times.length; i++){
	var message = times[i];
	var par = message.parentNode;
	if(names.indexOf(par.textContent) > -1){
//		console.log("found name is " + message.textContent);
		continue;
	}
	if(message.textContent.substring(0, 17) != "Movie suggestions"){
//		console.log(message.textContent.substring(0, 16) + " id is " + message.id);
		str += "\n" + message.textContent;
	}
	else{
		str = "";
	}
}

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
	if (xhttp.readyState == 4 && xhttp.status == 200) {
		chrome.runtime.sendMessage({
    		type: 'copy',
    		text: xhttp.responseText
		});
	}
};
var lines = str.split(/\r\n|\r|\n/).length
if(lines > 3 || str.length > 20){
	chrome.runtime.sendMessage({
		type: 'copying'
	});
	xhttp.open('POST', 'https://www.marktai.com/csg/category', true);
	//alert(str);
	xhttp.send(str);
}
else{
	chrome.runtime.sendMessage({
		type: 'none'
	});
}