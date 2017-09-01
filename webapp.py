from flask import Flask, session, render_template, request, redirect, url_for, flash
#from flask_oauthlib.client import OAuth
import os
import pprint
import sys

app = Flask(__name__)
app.secret_key='w98fw9ef8hwe98fhwef'
"""
session.clear()

env_vars = ['GITHUB_CLIENT_ID','GITHUB_CLIENT_SECRET','APP_SECRET_KEY']

oauth = OAuth(app)
github = oauth.remote_app('github',
    consumer_key=os.environ['GITHUB_CLIENT_ID'],
    consumer_secret=os.environ['GITHUB_CLIENT_SECRET'],
    request_token_params={'scope': 'read:org'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)

def is_localhost():
	root_url = request.url_root
	developer_url = 'http://127.0.0.1:5000/'
	return root_url == developer_url

"""



@app.route('/')
def render_home():
	return render_template('home.html')

"""
@app.route('/login')
def login():
	if is_localhost():
		return github.authorize(callback=url_for('authorized',_external=True))

	return github.authorize(callback=url_for('authorized',_external=True,_scheme='https'))

@app.route('/login/authorized')
def login_authorized():
	resp = github.authorized_response()

	if resp is None:
		session.clear()
		login_error_message = 'Access denied: reason=%s error=%s full=%s' % (
            request.args['error'],
            request.args['error_description'],
            pprint.pformat(request.args)
        )        
        flash(login_error_message, 'error')
		return redirect(url_for('/'))

	try:
		session['github_token'] = (resp['oauth_token'],
									resp['oauth_token_secret'])
		session['twitter_user'] = resp['screen_name']
		flash('You were loggined in as %s' % resp['screen_name'])

@app.route('/logout')
def logout():
	session.clear()
	flash('You were logged out!')
	return redirect(url_for('/'))
"""
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
