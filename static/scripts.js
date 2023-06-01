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
  });

}());
