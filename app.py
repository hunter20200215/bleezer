import base64
import pickle

from flask import Flask
from flask import jsonify
from flask import request


app = Flask(__name__)


@app.route("/api/cookie/update", methods=['GET', 'POST'])
def file_write_cookie():
	data = request.get_json()
	print (data)
	cookie_file = f"%s_cookie.pkl" %(data['user'])
	with open(cookie_file, 'wb') as ff:
		pickle.dump( data['cookie'], ff)
	return "success"



@app.route("/api/user/random")
def get_random_user():
    username = "definetrue215@protonmail.com"
    password = "password215"
    playlist = "enjoy"
    time_to_play_for = 60
    shuffle = False
    cookie_file = f"%s_cookie.pkl" % (username)
    print(cookie_file)
    try:
    	with open(cookie_file, 'rb') as ff:
    		cookies = pickle.load(ff)
    except:
    	cookies = {"error":1}
    
    # encoded_cookie_data = base64.b64encode(data)

    return jsonify({"username":username, "password":password, "cookie":cookies, "playlist":playlist, "time_to_play_for": time_to_play_for, "shuffle": shuffle})

#calling url
@app.route("/test/user/random")
def test_random_user():

	url = 'http://127.0.0.1:5000/api/user/random'
	data = ""
	import requests
	response = requests.get(url, data=data)
	
	return response.text

app.run()	