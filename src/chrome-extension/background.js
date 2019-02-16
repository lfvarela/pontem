// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

// chrome.runtime.onInstalled.addListener(function() {
//   chrome.storage.sync.set({color: '#3aa757'}, function() {
//     console.log('The color is green.');
//   });
//   // chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
//   //   chrome.declarativeContent.onPageChanged.addRules([{
//   //     conditions: [new chrome.declarativeContent.PageStateMatcher({
//   //       pageUrl: {hostEquals: 'developer.chrome.com'},
//   //     })],
//   //     actions: [new chrome.declarativeContent.ShowPageAction()]
//   //   }]);
//   // });

chrome.runtime.onInstalled.addListener(function() {
  chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    console.log("ready");
    console.log(sender.tab.url);

    var requestUrl = "http://18.144.34.151/ale"
    var xhr = new XMLHttpRequest();
    xhr.open('POST', requestUrl, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function(){
      console.log('getFinalUrl', xhr.responseURL);
    };
    xhr.send(JSON.stringify({putanginamo: sender.tab.url}));
  });
});
