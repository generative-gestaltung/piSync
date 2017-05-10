window.onload = function() {

  var WEBSOCKET_ROUTE = "/ws";
  


  if(window.location.protocol == "http:"){
    //localhost
    var ws = new WebSocket("ws://" + window.location.host + WEBSOCKET_ROUTE);
  }

  ws.onopen = function(evt) {
    console.log("open");
    document.getElementById("ws-status").innerHTML = "WS connected";
  };

  ws.onmessage = function(evt) {
    console.log("msg",evt.data);
  };

  ws.onclose = function(evt) {
    console.log("close");
  };

  document.getElementById("button_on").onclick = function() {
    var msg = {"cmd": "COMPILE", "code" : editor.getValue()};
    ws.send(JSON.stringify(msg));
  }

  document.getElementById("button_off").onclick = function() {
    var msg = {"cmd": "STOP"};
    ws.send(JSON.stringify(msg));
  }
}
