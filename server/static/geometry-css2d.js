"use strict";
// CSS2D renderer

function initCanvas(elCanvas, width, height) {
  elCanvas.innerHTML = "";
  elCanvas.className = "geometry_canvas";
  elCanvas.style.height = height.toString() + "px";
  elCanvas.style.width = width.toString() + "px";
  return elCanvas;
}

function drawText(elCanvas, x, y, text, fontSize, color) {
  var div = document.createElement("DIV");
  div.appendChild(document.createTextNode(text));
  elCanvas.appendChild(div);
  div.classList = "geometry_text";
  div.style.transform = "translate(" + x + "px, " + y + "px)";

  // Optional drawing parameters
  if (fontSize) div.style.fontSize = fontSize + "px";
  if (color) {
    var s = "rgba(" + color[0] + ", " + color[1] + ", " + color[2] + ", " + color[3] + ")";
    div.style.color = s;
  }

  return div;
}

function drawPoint(elCanvas, x, y, size, color) {
  var div = document.createElement("DIV");
  elCanvas.appendChild(div);
  div.classList = "geometry_point";
  div.style.transform = "translate(" + x + "px, " + y + "px)";

  // Optional drawing parameters
  if (size) {
    div.style.margin = (-size) + "px";
    div.style.width = (size * 2) + "px";
    div.style.height = (size * 2) + "px";
    div.style.borderRadius = size + "px";
  }
  if (color) {
    var s = "rgba(" + color[0] + ", " + color[1] + ", " + color[2] + ", " + color[3] + ")";
    div.style.backgroundColor = s;
  }

  return div;
}

function drawLine(elCanvas, x0, y0, x1, y1, thickness, color) {
  var xd = x1 - x0, yd = y1 - y0, theta = Math.atan2(yd, xd);

  var div = document.createElement("DIV");
  elCanvas.appendChild(div);
  div.classList = "geometry_line";
  div.style.width = Math.sqrt(xd * xd + yd * yd) + "px";
  div.style.transform = "translate(" + x0 + "px, " + y0 + "px) rotate(" + theta + "rad)";

  // Optional drawing parameters
  if (thickness) {
    div.style.margin = (-thickness) + "px";
    div.style.height = (thickness * 2) + "px";
    div.style.width = (Math.sqrt(xd * xd + yd * yd) + thickness * 2) + "px";
    div.style.borderRadius = thickness + "px";
    div.style.transformOrigin = thickness + "px center";
  }
  if (color) {
    var s = "rgba(" + color[0] + ", " + color[1] + ", " + color[2] + ", " + color[3] + ")";
    div.style.backgroundColor = s;
  }

  return div;
}

function drawTriangle(elCanvas, x0, y0, x1, y1, x2, y2, color) {
  var l01 = Math.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0));
  var l12 = Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
  var l20 = Math.sqrt((x0 - x2) * (x0 - x2) + (y0 - y2) * (y0 - y2));
  var l = Math.max(l01, l12, l20) * Math.sqrt(2); // Ensure high resolution (?)

  var div = document.createElement("DIV");
  elCanvas.appendChild(div);
  div.classList = "geometry_triangle";
  div.style.borderWidth = (l / 2) + "px"; // Ensure high resolution (?)
  // CSS 2D transform matrix:
  // / a c tx \
  // \ b d ty /
  var tx = x0, ty = y0;
  var c = (x1 - tx) / l, d = (y1 - ty) / l;
  var a = (x2 - tx) * 2 / l - c, b = (y2 - ty) * 2 / l - d;
  div.style.transform = "matrix(" + a + ", " + b + ", " + c + ", " + d + ", " + tx + ", " + ty + ")";

  // Optional drawing parameters
  if (color) {
    var s = "rgba(" + color[0] + ", " + color[1] + ", " + color[2] + ", " + color[3] + ")";
    div.style.borderLeftColor = s;
  }

  return div;
}
