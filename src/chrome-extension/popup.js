// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';
// chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
//   if(message.type === "updateData"){
//     let currentArticleTitle = document.getElementById('currentArticleTitle');
//     currentArticleTitle.innerHTML = message.payload.title;
//     console.log("Updating popup");
//     console.log(message.payload);
//   }
// });

let currentArticleTitle = document.getElementById("currentArticleTitle");


let testButton = document.getElementById("testButton");
testButton.onclick = (element) => {
  console.log("clicked test button");
}

chrome.storage.local.get("article", (article) => {
  console.log('The article is');
  console.log(article);
  const toSet = JSON.parse(article.article);
  currentArticleTitle.innerHTML = toSet.title;
});

chrome.storage.onChanged.addListener((changes, namespace) => {
   if(changes["article"]){
     const article = changes["article"];
     console.log(article);
   }
});
