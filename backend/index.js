const express = require('express')
const users = require('./services/users');
const bodyParser = require('body-parser')
const Ajv = require('ajv').default

const app = express()
const port = 3000
const ajv = new Ajv()
const jsonSchemaPayment = require('./schemas/jsonSchemaPayment.json')


app.use(express.json())

/*
    Implementation of performing a transaction to a users account, done in 3 steps:
      1. The users request is verified against a schema making sure the request is correct
      2. The transaction is carried out and the user is debited the transaction amount
      3. The server returns that the transaction has been carried out.
    
    POSSIBLE TO DO: add verification to make sure that the one making the transaction is a 
    legitimate vending machine.
*/
app.post('/payment', (req, res) => {
  console.log(req.body)

  // request gets validated against schema
  let validate = ajv.compile(jsonSchemaPayment)
  let valid = validate(req.body)
  
  if(valid == false) {
    res.status(400)
    res.send(validate.errors.map(err => err.message))
    return
  }

  let currUser = users.getUser(req.body.username,req.body.number)
  console.log(currUser)

  // check that user is good
  if(currUser.length == 0) {
    return res.sendStatus(400)
  }

  // now debit user with the set amount - done by editing user account
  creditedUser = currUser[0]
  // //console.log(creditedUser)
  // //console.log(parseFloat(req.body.amount))
  creditedUser.amount += parseFloat(req.body.amount)

  //console.log(users.changeUser(debitedUser.id,debitedUser))

  //console.log(debitedUser)
  console.log(users.getAll())
  res.send("gaming")
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})


/* For vending machine verification, one possible solution would be to make the vending 
machine GUI make a BASIC/or other login request to obtain token for later transactions, 
this way the transactions will not be delayed by authorization constraints.
*/