from requests_oauthlib import OAuth2Session
from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask.json import jsonify
import logging
import os
import pprint
import sys

app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
app.secret_key=os.urandom(24)

client_id = os.environ['GITHUB_CLIENT_ID']
client_secret = os.environ['GITHUB_CLIENT_SECRET']
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'
redirect_uri = 'https://polar-coast-87574.herokuapp.com/login/authorized'

@app.context_processor
def inject_logged_in():
	return dict(logged_in=(is_logged_in()))

def is_logged_in():
	return ('oauth_token' in session)

@app.route('/')
def render_home():
	return render_template('home.html')

@app.route('/login')
def login():
	session.clear()
	github = OAuth2Session(client_id, redirect_uri=redirect_uri)
	(authorization_url,state) = github.authorization_url(authorization_base_url)
	print authorization_url
	print state
	session['oauth_state'] = state
	return redirect(authorization_url)


@app.route('/login/authorized', methods=["GET"])
def authorized():
	try:
		github = OAuth2Session(client_id, state=session['oauth_state'])
		token = github.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
		print token
		session['oauth_token'] = token
		return redirect(url_for('.profile'))
	except KeyError as error:
		session.clear()
		print error
		return redirect(url_for('render_home'))


@app.route('/profile', methods=["GET"])
def profile():
	github = OAuth2Session(client_id, token=session['oauth_token'])
	json_data = jsonify(github.get('https://api.github.com/user').json())
	return render_template('profile.html',profile_data=json_data)

@app.route('/logout')
def logout():
	session.clear()
	flash('You were logged out!')
	return redirect(url_for('render_home'))

@app.route('/conversions')
def render_conversions_home():
	return render_template('conversion_home.html')

@app.route('/tutorials')
def render_tutorials_home():
	return render_template('tutorial_home.html')

@app.route('/jquery-animate')
def render_tutorials_animate():
	return render_template('animate_key.html')

@app.route('/jquery-slide')
def render_tutorials_slide():
	return render_template('slide.html')

@app.route('/ctof')
def render_ctof():
	return render_template('ctof.html')

@app.route('/ftoc')
def render_ftoc():
	return render_template('ftoc.html')

@app.route('/mtokm')
def render_mtokm():
	return render_template('mtokm.html')

@app.route('/ctof_result')
def render_ctof_result():
	try:
		ctemp_result = float(request.args['cTemp'])
		ftemp_result = ctof(ctemp_result)
		return render_template('ctof_result.html',cTemp=ctemp_result, fTemp=ftemp_result)
	except ValueError:
		error_message = "Sorry, could not convert..."
		flash(error_message)
		return redirect(url_for('render_home'))

@app.route('/ftoc_result')
def render_ftoc_result():
	try:
		ftemp_result = float(request.args['fTemp'])
		ctemp_result = ftoc(ftemp_result)
		return render_template('ftoc_result.html',fTemp=ftemp_result, cTemp=ctemp_result)
	except ValueError:
		error_message = "Sorry, could not convert..."
		flash(error_message)
		return redirect(url_for('render_home'))

@app.route('/mtokm_result')
def render_mtokm_result():
	try:
		miles = float(request.args['miles'])
		kilometers = mtokm(miles)
		return render_template('mtokm_result.html',miles=miles, kilometers=kilometers)
	except ValueError:
		error_message = "Sorry, could not convert..."
		flash(error_message)
		return redirect(url_for('render_home'))

def ctof(ctemp):
	return (ctemp * (9.0/5.0)) + 32.0

def ftoc(ftemp):
	return (ftemp-32.0)*(5.0/9.0)

def mtokm(miles):
	return (miles * 1.60934)

if __name__ == "__main__":
	app.run(debug=True)
