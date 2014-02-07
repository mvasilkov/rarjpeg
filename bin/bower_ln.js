#!/usr/bin/env node
var inp = '', is = process.stdin
is.setEncoding('utf8')
is.on('data', function (s) { inp += s })
is.on('end', function () {
    var obj = JSON.parse(inp), p
    for (p in obj) console.log(obj[p])
})
is.resume()
