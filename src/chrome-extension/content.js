// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

console.log("content!")

chrome.runtime.sendMessage({}, function(response) {
    return true;
});