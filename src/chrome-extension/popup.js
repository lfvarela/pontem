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

let currentArticleAuthors = document.getElementById("currentArticleAuthors");

let relatedArticles = document.getElementById("relatedArticles");

chrome.storage.local.get("article", (article) => {
  console.log('The article is');
  console.log(article);
  const toSet = JSON.parse(article.article);
  setupPage(toSet)
});

chrome.storage.onChanged.addListener((changes, namespace) => {
  if(changes["article"]){
    const article = changes["article"];
    console.log(article);
  }
});


function setupPage(article){
  currentArticleTitle.innerHTML = article.title;
  currentArticleAuthors.innerHTML = article.authors[0];

  var counter = 0
  let firstElement = document.createElement("div");
  for (var i in article["related articles"]){
    const page = article["related articles"][i];
    console.log(page);
    var newElement = document.createElement("div");
    newElement.className = "relatedArticle"
    newElement.id = counter
    newElement.innerHTML = getArticleHTML(page);
    counter += 1
    relatedArticles.appendChild(newElement);
    console.log(newElement);
  }
  for (var i in article["related articles"]){
    const page = article["related articles"][i];
    let newElement = document.getElementById(i);
    newElement.addEventListener("click", (event) => {
      chrome.runtime.sendMessage({
        type: "redirect",
        redirect: article["related articles"][event.srcElement.id].url,
      });
      });
    }
  }


  function getArticleHTML(page){
    console.log(page);
    return '<h2 class="articleTitle">'+ page.title + '</h2>' + '<h3>'+page.authors[0]+'</h3>'+'<div>' + page.value + '</div>';
  }
