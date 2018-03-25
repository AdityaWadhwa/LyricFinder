from flask import Flask, request, render_template, redirect, url_for, jsonify
import json
import requests
from credentials import creds

app = Flask(__name__)

url_search = "http://api.musixmatch.com/ws/1.1/track.search"
search_params = {
    	"apikey":creds['MUSIX_API_KEY'],
    	"q_artist":"",
    	"q_track":"",
    	"page_size":1,
    	"page":1,
    	"s_track_rating":"desc"
		}
url_lyric = "http://api.musixmatch.com/ws/1.1/track.lyrics.get"
lyric_params = {
    	"apikey":creds['MUSIX_API_KEY'],
    	"track_id":0
		}




@app.route('/')
def home():
	return render_template("index.html")


@app.route('/tasks/<int:id>')
def tasks(id):
	return "Task id: {}".format(id)


@app.route('/bio')
def get_bio():
	name = request.args.get("name")
	age = request.args.get("age")
	d = date.today()
	data = [[1,2,3],
			[4,5,6],
			[7,8,9]]
	return render_template("bio.html", name=name, age=age, date=d, 
							data=data)


@app.route('/find', methods=['GET', 'POST'])
def finder():
	if request.method == 'GET':
		return render_template("find.html")

	elif request.method == 'POST':
		title = request.form.get("title")
		artist = request.form.get("artist")

		search_params['q_artist']=artist
		search_params['q_track']=title

		r = requests.get(url=url_search,params=search_params)
		data = r.json()
		id = data['message']['body']['track_list'][0]['track']['track_id']
		
		lyric_params['track_id']=id

		r = requests.get(url=url_lyric,params=lyric_params)
		data = r.json()
		lyrics = data['message']['body']['lyrics']['lyrics_body']
		lyrics = lyrics.replace('\n', '<br>')
		
		return lyrics,200




if __name__ == "__main__":
	app.run(port=8000)