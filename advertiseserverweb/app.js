const express = require('express')
const fs = require('fs')
const app = express()
const port = 4000
let currentactive = 0
let current_emo = {}
app.use(express.static('public'))

app.listen(port, () => {
    console.log(`listenting to the port ${port}`)
})

app.get('/live', (req,res) => {
    const data = fs.readFileSync(`../storecam/data.json`, 'utf-8')
    res.send(data)
})

app.get('/liveads',(req,res) => {
     currentactive = req.query.isactive
     current_emo = req.query.emos 
     res.send('updated')
    //  console.log(current_emo)
})
app.get('/ads',(req,res)=> {
    // console.log(currentactive)
    if(currentactive === 0) {
        res.send(currentactive+'')
    }
    else {
        res.send(currentactive+'')
    }
})
// app.get('/livestream',(req,res)=>{
    // res.sendFile(`${__dirname}/../storecam/images.png`)
// })