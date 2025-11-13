# artsbook-backend
A Firebase service account key is needed for this code to work - can be done with Firebase account or I can send the json.  

To create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate
```

To install Flask, Flask-CORS, requests, firebase-admin
```
pip install -r requirements.txt
```

To run: 
```
export FLASK_APP=main.py  
python -m flask run
```

To open, go to:
```
http://127.0.0.1:5000/
```

The URL routing in the code will indicate where the output from API calls and reading from the database can be found. To show that we can write to the database, we can use the Google Developer Console (inspect -> console) and paste:
```
fetch("http://127.0.0.1:5000/api/reviews", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    username: "test_user",
    content: "test review!"
  })
})
  .then(res => res.json())
  .then(console.log)
```
(can replace username and content with different strings)
After hitting enter, we can see an id and confirmation message. When reading from the database again, the newly written data will be visible.
