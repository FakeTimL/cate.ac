// See: https://facelessuser.github.io/pymdown-extensions/extensions/arithmatex/#loading-katex
// See: https://highlightjs.org/usage/

(function () {
  'use strict';

  var onReady = function onReady(fn) {
    if (document.addEventListener) {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      document.attachEvent("onreadystatechange", function () {
        if (document.readyState === "interactive") {
          fn();
        }
      });
    }
  };

  var addStyling = function (selector, classes) {
    var elems = document.querySelectorAll(selector);
    for (var i = 0; i < elems.length; i++) {
      elems[i].className += ' ' + classes;
    }
  }

  onReady(function () {
    if (typeof katex !== 'undefined') {
      var maths = document.querySelectorAll('.arithmatex');
      for (var i = 0; i < maths.length; i++) {
        var tex = maths[i].textContent || maths[i].innerText;
        // Arithmatex handles `$$...$$` incorrectly.
        if (tex.startsWith('\\(\\(') && tex.endsWith('\\)\\)')) {
          katex.render(tex.slice(4, -4), maths[i], { 'displayMode': true });
        } else if (tex.startsWith('\\(') && tex.endsWith('\\)')) {
          katex.render(tex.slice(2, -2), maths[i], { 'displayMode': false });
        }
      }
    }
    if (typeof hljs !== 'undefined') {
      hljs.highlightAll();
    }
    // Add styling classes to markdown content.
    addStyling('.markdown h1', 'ui header');
    addStyling('.markdown h2', 'ui header');
    addStyling('.markdown h3', 'ui header');
    addStyling('.markdown h4', 'ui header');
    addStyling('.markdown h5', 'ui header');
    addStyling('.markdown h6', 'ui header');
    addStyling('.markdown ul', 'ui bulleted list');
    addStyling('.markdown ul li', 'item');
    addStyling('.markdown ol', 'ui list');
    addStyling('.markdown ol li', 'item');
    addStyling('.markdown table', 'ui celled table');
    addStyling('.markdown img', 'ui centered medium rounded image');
    addStyling('.markdown hr', 'ui divider');
  });

}());
