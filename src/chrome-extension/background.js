// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

chrome.runtime.onInstalled.addListener(function() {

  chrome.storage.local.set({"current_url": null}, function() {
    console.log("initializing urlset");
  });

  chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    chrome.storage.local.get(["current_url"], function(result) {

      if(result.current_url == sender.tab.url) {
        console.log("redundant");
        return;
      } else {

        chrome.storage.local.set({"current_url": sender.tab.url}, function() {
          console.log("processing url");

          var requestUrl = "http://52.52.89.74/url"
          var xhr = new XMLHttpRequest();
          xhr.open('POST', requestUrl, true);
          xhr.setRequestHeader("Content-Type", "application/json");
          xhr.onload = function(){
            console.log('getFinalUrl', xhr.responseURL);
            sendResponse(this.response);
          };
          xhr.send(JSON.stringify({url: sender.tab.url}));
        });
      }
    });


    return true;

  });
});
