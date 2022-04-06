const chai = require('chai')
const expect = require('chai').expect
chai.use(require('chai-http'))
const api = 'https://c18437596-fyp-api.herokuapp.com/'
const { it } = require('mocha')

describe('Testing the Transaction API', async function() {
    
    let JWT = null

    describe('Testing the login endpoint (stations/login)', function() {

        it("Should return 200 on logging in with correct credentials", async function() {
            await chai.request(api)
            .get('stations/login')
            .auth('b8cd3d55-c3bc-4f19-b3f9-3d3f92d192d4','$2a$12$LQf4l7AItghSghQjZVK6DOuZoW0nFcmYhHLS2gNxz45At4str6KIi')
            .then(response => {
                JWT = response.body.token
                expect(response).to.have.property('status')
                expect(response.status).to.equal(200)
                expect(response.body).to.have.property('token')
            })
        })

        it("Should return 401 on logging in with wrong id", async function() {
            await chai.request(api)
            .get('stations/login')
            .auth('wrong id', '$2a$12$LQf4l7AItghSghQjZVK6DOuZoW0nFcmYhHLS2gNxz45At4str6KIi')
            .then(response => {
                expect(response).to.have.property('status')
                expect(response.status).to.equal(401)
            })
        })

        it("Should return 401 on logging in with wrong password", async function() {
            await chai.request(api)
            .get('stations/login')
            .auth('b8cd3d55-c3bc-4f19-b3f9-3d3f92d192d4', 'wrongpw')
            .then(response => {
                expect(response).to.have.property('status')
                expect(response.status).to.equal(401)
            })
        })
        
    }) 
    
    describe('Testing the transaction endpoint (/payment)', function() {
        it("Should return 200 on everything OK", async function() {
            let contents = {
                username: 'John Smith',
                number: '0851234567',
                amount: 0.25
            }
            contents = JSON.stringify(contents)
            await chai.request(api)
            .post('payment')
            .set('Authorization', 'Bearer ' + JWT)
            .set('Content-Type', 'application/json')
            .send(contents)
            .then(response =>{
                expect(response).to.have.property('status')
                expect(response.status).to.equal(200)
                expect(response.text).to.be.equal('User has been credited 0.25')
            })
        })

        it("Should return 401 with missing JWT", async function() {
            let contents = {
                username: 'John Smith',
                number: '0851234567',
                amount: 0.25
            }
            contents = JSON.stringify(contents)
            await chai.request(api)
            .post('payment')
            .send(contents)
            .then(response =>{
                expect(response).to.have.property('status')
                expect(response.status).to.equal(401)
            })
        })

        it("Should return 400 with wrong username", async function() {
            let contents = {
                username: 'wrong user',
                number: '0851234567',
                amount: 0.25
            }
            contents = JSON.stringify(contents)
            await chai.request(api)
            .post('payment')
            .set('Authorization', 'Bearer ' + JWT)
            .set('Content-Type', 'application/json')
            .send(contents)
            .then(response =>{
                expect(response).to.have.property('status')
                expect(response.status).to.equal(400)
            })
        })

        it("Should return 400 with wrong phone number", async function() {
            let contents = {
                username: 'John Smith',
                number: '0851234568',
                amount: 0.25
            }
            contents = JSON.stringify(contents)
            await chai.request(api)
            .post('payment')
            .set('Authorization', 'Bearer ' + JWT)
            .set('Content-Type', 'application/json')
            .send(contents)
            .then(response =>{
                expect(response).to.have.property('status')
                expect(response.status).to.equal(400)
            })
        })

        it("Should return 400 with missing username", async function() {
            let contents = {
                number: '0851234567',
                amount: 0.25
            }
            contents = JSON.stringify(contents)
            await chai.request(api)
            .post('payment')
            .set('Authorization', 'Bearer ' + JWT)
            .set('Content-Type', 'application/json')
            .send(contents)
            .then(response =>{
                expect(response).to.have.property('status')
                expect(response.status).to.equal(400)
                expect(response.text).to.be.equal('["must have required property \'username\'"]')
            })
        })

        it("Should return 400 with missing phone number", async function() {
            let contents = {
                username: 'John Smith',
                amount: 0.25
            }
            contents = JSON.stringify(contents)
            await chai.request(api)
            .post('payment')
            .set('Authorization', 'Bearer ' + JWT)
            .set('Content-Type', 'application/json')
            .send(contents)
            .then(response =>{
                expect(response).to.have.property('status')
                expect(response.status).to.equal(400)
                expect(response.text).to.be.equal('["must have required property \'number\'"]')
            })
        })

        it("Should return 400 with missing payment amount", async function() {
            let contents = {
                username: 'John Smith',
                number: '0851234567'
            }
            contents = JSON.stringify(contents)
            await chai.request(api)
            .post('payment')
            .set('Authorization', 'Bearer ' + JWT)
            .set('Content-Type', 'application/json')
            .send(contents)
            .then(response =>{
                expect(response).to.have.property('status')
                expect(response.status).to.equal(400)
                expect(response.text).to.be.equal('["must have required property \'amount\'"]')
            })
        })

        it("Should return 400 - too FEW characters in number", async function() {
            let contents = {
                username: 'John Smith',
                number: '085',
                amount: 0.25
            }
            contents = JSON.stringify(contents)
            await chai.request(api)
            .post('payment')
            .set('Authorization', 'Bearer ' + JWT)
            .set('Content-Type', 'application/json')
            .send(contents)
            .then(response =>{
                expect(response).to.have.property('status')
                expect(response.status).to.equal(400)
                expect(response.text).to.be.equal('["must NOT have fewer than 10 characters"]')
            })
        })

        it("Should return 400 - too MANY characters in number", async function() {
            let contents = {
                username: 'John Smith',
                number: '08512345678',
                amount: 0.25
            }
            contents = JSON.stringify(contents)
            await chai.request(api)
            .post('payment')
            .set('Authorization', 'Bearer ' + JWT)
            .set('Content-Type', 'application/json')
            .send(contents)
            .then(response =>{
                expect(response).to.have.property('status')
                expect(response.status).to.equal(400)
                expect(response.text).to.be.equal('["must NOT have more than 10 characters"]')
            })
        })
    })
})