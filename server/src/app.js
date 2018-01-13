var express = require('express')

var app = express()

app.get('/test', function(req,res){
  res.send('hej')
})

app.get('/profile/:id', function(req,res){
  res.send('hej ' + req.params.id)
})

app.listen(3000)
