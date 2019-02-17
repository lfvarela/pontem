// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

console.log("content!")

chrome.runtime.sendMessage({}, (response) => {
    console.log('Calling the response');
    console.log(response);
    chrome.storage.local.set({
      "article": response,
    }, () => {
      console.log('Set local storage');
    });
    // chrome.runtime.sendMessage({
    //   type: "updateData",
    //   payload: response,
    // });
});
