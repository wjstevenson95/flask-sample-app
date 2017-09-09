from flask import Flask, session, render_template, request
from flask import redirect, url_for, flash, Markup, jsonify
from flask_oauthlib.client import OAuth, OAuthException
import logging
import os
import pprint
import sys
import time

app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
app.secret_key = os.urandom(24)

oauth = OAuth(app)
facebook = oauth.remote_app('facebook',
	base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=os.environ['FACEBOOK_APP_ID'],
    consumer_secret=os.environ['FACEBOOK_APP_SECRET'],
    request_token_params={'scope': 'email'}
)

login_error_message = None

def is_localhost():
	root_url = request.url_root
	developer_url = 'http://127.0.0.1:5000/'
	return root_url == developer_url

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
	callback = url_for('authorized', _external=True, _scheme='https')
	return facebook.authorize(callback=callback)


@app.route('/login/authorized')
def authorized():
	resp = facebook.authorized_response()

	if resp is None:
		session.clear()
		login_error_message = 'Access denied: reason=%s error=%s full=%s' % (
            request.args['error'],
            request.args['error_description'],
            pprint.pformat(request.args))
		flash(login_error_message, 'error')
        return redirect(url_for('home'))

	if isinstance(resp, OAuthException):
		return 'Access denied: %s' % resp.message

	session['oauth_token'] = (resp['access_token'], '') #Save access token in session
	current_user = facebook.get('/me')
	return 'Logged in as id=%s name=%s redirect=%s' % \
		(me.data['id'], me.data['name'], request.args.get('next'))


@app.route('/profile')
def profile():
	if not is_logged_in():
		error = "No user is currently logged in..."
		flash(error, 'error')
		return redirect(url_for('render_home'))
	else:
		user = facebook.get('user')
		return jsonify(user.data)


@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('render_home'))

@facebook.tokengetter
def get_facebook_oauth_token():
	return session['oauth_token']

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
