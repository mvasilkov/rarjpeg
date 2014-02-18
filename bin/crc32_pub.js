#!/usr/bin/env node
var assert = require('assert'),
    fs = require('fs'),
    crc32 = require('sse4_crc32'),
    inp = '', is = process.stdin
is.setEncoding('utf8')
is.on('data', function (s) { inp += s })
is.on('end', function () {
    var files = inp.split('\n'), buf, res = {}
    assert(files.pop() === '')
    for (var f in files) {
        buf = fs.readFileSync(files[f])
        res[files[f]] = pad(crc32.calculate(buf).toString(16), 8)
    }
    console.log('%j', res)
})
is.resume()
function pad(str, len) {
    if (str.length < len)
        return ('00000000' + str).slice(-len)
    return str
}
