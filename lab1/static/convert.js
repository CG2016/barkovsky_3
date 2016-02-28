"use strict";


var x_d65 = 95.047;
var y_d65 = 100.000;
var z_d65 = 108.883;

function setColorBlock(r, g, b) {
    var color = sprintf('rgb(%d, %d, %d)', r, g, b);
    $('#color-block').css('background-color', color);
}

function setLabValues(l, a, b) {
    $('#lab-l').val(l);
    $('#lab-l-value').text(sprintf('%.2f', l));
    $('#lab-a').val(a);
    $('#lab-a-value').text(sprintf('%.2f', a));
    $('#lab-b').val(b);
    $('#lab-b-value').text(sprintf('%.2f', b));
}

function setCmyValues(c, m, y) {
    $('#cmy-c').val(c);
    $('#cmy-c-value').text(sprintf('%.2f', c));
    $('#cmy-m').val(m);
    $('#cmy-m-value').text(sprintf('%.2f', m));
    $('#cmy-y').val(y);
    $('#cmy-y-value').text(sprintf('%.2f', y));
}

function setHsvValues(h, s, v) {
    $('#hsv-h').val(h);
    $('#hsv-h-value').text(sprintf('%.2f', h));
    $('#hsv-s').val(s);
    $('#hsv-s-value').text(sprintf('%.2f', s));
    $('#hsv-v').val(v);
    $('#hsv-v-value').text(sprintf('%.2f', v));
}

function labToXyz(l, a, b) {
    var delta = 6 / 29;
    var finv = function(t) {
        if (t > delta)
            return t * t * t;
        else
            return 3 * delta * delta * (t - 4 / 29);
    }

    var x = x_d65 * finv((l + 16) / 116 + a / 500) / 100;
    var y = y_d65 * finv((l + 16) / 116) / 100;
    var z = z_d65 * finv((l + 16) / 116 - b / 200) / 100;
    return {
        x: x,
        y: y,
        z: z
    }
}

function xyzToLab(x, y, z) {
    var f = function(t) {
        if (t > Math.pow(6 / 29, 3))
            return Math.pow(t, 1 / 3);
        else
            return 1 / 3 * Math.pow(29 / 6, 2) * t + 4 / 29
    }

    return {
        l: 116 * f(y / y_d65) - 16,
        a: 500 * (f(x / x_d65) - f(y / y_d65)),
        b: 200 * (f(y / y_d65) - f(z / z_d65))
    }
}

function xyzToSrgb(x, y, z) {
    var r_lin = 3.2406 * x - 1.5372 * y - 0.4986 * z;
    var g_lin = -0.9689 * x + 1.8758 * y + 0.0415 * z;
    var b_lin = 0.0557 * x - 0.2040 * y + 1.0570 * z;

    var a = 0.055;
    var linToLog = function(lin) {
        if (lin <= 0.0031308)
            return 12.92 * lin;
        else
            return (1 + a) * Math.pow(lin, 1 / 2.4) - a;
    }

    return {
        r: Math.floor(linToLog(r_lin) * 255),
        g: Math.floor(linToLog(g_lin) * 255),
        b: Math.floor(linToLog(b_lin) * 255)
    }
}

function srgbToXyz(r, g, b) {
    var a = 0.055;
    var toLin = function(c) {
        if (c <= 0.04045)
            return c / 12.92;
        else
            return Math.pow((c + a) / (1 + a), 2.4)
    }

    var r_lin = toLin(r / 255);
    var g_lin = toLin(g / 255);
    var b_lin = toLin(b / 255);

    return {
        x: (0.4124 * r_lin + 0.3576 * g_lin + 0.1805 * b_lin) * 100,
        y: (0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin) * 100,
        z: (0.0193 * r_lin + 0.1192 * g_lin + 0.9505 * b_lin) * 100
    }
}

function rgbToCmy(r, g, b) {
    return {
        c: (1 - r / 255) * 100,
        m: (1 - g / 255) * 100,
        y: (1 - b / 255) * 100
    }
}

function cmyToRgb(c, m, y) {
    return {
        r: (1 - c / 100) * 255,
        g: (1 - m / 100) * 255,
        b: (1 - y / 100) * 255,
    }
}

function rgbToHsv(r, g, b) {
    r /= 255;
    g /= 255;
    b /= 255;

    var cmax = Math.max(r, g, b);
    var cmin = Math.min(r, g, b);
    var delta = cmax - cmin;

    var h;
    if (delta == 0)
        h = 0;
    else if (cmax == r)
        h = 60 * (((g - b) / delta) % 6);
    else if (cmax == g)
        h = 60 * ((b - r) / delta + 2);
    else
        h = 60 * ((r - g) / delta + 4);
    h = (h + 360) % 360;

    var s;
    if (cmax == 0)
        s = 0;
    else
        s = delta / cmax * 100;

    var v = cmax * 100;

    return {
        h: h,
        s: s,
        v: v
    }
}

function renderLab() {
    var l = parseFloat($('#lab-l').val());
    var a = parseFloat($('#lab-a').val());
    var b = parseFloat($('#lab-b').val());
    setLabValues(l, a, b);

    var xyz = labToXyz(l, a, b);
    var rgb = xyzToSrgb(xyz.x, xyz.y, xyz.z);
    var cmy = rgbToCmy(rgb.r, rgb.g, rgb.b);
    var hsv = rgbToHsv(rgb.r, rgb.g, rgb.b);

    setColorBlock(rgb.r, rgb.g, rgb.b);
    setCmyValues(cmy.c, cmy.m, cmy.y);
    setHsvValues(hsv.h, hsv.s, hsv.v);
}

function renderCmy() {
    var c = parseFloat($('#cmy-c').val());
    var m = parseFloat($('#cmy-m').val());
    var y = parseFloat($('#cmy-y').val());
    setCmyValues(c, m, y);

    var rgb = cmyToRgb(c, m, y);
    var hsv = rgbToHsv(rgb.r, rgb.g, rgb.b);
    var xyz = srgbToXyz(rgb.r, rgb.g, rgb.b);
    var lab = xyzToLab(xyz.x, xyz.y, xyz.z);

    setColorBlock(rgb.r, rgb.g, rgb.b);
    setHsvValues(hsv.h, hsv.s, hsv.v);
    setLabValues(lab.l, lab.a, lab.b);
}


$(document).ready(function () {
    setCmyValues(7, 87, 96);
    renderCmy();

    $('#lab-l').on('input', renderLab);
    $('#lab-a').on('input', renderLab);
    $('#lab-b').on('input', renderLab);

    $('#cmy-c').on('input', renderCmy);
    $('#cmy-m').on('input', renderCmy);
    $('#cmy-y').on('input', renderCmy);
});
