const express = require('express')
const users = require('./services/users');
//const Ajv = require('ajv').default

const app = express()
const port = 3000
//const jsonSchemaPayment = require('./schemas/jsonSchemaPayment.json')

/*
    Implementation of performing a transaction to a users account, done in 3 steps:
      1. The users request is verified against a schema making sure the request is correct
      2. The transaction is carried out and the user is debited the transaction amount
      3. The server returns that the transaction has been carried out.
    
    POSSIBLE TO DO: add verification to make sure that the one making the transaction is a 
    legitimate vending machine.
*/
app.post('/payment', (req, res) => {
  res.send('Hello World!')
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})


/* For vending machine verification, one possible solution would be to make the vending 
machine GUI make a BASIC/or other login request to obtain token for later transactions, 
this way the transactions will not be delayed by authorization constraints.
*/