// firebase information

let firebaseConfig = [
  {
    apiKey: "",
    authDomain: "",
    databaseURL: "",
    projectId: "",
    storageBucket: "",
    messagingSenderId: "",
    appId: ""
  }
];

module.exports = {
  getConfig: () => firebaseConfig[0]
}
