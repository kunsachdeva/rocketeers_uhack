const express = require('express')
const fs = require('fs')
const app = express()
const port = 4000
let currentactive = 0
let current_emo = {}
let genders = []
let Ages = []
var oxford = require('project-oxford'),
client = new oxford.Client('7fb073s72bh72663y5ddh129m12e598d')
app.use(express.static('public'))

app.listen(port, () => {
    console.log(`listenting to the port ${port}`)
})

app.get('/live', (req,res) => {
    const data = fs.readFileSync(`../storecam/data.json`, 'utf-8')
    client.face.detect({
        path: 'images.jpg',
        analyzesAge: true,
        analyzesGender: true
    }).then(function (response) {
        Ages = response[0].attributes.age
        genders = response[0].attributes.gender
        data['Ages'] = Ages
        data['Genders'] = genders
    });
    res.send(data)
})

app.get('/liveads',(req,res) => {
     currentactive = req.query.isactive
     current_emo = req.query.emos 
     res.send('updated')
     console.log(current_emo)
})
app.get('/ads',(req,res)=> {
    // console.log(currentactive)
    res.send(currentactive)
})
// app.get('/livestream',(req,res)=>{
    // res.sendFile(`${__dirname}/../storecam/images.png`)
// })