chrome.runtime.onMessage.addListener(function(message) {
    if (message && message.type == 'copy') {
        var input = document.createElement('textarea');
        document.body.appendChild(input);
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
});