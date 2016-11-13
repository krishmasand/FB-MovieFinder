chrome.runtime.onMessage.addListener(function(message) {
    if (message && message.type == 'copy') {
        var input = document.createElement('textarea');
        document.body.appendChild(input);
        if(message.text != "There are no movie suggestions :("){
	        input.value = message.text;
	        input.focus();
	        input.select();
	        document.execCommand('Copy');
	        input.remove();

	        chrome.notifications.clear("1");
	  		chrome.notifications.create(
	          "1",
	          {
	            type:'basic',
	            iconUrl:chrome.runtime.getURL("icon.png"),
	            title : "Copied Movie Suggestions to clipboard!",
	            message : "",
	            isClickable: true
	            
	          },
	          function() {
	            console.log(chrome.runtime.lastError);
	          }
	        );

	        //alert("copied");
        }
        else{
        	chrome.notifications.clear("1");
	  		chrome.notifications.create(
	          "1",
	          {
	            type:'basic',
	            iconUrl:chrome.runtime.getURL("icon.png"),
	            title : "There are no movie suggestions :(",
	            message : "",
	            isClickable: true
	            
	          },
	          function() {
	            console.log(chrome.runtime.lastError);
	          }
	        );
        }

    }
    else if(message && message.type == 'copying'){
        chrome.notifications.clear("1");
  		chrome.notifications.create(
          "1",
          {
            type:'basic',
            iconUrl:chrome.runtime.getURL("icon.png"),
            title : "Looking up movies...",
            message : "",
            isClickable: true
            
          },
          function() {
            console.log(chrome.runtime.lastError);
          }
        );
    }
    else if(message && message.type == 'none'){
        chrome.notifications.clear("1");
  		chrome.notifications.create(
          "1",
          {
            type:'basic',
            iconUrl:chrome.runtime.getURL("icon.png"),
            title : "Not enough information to parse",
            message : "",
            isClickable: true
            
          },
          function() {
            console.log(chrome.runtime.lastError);
          }
        );
    }
});