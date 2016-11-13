var str = '';
var times = document.getElementsByClassName('_3oh-');
for(i = 0; i < times.length; i++){
	var message = times[i];
	str += "\n" + message.textContent;
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
if(lines > 3){
	chrome.runtime.sendMessage({
		type: 'copying'
	});
	xhttp.open('POST', 'https://www.marktai.com/csg/category', true);
	//alert(str);
	xhttp.send(str);
}