
var currentLimit = 10; 
$( document ).ready(function() {
   var button = document.getElementById("tabSubmit");
   $("#currentLimit").text(currentLimit);
   // add onclick event 
   button.onclick = function() { 
   	var value = $("#tabs").val();
   	 if (parseInt(value) <= 0 || !(isInt(value)) )
   	 {
   	 	$("#error").show();
   	 	$("#bro").css(red);
   	 }
   	 else{
   	  $("#error").hide();
   	  chrome.extension.sendRequest({message: value});
   	  $("#currentLimit").text(value);
   	  currentLimit = value; 
   	 }
   }

});

function isInt(x) {
   var y = parseInt(x, 10);
   return !isNaN(y) && x == y && x.toString() == y.toString();
}