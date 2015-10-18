// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Search the bookmarks when entering the search keyword.
// $(function() {

//   // $('#search').change(function() {
//   //    $('#bookmarks').empty();
//   //    dumpBookmarks($('#search').val());
//   // });
// });

window.MAX_TABS = 10; 
/*
function isDuplicate(allTabs,newUrl)
{
    var int i = 0; 
    alert("haha");
    while (i<allTabs[tabs.length]){
      if (allTabs[tabs[i].url] == newUrl)
      {
        alert(i);
        alert("Duplicate Tab opened!");
      }
      i++; 
    }
}
*/
function sortTabs(allTabs){
  

  var newArray = [];
  // we sort with a dictionary , based on date tab was last used/created 
  for (var key in allTabs) {
      newArray.push({id: key, date: allTabs[key]});
  }

  newArray.sort(function(a,b) {
      return a.date - b.date;
  });


  return newArray;
}


 
chrome.extension.onRequest.addListener(function(request, sender)
{
  window.MAX_TABS=parseInt(request.message);
});
 


window.allTabs = {};
// Get the initial tab
chrome.tabs.query({}, function (tabs) {
  window.allTabs[tabs[0].id.toString()] = new Date();
});


// on a new tab, lets see if we have a tab with the same URL
chrome.tabs.onCreated.addListener(function(newtab) {
   // alert("haha");
//  isDuplicate(window.allTabs,newtab.url);
  window.allTabs[newtab.id.toString()] = new Date();
});



// If a tab is clicked it gets a new date 
chrome.tabs.onHighlighted.addListener(function(tabs) {
  window.allTabs[tabs.tabIds.toString()] = new Date();
});

chrome.tabs.onRemoved.addListener(function(newtab) {
  delete window.allTabs[newtab.id.toString()];
});


setInterval(function () {
   chrome.tabs.query({}, function (tabs) {
      if (tabs.length > window.MAX_TABS)
      {
        
        sortedTabs = sortTabs(window.allTabs); 
        chrome.tabs.remove(parseInt(sortedTabs[0].id));
        delete window.allTabs[sortedTabs[0].id];
      }

    });
  }, 2000);

function returnMessage(messageToReturn)
{
 chrome.tabs.getSelected(null, function(tab) {
  var joinedMessage = messageToReturn + backgroundScriptMessage; 
  alert("Background script is sending a message to contentscript:'" + joinedMessage +"'");
  chrome.tabs.sendMessage(tab.id, {message: joinedMessage});
 });
} 


