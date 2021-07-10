import pyrebase

config = {
  'apiKey': "AIzaSyCogzrt_1Xz2fHHomCWzyMk6qjmM7SJyWM",
  "authDomain": "my-demo-test-68c4d.firebaseapp.com",
  'databaseURL': "https://my-demo-test-68c4d.firebaseio.com",
  'projectId': "my-demo-test-68c4d",
  'storageBucket': "my-demo-test-68c4d.appspot.com",
  'messagingSenderId': "317808783210",
  'appId': "1:317808783210:web:6d38aed44d57139ae97f13",
  'measurementId': "G-XCCNX4CHDD"
};

firebase = pyrebase.initialize_app(config)

firebase_auth= firebase.auth()
firebase_db = firebase.database()