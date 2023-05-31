"use strict";
// Geometry.js core
// Supported renderers: CSS2D

var MathJaxDisabled = false;


// Additional drawing functions
function drawArrowhead(hCanvas, x, y, xdx, xdy, width, length, offset, thickness, color) {
  var l = Math.sqrt(xdx * xdx + xdy * xdy); xdx /= l; xdy /= l;
  var ydx = -xdy, ydy = xdx;
  // Offset (in pixels)
  if (offset) { x += xdx * offset; y += xdy * offset; }
  // Type 1
  // var hLine1 = drawLine(hCanvas, x, y, x + xdx * (-length) + ydx * (width), y + xdy * (-length) + ydy * (width), thickness, color);
  // var hLine2 = drawLine(hCanvas, x, y, x + xdx * (-length) + ydx * (-width), y + xdy * (-length) + ydy * (-width), thickness, color);
  // return [hLine1, hLine2];
  // Type 2
  var hTri = drawTriangle(hCanvas,
    x + xdx * (-length) + ydx * (width), y + xdy * (-length) + ydy * (width),
    x + xdx * (-length) + ydx * (-width), y + xdy * (-length) + ydy * (-width),
    x, y,
    color);
  return hTri;
}


// Matrices
function Matrix(h, w) {
  var r = { "h": h, "w": w, "data": [] };
  for (var i = 0; i < h; i++) for (var j = 0; j < w; j++) r.data.push(0);

  r.get = function (i, j) { return this.data[i * this.w + j]; }
  r.set = function (i, j, v) { this.data[i * this.w + j] = v; }

  r.copy = function () {
    var res = Matrix(this.h, this.w);
    for (var i = 0; i < this.h; i++) for (var j = 0; j < this.w; j++) res.data[i * res.w + j] = this.data[i * this.w + j];
    return res;
  }

  r.getTranspose = function () {
    var res = Matrix(this.w, this.h);
    for (var i = 0; i < this.w; i++) for (var j = 0; j < this.h; j++) res.data[i * res.w + j] = this.data[j * this.w + i];
    return res;
  }

  r.add = function (rhs) {
    console.assert(this.h == rhs.h && this.w == rhs.w, "Adding matrices with incompatible size");
    var res = Matrix(this.h, this.w);
    for (var i = 0; i < this.h; i++) for (var j = 0; j < this.w; j++) res.data[i * res.w + j] = this.data[i * this.w + j] + rhs.data[i * rhs.w + j];
    return res;
  }
  /*
  r.sub = function(rhs) {
    console.assert(this.h == rhs.h && this.w == rhs.w, "Subtracting matrices with incompatible size");
    res = Matrix(this.h, this.w);
    for (var i = 0; i < this.h; i++) for (var j = 0; j < this.w; j++) res.data[i * res.w + j] = this.data[i * this.w + j] - rhs.data[i * rhs.w + j];
    return res;
  }
  */
  r.mul = function (rhs) {
    console.assert(this.w == rhs.h, "Multiplying matrices with incompatible size");
    var res = Matrix(this.h, rhs.w);
    for (var i = 0; i < this.h; i++) for (var j = 0; j < rhs.w; j++) {
      for (var k = 0; k < this.w; k++) res.data[i * res.w + j] += this.data[i * this.w + k] * rhs.data[k * rhs.w + j];
    }
    return res;
  }

  // row[i] *= k
  r.mulRow = function (i, k) { for (var l = 0; l < this.w; l++) this.data[i * this.w + l] *= k; }
  // swap(row[i], row[j])
  r.swapRows = function (i, j) { for (var l = 0; l < this.w; l++) { var t = this.get(i, l); this.set(i, l, this.get(j, l)); this.set(j, l, t); } }
  // row[i] += row[j] * k
  r.mulAndAdd = function (i, j, k) { for (var l = 0; l < this.w; l++) this.data[i * this.w + l] += this.data[j * this.w + l] * k; }

  return r;
}

// Square matrices
function Identity(s) {
  var r = Matrix(s, s);
  for (var i = 0; i < s; i++) r.set(i, i, 1);

  r.getInverse = function () {
    // Gauss-Jordan with partial pivoting
    var n = this.h, t = this.copy();
    var res = Identity(n);
    for (var i = 0; i < n; i++) {
      var p = i;
      for (var j = i + 1; j < n; j++) if (Math.abs(t.get(j, i)) > Math.abs(t.get(p, i))) p = j;
      t.swapRows(i, p); res.swapRows(i, p);
      var k = 1 / t.get(i, i);
      t.mulRow(i, k); res.mulRow(i, k);
      for (var j = i + 1; j < n; j++) {
        var k = -t.get(j, i);
        t.mulAndAdd(j, i, k); res.mulAndAdd(j, i, k);
      }
    }
    for (var i = n - 1; i >= 0; i--) {
      for (var j = 0; j < i; j++) {
        var k = -t.get(j, i);
        t.mulAndAdd(j, i, k); res.mulAndAdd(j, i, k);
      }
    }
    return res;
  }

  return r;
}

// Construct a translation matrix
function Translation(x, y, z) {
  var res = Identity(4);
  res.data[3] = x; res.data[7] = y; res.data[11] = z;
  return res;
}

// Construct a rotation matrix
function Rotation(degrees, x, y, z) {
  var res = Identity(4);
  var norm = Math.sqrt(x * x + y * y + z * z); x /= norm; y /= norm; z /= norm;
  var alpha = degrees * Math.PI / 180, s = Math.sin(alpha), c = Math.cos(alpha), t = 1 - c;
  res.data[0] = t * x * x + c;
  res.data[1] = t * x * y + s * z;
  res.data[2] = t * x * z - s * y;
  res.data[4] = t * x * y - s * z;
  res.data[5] = t * y * y + c;
  res.data[6] = t * y * z + s * x;
  res.data[8] = t * x * z + s * y;
  res.data[9] = t * y * z - s * x;
  res.data[10] = t * z * z + c;
  res.data[15] = 1;
  return res;
}

// Construct a perspective projection matrix
function Perspective(fov, aspect, zNear, zFar) {
  var res = Identity(4);
  var f = 1 / Math.tan(fov * Math.PI / 180 / 2), a = zNear - zFar;
  res.data[0] = f / aspect;
  res.data[5] = f;
  res.data[10] = (zFar + zNear) / a;
  res.data[11] = 2 * zFar * zNear / a;
  res.data[14] = -1;
  return res;
}

// Construct an orthogonal projection matrix
function Orthogonal(left, right, top, bottom, zNear, zFar) {
  var a = right - left, b = top - bottom, c = zFar - zNear;
  var res = Identity(4);
  res.data[0] = 2 / a;
  res.data[3] = -(right + left) / a;
  res.data[5] = 2 / b;
  res.data[7] = -(top + bottom) / b;
  res.data[10] = -2 / c;
  res.data[11] = -(zFar + zNear) / c;
  res.data[15] = 1;
  return res;
}


// NDC to percentage [-50%, 50%]
function N2P(x) { return Math.round(x * 50).toString() + "%"; }
// NDC to pixel [0, n]
function N2PX(x, width) { return width / 2 + x * width / 2; }
function N2PY(y, height) { return height / 2 - y * height / 2; }


// Tag (text)
// text: string, oclock: number, dist: number
function Tag(text_, oclock_, dist_) {
  var r = { "text": text_, "dx": Math.sin(oclock_ / 12 * Math.PI * 2) * dist_, "dy": -Math.cos(oclock_ / 12 * Math.PI * 2) * dist_ };
  return r;
}

// Point: Shape
// name: string / Tag, dim: number, x: number, y: number, z: number, size: number, color: [number, number, number, number]
function Point(name_, x_, y_, z_) {
  var r = { "type": "point", "dim": 0, "name": name_, "x": 0, "y": 0, "z": 0, "size": 1 };
  if (typeof x_ !== "undefined") r.x = x_;
  if (typeof y_ !== "undefined") r.y = y_;
  if (typeof z_ !== "undefined") r.z = z_;
  if (typeof name_ !== "string") { // Tag as name parameter
    r.tag = name_;
    r.name = r.tag.text;
  }

  r.getName = function () { return this.name; }
  r.getVector = function () { var res = Matrix(4, 1); res.data[0] = this.x; res.data[1] = this.y; res.data[2] = this.z; res.data[3] = 1; return res; }
  r.initDraw = function (hCanvas, transform, width, height) {
    var v = transform.mul(this.getVector());
    var x = N2PX(v.data[0] / v.data[3], width), y = N2PY(v.data[1] / v.data[3], height);
    if (this.size) this.hPoint = drawPoint(hCanvas, x, y, this.size, this.color);
    if (this.name) { // Name tag
      var dx = (this.tag ? this.tag.dx : 0), dy = (this.tag ? this.tag.dy : 0);
      this.hTag = drawText(hCanvas, x + dx, y + dy, MathJaxDisabled ? this.name : "$" + this.name + "$");
    }
  }
  r.postTypesetDraw = function (hCanvas, transform, width, height) {
    var v = transform.mul(this.getVector());
    var x = N2PX(v.data[0] / v.data[3], width), y = N2PY(v.data[1] / v.data[3], height);
    if (this.name) { // Name tag
      var w = this.hTag.clientWidth, h = this.hTag.clientHeight; // ##### CSS2D bound
      var dx = (this.tag ? this.tag.dx : 0), dy = (this.tag ? this.tag.dy : 0);
      this.hTag.style.transform = "translate(" + (x - w / 2 + dx) + "px, " + (y - h / 2 + dy) + "px)"; // ##### CSS2D bound
    }
  }

  return r;
}

// Arrowhead: Shape
// dim: number, p: Point, d: Point, size: number, offset: number, thickness: number, color: [number, number, number, number]
function Arrowhead(p_, d_) {
  var r = { "type": "arrowhead", "dim": 0, "p": p_, "d": d_, "size": 3, "thickness": 1 };

  r.getName = function () { return this.name; }
  r.getVector = function () { var res = Matrix(4, 1); res.data[0] = this.p.x; res.data[1] = this.p.y; res.data[2] = this.p.z; res.data[3] = 1; return res; }
  r.getDirectionVector = function () { var res = Matrix(4, 1); res.data[0] = this.d.x; res.data[1] = this.d.y; res.data[2] = this.d.z; return res; }
  r.initDraw = function (hCanvas, transform, width, height) {
    var v = transform.mul(this.getVector()), v1 = transform.mul(this.getVector().add(this.getDirectionVector()));
    var x = N2PX(v.data[0] / v.data[3], width), y = N2PY(v.data[1] / v.data[3], height);
    var x1 = N2PX(v1.data[0] / v1.data[3], width), y1 = N2PY(v1.data[1] / v1.data[3], height);
    this.hArrow = drawArrowhead(hCanvas, x, y, x1 - x, y1 - y, this.size * 0.6, this.size, this.offset, this.thickness, this.color);
  }

  return r;
}

// Line segment: Shape
// dim: number, p0: Point, p1: Point, thickness: number, color: [n, n, n, n], dashes: [number, ...]
function Line(p0_, p1_) {
  var r = { "type": "line", "dim": 1, "p0": p0_, "p1": p1_, "thickness": 1 };

  r.getName = function () { return this.p0.name + this.p1.name; }
  r.getChildren = function () { return [this.p0, this.p1]; };
  r.initDraw = function (hCanvas, transform, width, height) {
    var v0 = transform.mul(this.p0.getVector()), v1 = transform.mul(this.p1.getVector());
    var x0 = N2PX(v0.data[0] / v0.data[3], width), y0 = N2PY(v0.data[1] / v0.data[3], height);
    var x1 = N2PX(v1.data[0] / v1.data[3], width), y1 = N2PY(v1.data[1] / v1.data[3], height);
    if (this.dashes) {
      var dx = x1 - x0, dy = y1 - y0, len = Math.sqrt(dx * dx + dy * dy);
      var cx = x0, cy = y0, clen = 0, i = 0, penDown = true;
      dx /= len; dy /= len;
      this.hLines = [];
      while (clen < len) {
        var seglen = Math.min(this.dashes[i], len - clen);
        if (penDown) this.hLines.push(drawLine(hCanvas, cx, cy, cx + dx * seglen, cy + dy * seglen, this.thickness, this.color));
        cx += dx * seglen; cy += dy * seglen; clen += this.dashes[i]; penDown = !penDown;
        i++; if (i >= this.dashes.length) i = 0;
      }
    }
    else this.hLine = drawLine(hCanvas, x0, y0, x1, y1, this.thickness, this.color);
  }

  return r;
}

var T_ = Tag;
var P_ = Point;
var A_ = Arrowhead;
var L_ = Line;

// Measurement: Shape
// name: string / Tag, dim: number, p0: Point, p1: Point, spacing: number;
// width: number, thickness: number, color: [n, n, n, n]
function Measure(name_, p0_, p1_, spacing_) {
  var r = { "type": "measure", "dim": 1, "name": name_, "p0": p0_, "p1": p1_, "spacing": spacing_, "width": 20, "thickness": 0.5, "color": [0, 0, 0, 1.0] };
  if (typeof name_ !== "string") { // Tag as name parameter
    r.tag = name_;
    r.name = r.tag.text;
  }

  r.getName = function () { return this.p0.name + this.p1.name; }
  r.initDraw = function (hCanvas, transform, width, height) {
    var v0 = transform.mul(this.p0.getVector()), v1 = transform.mul(this.p1.getVector());
    var x0 = N2PX(v0.data[0] / v0.data[3], width), y0 = N2PY(v0.data[1] / v0.data[3], height);
    var x1 = N2PX(v1.data[0] / v1.data[3], width), y1 = N2PY(v1.data[1] / v1.data[3], height);
    var xdx = x1 - x0, xdy = y1 - y0;
    var l = Math.sqrt(xdx * xdx + xdy * xdy); xdx /= l; xdy /= l;
    var ydx = -xdy, ydy = xdx;

    this.hLine0 = drawLine(hCanvas,
      x0 + ydx * this.width / 2, y0 + ydy * this.width / 2,
      x0 + ydx * this.width / 2 + xdx * (l - this.spacing) / 2, y0 + ydy * this.width / 2 + xdy * (l - this.spacing) / 2,
      this.thickness, this.color);
    this.hLine1 = drawLine(hCanvas,
      x1 + ydx * this.width / 2 - xdx * (l - this.spacing) / 2, y1 + ydy * this.width / 2 - xdy * (l - this.spacing) / 2,
      x1 + ydx * this.width / 2, y1 + ydy * this.width / 2,
      this.thickness, this.color);
    this.hLine2 = drawLine(hCanvas, x0, y0, x0 + ydx * this.width, y0 + ydy * this.width, this.thickness, this.color);
    this.hLine3 = drawLine(hCanvas, x1, y1, x1 + ydx * this.width, y1 + ydy * this.width, this.thickness, this.color);

    var size = Math.max(8.0, this.thickness * 8.0);
    this.hArrow0 = drawArrowhead(hCanvas, x0 + ydx * this.width / 2, y0 + ydy * this.width / 2, -xdx, -xdy, size * 0.6, size, 0, this.thickness, this.color);
    this.hArrow1 = drawArrowhead(hCanvas, x1 + ydx * this.width / 2, y1 + ydy * this.width / 2, +xdx, +xdy, size * 0.6, size, 0, this.thickness, this.color);

    if (this.name) { // Name tag
      var x = (x0 + x1 + ydx * this.width) / 2, y = (y0 + y1 + ydy * this.width) / 2;
      var dx = (this.tag ? this.tag.dx : 0), dy = (this.tag ? this.tag.dy : 0);
      this.hTag = drawText(hCanvas, x, y, MathJaxDisabled ? this.name : "$" + this.name + "$");
    }
  }
  r.postTypesetDraw = function (hCanvas, transform, width, height) {
    var v0 = transform.mul(this.p0.getVector()), v1 = transform.mul(this.p1.getVector());
    var x0 = N2PX(v0.data[0] / v0.data[3], width), y0 = N2PY(v0.data[1] / v0.data[3], height);
    var x1 = N2PX(v1.data[0] / v1.data[3], width), y1 = N2PY(v1.data[1] / v1.data[3], height);
    var xdx = x1 - x0, xdy = y1 - y0;
    var l = Math.sqrt(xdx * xdx + xdy * xdy); xdx /= l; xdy /= l;
    var ydx = -xdy, ydy = xdx;

    if (this.name) { // Name tag
      var x = (x0 + x1 + ydx * this.width) / 2, y = (y0 + y1 + ydy * this.width) / 2;
      var w = this.hTag.clientWidth, h = this.hTag.clientHeight; // ##### CSS2D bound
      var dx = (this.tag ? this.tag.dx : 0), dy = (this.tag ? this.tag.dy : 0);
      this.hTag.style.transform = "translate(" + (x - w / 2 + dx) + "px, " + (y - h / 2 + dy) + "px)"; // ##### CSS2D bound
    }
  }

  return r;
}

// Triangle: Shape
// dim: number, p0~p2: Point, l0~l2: Line, color: [n, n, n, n]
function Triangle(p0_, p1_, p2_) {
  var r = { "type": "triangle", "dim": 2, "p0": p0_, "p1": p1_, "p2": p2_ };
  r.l0 = L_(r.p0, r.p1); r.l1 = L_(r.p1, r.p2); r.l2 = L_(r.p2, r.p0);

  r.getName = function () { return this.p0.name + this.p1.name + this.p2.name; }
  r.getChildren = function () {
    return [
      this.p0, this.p1, this.p2,
      this.l0, this.l1, this.l2
    ];
  };
  r.initDraw = function (hCanvas, transform, width, height) {
    if (this.color) {
      var v0 = transform.mul(this.p0.getVector());
      var v1 = transform.mul(this.p1.getVector());
      var v2 = transform.mul(this.p2.getVector());
      var x0 = N2PX(v0.data[0] / v0.data[3], width), y0 = N2PY(v0.data[1] / v0.data[3], height);
      var x1 = N2PX(v1.data[0] / v1.data[3], width), y1 = N2PY(v1.data[1] / v1.data[3], height);
      var x2 = N2PX(v2.data[0] / v2.data[3], width), y2 = N2PY(v2.data[1] / v2.data[3], height);
      this.hTri = drawTriangle(hCanvas, x0, y0, x1, y1, x2, y2, this.color);
    }
  }

  return r;
}

// Quadrilateral: Shape
// dim: number, p0~p3: Point, l0~l3: Line, color: [n, n, n, n]
function Quad(p0_, p1_, p2_, p3_) {
  var r = { "type": "quad", "dim": 2, "p0": p0_, "p1": p1_, "p2": p2_, "p3": p3_ };
  r.l0 = L_(r.p0, r.p1); r.l1 = L_(r.p1, r.p2); r.l2 = L_(r.p2, r.p3); r.l3 = L_(r.p3, r.p0);

  r.getName = function () { return this.p0.name + this.p1.name + this.p2.name + this.p3.name; }
  r.getChildren = function () {
    return [
      this.p0, this.p1, this.p2, this.p3,
      this.l0, this.l1, this.l2, this.l3
    ];
  };
  r.initDraw = function (hCanvas, transform, width, height) {
    if (this.color) {
      var v0 = transform.mul(this.p0.getVector());
      var v1 = transform.mul(this.p1.getVector());
      var v2 = transform.mul(this.p2.getVector());
      var v3 = transform.mul(this.p3.getVector());
      var x0 = N2PX(v0.data[0] / v0.data[3], width), y0 = N2PY(v0.data[1] / v0.data[3], height);
      var x1 = N2PX(v1.data[0] / v1.data[3], width), y1 = N2PY(v1.data[1] / v1.data[3], height);
      var x2 = N2PX(v2.data[0] / v2.data[3], width), y2 = N2PY(v2.data[1] / v2.data[3], height);
      var x3 = N2PX(v3.data[0] / v3.data[3], width), y3 = N2PY(v3.data[1] / v3.data[3], height);
      this.hTri0 = drawTriangle(hCanvas, x0, y0, x1, y1, x2, y2, this.color);
      this.hTri1 = drawTriangle(hCanvas, x0, y0, x2, y2, x3, y3, this.color);
    }
  }

  return r;
}

// Circle: Shape
// dim: number, p0: Point, p1: Point, n "normal": Point (3-vector), resolution: number, color: [n, n, n, n]
function Circle(p0_, p1_, normal_) {
  var r = { "type": "circle", "dim": 2, "p0": p0_, "p1": p1_, "n": normal_, "resolution": 120 };
  if (typeof r.n === "undefined") r.n = P_("", 0, 0, 1); // Default: facing positive Z

  r.getName = function () { return this.p.name; }
  //r.getChildren = function() { return [this.p0, this.p1]; }
  r.initDraw = function (hCanvas, transform, width, height) {
    var ox = this.p0.x, oy = this.p0.y, oz = this.p0.z;
    var xdx = this.p1.x - ox, xdy = this.p1.y - oy, xdz = this.p1.z - oz;
    var ydx = this.n.y * xdz - this.n.z * xdy, ydy = this.n.z * xdx - this.n.x * xdz, ydz = this.n.x * xdy - this.n.y * xdx;
    var lxd = Math.sqrt(xdx * xdx + xdy * xdy + xdz * xdz); xdx /= lxd; xdy /= lxd; xdz /= lxd;
    var lyd = Math.sqrt(ydx * ydx + ydy * ydy + ydz * ydz); ydx /= lyd; ydy /= lyd; ydz /= lyd;
    var r = lxd;
    this.lines = [];
    this.tris = [];

    var n = this.resolution;
    for (var i = 0; i < n; i++) {
      var t0 = 2 * Math.PI * (i / n), t = 2 * Math.PI * ((i + 1) / n);
      var x0 = Math.cos(t0) * r, y0 = Math.sin(t0) * r, x = Math.cos(t) * r, y = Math.sin(t) * r;

      var segment = L_(
        P_("", ox + xdx * x0 + ydx * y0, oy + xdy * x0 + ydy * y0, oz + xdz * x0 + ydz * y0),
        P_("", ox + xdx * x + ydx * y, oy + xdy * x + ydy * y, oz + xdz * x + ydz * y)
      );
      this.lines.push(segment);

      if (this.color) {
        var fragment = Triangle(
          P_("", ox, oy, oz),
          P_("", ox + xdx * x0 + ydx * y0, oy + xdy * x0 + ydy * y0, oz + xdz * x0 + ydz * y0),
          P_("", ox + xdx * x + ydx * y, oy + xdy * x + ydy * y, oz + xdz * x + ydz * y)
        );
        fragment.color = this.color;
        this.tris.push(fragment);
      }
    }

    for (var line of this.lines) line.initDraw(hCanvas, transform, width, height);
    for (var tri of this.tris) tri.initDraw(hCanvas, transform, width, height);
  }

  return r;
}

// Axis: Shape
// dim: number, zero: Point, one: Point, lower: number, upper: number;
// thickness: number, color: [n, n, n, n], tag: Tag, n "normal": Point, nst "number stride": number, pst "primary tick stride": number, sst "secondary tick stride": number, number0: bool, noff "number offset": number, poff "primary tick offset": number, soff "secondary tick offset": number
function Axis(zero_, one_, lower_, upper_, tag_, n_) {
  var r = {
    "type": "axis", "dim": 1, "zero": zero_, "one": one_, "lower": lower_, "upper": upper_, "tag": tag_, "n": n_,
    "thickness": 1, "color": [0, 0, 0, 1.0], // "pthickness": 1, "sthickness": 0.5
    "number0": true
  };
  if (typeof r.n === "undefined") r.n = P_("", 0, 0, 1); // Default: facing positive Z

  r.getName = function () { return this.zero.name + (this.tag ? this.tag.text : this.one.name); };
  // Automatically decide ticking strides
  // [elen "estimated length (in pixels)": number]
  r.autoTick = function (elen) {
    this.ticks = true;
    var large = Math.pow(10, Math.floor(Math.log10(this.upper - this.lower)));
    if (large * 5 < this.upper) large *= 5;
    if (large * 2 < this.upper) large *= 2;
    this.large = large; this.nst = large / 2; this.pst = large / 2; this.sst = large / 10;
    this.noff = -large / 17; this.poff = large / 30; this.soff = large / 50;
  };
  r.initDraw = function (hCanvas, transform, width, height) {
    var upper = this.upper, lower = this.lower;
    var ox = this.zero.x, oy = this.zero.y, oz = this.zero.z;
    var dx = this.one.x - ox, dy = this.one.y - oy, dz = this.one.z - oz;
    this.lines = [];
    this.points = [];

    // TEMP CODE
    function divisible(a, b) { var rem = Math.abs(a) % b; return rem < 1e-8 || rem > (b - 1e-8); }

    // Axis line
    var axisLine = L_(P_("", ox + dx * lower, oy + dy * lower, oz + dz * lower), P_("", ox + dx * upper, oy + dy * upper, oz + dz * upper));
    axisLine.thickness = this.thickness;
    axisLine.color = this.color;
    this.lines.push(axisLine);

    // Ticks & numbering
    if (this.ticks) {
      var ydx = this.n.y * dz - this.n.z * dy, ydy = this.n.z * dx - this.n.x * dz, ydz = this.n.x * dy - this.n.y * dx; // Binormal
      var k = Math.sqrt(dx * dx + dy * dy + dz * dz) / Math.sqrt(ydx * ydx + ydy * ydy + ydz * ydz); ydx *= k; ydy *= k; ydz *= k; // Normalize

      var psRatio = Math.round(this.pst / this.sst), nsRatio = Math.round(this.nst / this.sst);
      for (var i = Math.ceil(this.lower / this.sst); i <= Math.floor(this.upper / this.sst); i++) if (this.number0 || Math.abs(i) > 1e-8) {
        var val = i * this.sst, x = ox + dx * val, y = oy + dy * val, z = oz + dz * val;
        if (divisible(i, nsRatio)) {
          // Numbering
          var tagPoint = P_(val.toString(), x + ydx * this.noff, y + ydy * this.noff, z + ydz * this.noff);
          tagPoint.size = 0;
          this.points.push(tagPoint);
        }
        if (divisible(i, psRatio)) {
          // Primary ticks
          var tickLine = L_(P_("", x, y, z), P_("", x + ydx * this.poff, y + ydy * this.poff, z + ydz * this.poff));
          tickLine.thickness = this.thickness;
          tickLine.color = this.color;
          this.lines.push(tickLine);
        } else {
          // Secondary ticks
          var tickLine = L_(P_("", x, y, z), P_("", x + ydx * this.soff, y + ydy * this.soff, z + ydz * this.soff));
          tickLine.thickness = this.thickness * 0.5;
          tickLine.color = this.color;
          this.lines.push(tickLine);
        }
      }
    }

    // Arrowhead
    this.arrow = A_(P_("", ox + dx * upper, oy + dy * upper, oz + dz * upper), P_("", dx, dy, dz));
    this.arrow.size = this.arrow.offset = this.thickness * 8.0;
    this.arrow.thickness = this.thickness;
    this.arrow.color = this.color;

    // Axis tag ("x", "y", "t", etc.)
    if (this.tag) {
      var tagPoint = P_(this.tag, ox + dx * upper, oy + dy * upper, oz + dz * upper);
      tagPoint.size = 0;
      this.points.push(tagPoint);
    }

    for (var line of this.lines) line.initDraw(hCanvas, transform, width, height);
    this.arrow.initDraw(hCanvas, transform, width, height);
    for (var point of this.points) point.initDraw(hCanvas, transform, width, height);
  };
  r.postTypesetDraw = function (hCanvas, transform, width, height) {
    for (var point of this.points) point.postTypesetDraw(hCanvas, transform, width, height);
  };

  return r;
}

// Axes2D: Shape
// dim: number, o: Point, x: Point, y: Point, xmin: number, xmax: number, ymin: number, ymax: number, axes: bool, axesThickness: number, axesColor: [n, n, n, n], grid: bool, gridThickness: number, gridColor: [n, n, n, n], xtag: Tag, ytag: Tag
function Axes2D(o_, x_, y_, xmin_, xmax_, ymin_, ymax_, grid_) {
  var r = {
    "type": "axes2d", "dim": 2, "o": o_, "x": Axis(o_, x_, xmin_, xmax_, T_("x", 4.5, 13)), "y": Axis(o_, y_, ymin_, ymax_, T_("y", 10.5, 15)),
    "axes": true, "axesThickness": 1, "axesColor": [0, 0, 0, 0.8],
    "grid": false, "gridThickness": 1, "gridColor": [128, 128, 128, 0.3]
  };
  if (typeof grid_ !== "undefined") r.grid = grid_;

  r.getName = function () { return (this.x.tag ? this.x.tag.text : this.x.one.name) + this.o.name + (this.y.tag ? this.y.tag.text : this.y.one.name); };
  r.autoTick = function (xelen, yelen) {
    this.x.autoTick(xelen);
    this.y.autoTick(yelen);
    this.y.noff *= -1; this.y.poff *= -1; this.y.soff *= -1;
    this.x.number0 = this.y.number0 = false; // Avoid displaying ticks on origin
  };
  r.initDraw = function (hCanvas, transform, width, height) {
    var xmin = this.x.lower, xmax = this.x.upper, ymin = this.y.lower, ymax = this.y.upper;
    var ox = this.o.x, oy = this.o.y, oz = this.o.z;
    var xdx = this.x.one.x - ox, xdy = this.x.one.y - oy, xdz = this.x.one.z - oz;
    var ydx = this.y.one.x - ox, ydy = this.y.one.y - oy, ydz = this.y.one.z - oz;
    this.lines = [];

    if (this.grid) {
      for (var i = Math.ceil(xmin); i <= Math.floor(xmax); i++) if (!this.axes || Math.abs(i) > 1e-8) {
        var vertical = L_(
          P_("", ox + xdx * i + ydx * ymin, oy + xdy * i + ydy * ymin, oz + xdz * i + ydz * ymin),
          P_("", ox + xdx * i + ydx * ymax, oy + xdy * i + ydy * ymax, oz + xdz * i + ydz * ymax)
        );
        vertical.thickness = this.gridThickness;
        vertical.color = this.gridColor;
        this.lines.push(vertical);
      }
      for (var i = Math.ceil(ymin); i <= Math.floor(ymax); i++) if (!this.axes || Math.abs(i) > 1e-8) {
        var horizontal = L_(
          P_("", ox + xdx * xmin + ydx * i, oy + xdy * xmin + ydy * i, oz + xdz * xmin + ydz * i),
          P_("", ox + xdx * xmax + ydx * i, oy + xdy * xmax + ydy * i, oz + xdz * xmax + ydz * i)
        );
        horizontal.thickness = this.gridThickness;
        horizontal.color = this.gridColor;
        this.lines.push(horizontal);
      }
    }

    for (var line of this.lines) line.initDraw(hCanvas, transform, width, height);

    if (this.axes) {
      this.x.initDraw(hCanvas, transform, width, height);
      this.y.initDraw(hCanvas, transform, width, height);
    }
  };
  r.postTypesetDraw = function (hCanvas, transform, width, height) {
    if (this.axes) {
      this.x.postTypesetDraw(hCanvas, transform, width, height);
      this.y.postTypesetDraw(hCanvas, transform, width, height);
    }
  };

  return r;
}

// Function2D: Shape
// name: string, dim: number, axes: Axes2D, func: function(x: number) -> number, resolution: number, thickness: number, color: [n, n, n, n]
function Function2D(name_, axes_, func_) {
  var r = { "type": "function2d", "dim": 2, "name": name_, "axes": axes_, "func": func_, "resolution": 200 };

  r.getName = function () { return this.name; }
  r.initDraw = function (hCanvas, transform, width, height) {
    var xmin = this.axes.x.lower, xmax = this.axes.x.upper, ymin = this.axes.y.lower, ymax = this.axes.y.upper;
    var ox = this.axes.o.x, oy = this.axes.o.y, oz = this.axes.o.z;
    var xdx = this.axes.x.one.x - ox, xdy = this.axes.x.one.y - oy, xdz = this.axes.x.one.z - oz;
    var ydx = this.axes.y.one.x - ox, ydy = this.axes.y.one.y - oy, ydz = this.axes.y.one.z - oz;
    this.lines = [];

    var n = this.resolution, x0, y0;
    for (var i = 0; i <= n; i++) {
      var x = (xmax - xmin) * (i / n) + xmin;
      var y = this.func(x);
      if (i > 0 && y0 >= ymin && y0 <= ymax && y >= ymin && y <= ymax) {
        var segment = L_(
          P_("", ox + xdx * x0 + ydx * y0, oy + xdy * x0 + ydy * y0, oz + xdz * x0 + ydz * y0),
          P_("", ox + xdx * x + ydx * y, oy + xdy * x + ydy * y, oz + xdz * x + ydz * y)
        );
        if (this.thickness) segment.thickness = this.thickness;
        if (this.color) segment.color = this.color;
        this.lines.push(segment);
      }
      x0 = x; y0 = y;
    }

    for (var line of this.lines) line.initDraw(hCanvas, transform, width, height);
  };

  return r;
}

// Parametric2D: Shape
// name: string, dim: number, axes: Axes2D, func: function(t: number) -> [n, n], range: [n, n], resolution: number, thickness: number, color: [n, n, n, n]
function Parametric2D(name_, axes_, func_, range_) {
  var r = { "type": "parametric2d", "dim": 2, "name": name_, "axes": axes_, "func": func_, "range": range_, "resolution": 200 };

  r.getName = function () { return this.name; }
  r.initDraw = function (hCanvas, transform, width, height) {
    var xmin = this.axes.x.lower, xmax = this.axes.x.upper, ymin = this.axes.y.lower, ymax = this.axes.y.upper, tmin = this.range[0], tmax = this.range[1];
    var ox = this.axes.o.x, oy = this.axes.o.y, oz = this.axes.o.z;
    var xdx = this.axes.x.one.x - ox, xdy = this.axes.x.one.y - oy, xdz = this.axes.x.one.z - oz;
    var ydx = this.axes.y.one.x - ox, ydy = this.axes.y.one.y - oy, ydz = this.axes.y.one.z - oz;
    this.lines = [];

    var n = this.resolution, x0, y0;
    for (var i = 0; i <= n; i++) {
      var t = (tmax - tmin) * (i / n) + tmin, xy = this.func(t);
      var x = xy[0], y = xy[1];
      if (i > 0 && x0 >= xmin && x0 <= xmax && x >= xmin && x <= xmax && y0 >= ymin && y0 <= ymax && y >= ymin && y <= ymax) {
        var segment = L_(
          P_("", ox + xdx * x0 + ydx * y0, oy + xdy * x0 + ydy * y0, oz + xdz * x0 + ydz * y0),
          P_("", ox + xdx * x + ydx * y, oy + xdy * x + ydy * y, oz + xdz * x + ydz * y)
        );
        if (this.thickness) segment.thickness = this.thickness;
        if (this.color) segment.color = this.color;
        this.lines.push(segment);
      }
      x0 = x; y0 = y;
    }

    for (var line of this.lines) line.initDraw(hCanvas, transform, width, height);
  };

  return r;
}

// Triangular pyramid: Shape
// dim: number, p0~p3: Point, l0~l5: Line, (edgeThickness: number, faceColor: [n, n, n, n])
function TriPyramid(p0_, p1_, p2_, p3_) {
  var r = { "type": "tripyramid", "dim": 3, "p0": p0_, "p1": p1_, "p2": p2_, "p3": p3_ };
  r.l0 = L_(r.p1, r.p2); r.l1 = L_(r.p2, r.p3); r.l2 = L_(r.p3, r.p1); r.l3 = L_(r.p0, r.p1); r.l4 = L_(r.p0, r.p2); r.l5 = L_(r.p0, r.p3);
  r.getName = function () { return this.p0.name + "-" + this.p1.name + this.p2.name + this.p3.name; }
  r.getChildren = function () { return [this.p0, this.p1, this.p2, this.p3, this.l0, this.l1, this.l2, this.l3, this.l4, this.l5]; };
  return r;
}

// Quadrangular pyramid: Shape
// dim: number, p0~p4: Point, l0~l7: Line, (edgeThickness: number, faceColor: [n, n, n, n])
function QuadPyramid(p0_, p1_, p2_, p3_, p4_) {
  var r = { "type": "quadpyramid", "dim": 3, "p0": p0_, "p1": p1_, "p2": p2_, "p3": p3_, "p4": p4_ };
  r.l0 = L_(r.p1, r.p2); r.l1 = L_(r.p2, r.p3); r.l2 = L_(r.p3, r.p4); r.l3 = L_(r.p4, r.p1); r.l4 = L_(r.p0, r.p1); r.l5 = L_(r.p0, r.p2); r.l6 = L_(r.p0, r.p3); r.l7 = L_(r.p0, r.p4);
  r.getName = function () { return this.p0.name + "-" + this.p1.name + this.p2.name + this.p3.name + this.p4.name; }
  r.getChildren = function () { return [this.p0, this.p1, this.p2, this.p3, this.p4, this.l0, this.l1, this.l2, this.l3, this.l4, this.l5, this.l6, this.l7]; };
  return r;
}

// Cube: Shape
// dim: number, p0~p7: Point, l0~l11: Line, (edgeThickness: number, faceColor: [n, n, n, n])
function Cube(p0_, p1_, p2_, p3_, p4_, p5_, p6_, p7_) {
  var r = { "type": "cube", "dim": 3, "p0": p0_, "p1": p1_, "p2": p2_, "p3": p3_, "p4": p4_, "p5": p5_, "p6": p6_, "p7": p7_ };
  r.l0 = L_(r.p0, r.p1); r.l1 = L_(r.p1, r.p2); r.l2 = L_(r.p2, r.p3); r.l3 = L_(r.p3, r.p0); r.l4 = L_(r.p4, r.p5); r.l5 = L_(r.p5, r.p6); r.l6 = L_(r.p6, r.p7); r.l7 = L_(r.p7, r.p4); r.l8 = L_(r.p0, r.p4), r.l9 = L_(r.p1, r.p5), r.l10 = L_(r.p2, r.p6), r.l11 = L_(r.p3, r.p7);
  r.getName = function () { return this.p0.name + this.p1.name + this.p2.name + this.p3.name + "-" + this.p4.name + this.p5.name + this.p6.name + this.p7.name; }
  r.getChildren = function () { return [this.p0, this.p1, this.p2, this.p3, this.p4, this.p5, this.p6, this.p7, this.l0, this.l1, this.l2, this.l3, this.l4, this.l5, this.l6, this.l7, this.l8, this.l9, this.l10, this.l11]; };
  return r;
}

// Figure
// elements: [...], aspect: number, transform: Matrix(4, 4)
function Figure(elements_, aspect_, transform_) {
  // Using ES5 feature (`Set`) for duplicate removal
  var r = {
    "elements": [new Set(), new Set(), new Set(), new Set()],
    "aspect": aspect_,
    "transform": transform_
  };

  r.addElements = function (elements) {
    for (var x of elements) {
      this.elements[x.dim].add(x);
      var children = (x.getChildren ? x.getChildren() : []);
      for (var y of children) this.elements[y.dim].add(y);
    }
  }

  r.initDraw = function (el, noTypeset) {
    if (noTypeset) MathJaxDisabled = true; else MathJaxDisabled = false;
    var height = 320 / this.aspect, width = 320;
    this.hCanvas = initCanvas(el, width, height);
    for (var i = 3; i >= 0; i--) for (var x of this.elements[i]) {
      if (x.initDraw) x.initDraw(this.hCanvas, this.transform, width, height);
    }
    if (!noTypeset) MathJax.typeset();
    for (var i = 3; i >= 0; i--) for (var x of this.elements[i]) {
      if (x.postTypesetDraw) x.postTypesetDraw(this.hCanvas, this.transform, width, height);
    }
  }
  /*
  r.updateDraw = function() {
    var height = 500 / this.aspect, width = 500;
    for (var i = 3; i >= 0; i--) for (var x of this.elements[i]) {
      if (x.updateDraw) x.updateDraw(this.hCanvas, this.transform, width, height);
    }
    MathJax.typeset();
    for (var i = 3; i >= 0; i--) for (var x of this.elements[i]) {
      if (x.postTypesetDraw) x.postTypesetDraw(this.hCanvas, this.transform, width, height);
    }
  }
  */
  r.addElements(elements_);
  return r;
}

function Figure2D(elements, xmin, xmax, ymin, ymax) {
  var aspect = (xmax - xmin) / (ymax - ymin);
  var r = Figure(elements, aspect, Orthogonal(xmin, xmax, ymax, ymin, -1, 1), false);
  /*
  r.adjustViewport = function() {}
  */
  return r;
}

function Figure3D(elements, fov, aspect, zNear, zFar) {
  return Figure(elements, aspect, Perspective(fov, aspect, zNear, zFar), false);
}
