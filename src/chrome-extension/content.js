// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

console.log("content!")

chrome.runtime.sendMessage({
  type: "load",
}, (response) => {
    console.log('Calling the response');
    console.log(response);
    chrome.storage.local.set({
      "article": response,
    }, () => {
      console.log('Set local storage');
    });
});


chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  console.log('RECIEVING MESSAGE');
  if(message.type === "redirect"){
    console.log('HANDLING MESSAGE');
    location.replace(message.redirect)
  }
});
