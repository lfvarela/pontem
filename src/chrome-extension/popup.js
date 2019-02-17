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

let currentScore = document.getElementById("currentScore")

chrome.storage.local.get("article", (article) => {
  console.log('The article is');
  const toSet = JSON.parse(article.article);
  console.log(toSet);
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
  currentScore.innerHTML = Math.round(100*article.sentiment);

  var counter = 0
  let firstElement = document.createElement("div");
  for (var i in article["recommendations"]){
    const page = article["recommendations"][i];
    console.log(page);
    var newElement = document.createElement("li");
    newElement.className = "relatedArticle"
    newElement.innerHTML = getArticleHTML(page, i);
    counter += 1
    relatedArticles.appendChild(newElement);
    console.log(newElement);
  }
  for (var i in article["recommendations"]){
    const page = article["recommendations"][i];
    console.log(page);
    let newElement = document.getElementById(i);
    newElement.addEventListener("click", (event) => {
      const index = getElement(event)
      console.log("THE INDEX IS");
      chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
        chrome.tabs.sendMessage(tabs[0].id, {
          type: "redirect",
          redirect: article["recommendations"][index].url,
        });
      });
    });
  }
}

function getElement(event){
  for (var i in event.path){
    if (event.path[i].className === "articleContainer"){
      return event.path[i].id;
    }
  }
  return 0;
}


function getArticleHTML(page, index){
  console.log(index);
  return '<div class="articleContainer" id='+index+'> <div class="titleContainer"><h2 class="articleTitle">'+ page.title + '</h2>' + '<h3>'+page.authors[0]+'</h3>'+'</div> <div class="score">' + Math.round(100*page.sentiment) + '</div> </div>';
}
