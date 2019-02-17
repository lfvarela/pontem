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

document.getElementById("error").style.display = "none"

let currentArticleTitle = document.getElementById("currentArticleTitle");

let currentArticleAuthors = document.getElementById("currentArticleAuthors");

let relatedArticles = document.getElementById("relatedArticles");

let currentScore = document.getElementById("currentScore")

chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
  var requestUrl = "http://52.52.89.74:5000/url"
  var xhr = new XMLHttpRequest();
  xhr.open('POST', requestUrl, true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onload = function(){
    console.log(JSON.parse(this.response));
    document.getElementById("loader").style.display = "none";
    if(!JSON.parse(this.response).ok) {
      document.getElementById("error").style.display = "block";
    } else {
      document.getElementById("loaded").style.visibility = "visible";
      setupPage(JSON.parse(this.response));
    }
  };
  xhr.send(JSON.stringify({url: tabs[0].url}));
  // chrome.tabs.sendMessage(tabs[0].id, {
  //   type: "redirect",
  //   redirect: article["recommendations"][index].url,
  // });
  // window.close();
});

// chrome.storage.local.get("article", (article) => {
//   console.log('The article is');
//   const toSet = JSON.parse(article.article);
//   console.log(toSet);
//   setupPage(toSet)
// });

// chrome.storage.onChanged.addListener((changes, namespace) => {
//   if(changes["article"]){
//     const article = changes["article"];
//     console.log(article);
//     setupPage(JSON.parse(article.article));
//   }
// });

function setupPage(article){
  currentArticleTitle.innerHTML = article.title;
  currentArticleAuthors.innerHTML = article.authors[0];
  currentScore.innerHTML = Math.round(article.sentiment);

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
        // chrome.tabs.sendMessage(tabs[0].id, {
        //   type: "redirect",
        //   redirect: article["recommendations"][index].url,
        // });
        //TODO: redirect tab
        chrome.tabs.update(tabs[0].id,
          {url: article["recommendations"][index].url}, 
          function(){
            document.getElementById("loaded").style.visibility = "hidden";
            document.getElementById("loader").style.display = "block";
            window.close();
          }
        )
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
  return '<div class="articleContainer" id='+index+'> <div class="titleContainer"><h2 class="articleTitle">'+ page.title + '</h2>' + '<h3>'+page.authors[0]+'</h3>'+'</div> <div class="score">' + Math.round((100*page.sentiment)/10) + '</div> </div>';
}

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  console.log('RECIEVING MESSAGE');
  if(message.type === "redirect"){
    console.log('HANDLING MESSAGE');
    location.replace(message.redirect)
  }
});

// chrome.browserAction.onClicked.addListener(function(tab) {
//   console.log('tab', tab);
//   window.close();
// });
