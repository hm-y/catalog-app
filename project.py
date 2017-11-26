# Import libraries, Connect DB, Set up session

# !/usr/bin/env python

from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Category, Item, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)
app.secret_key = "my secret key"

engine = create_engine('sqlite:///content.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(open(
    'client_secrets.json', 'r').read())['web']['client_id']
registeredUser = False

# CRUD & JSON for Category Table

# Read all the categories


@app.route('/')
@app.route('/categories/')
def showCategories():
    items = session.query(Item).all()
    num_items = session.query(Item).count()
    categories = session.query(Category).all()
    num_categories = session.query(Category).count()
    return render_template('main.html', categories=categories, items=items,
                           num_items=num_items, num_cat=num_categories)


@app.route('/categories/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


# Create new category


@app.route('/categories/create/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        flash("You need to log in to create a new category!")
        return redirect('/login')
    if request.method == 'POST':
        categories = session.query(Category).all()
        name = request.form['name']
        isSame = False
        for cat in categories:
            if cat.name == name:
                isSame = True
        if not name:
            flash("The name cannot be blank.")
            return render_template('newCategory.html')
        elif isSame:
            flash("There is already a category with the name '" + name + "'.")
            return render_template('newCategory.html')
        else:
            newCategory = Category(name=name,
                                   user_id=login_session['user_id'])
            session.add(newCategory)
            session.commit()
            flash("New category added!")
            return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')


# Read One Category

@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/items/')
def showCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    num_items = session.query(Item).filter_by(category_id=category_id).count()
    owner = getUserInfo(category.user_id)
    if 'username' not in login_session or owner.id != login_session['user_id']:
        registeredUser = False
    else:
        registeredUser = True
    return render_template('category.html', items=items,
                           category=category, registeredUser=registeredUser,
                           num_items=num_items)


@app.route('/categories/<int:category_id>/JSON')
@app.route('/categories/<int:category_id>/items/JSON')
def oneCategoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(items=[i.serialize for i in items])


# Update a category

@app.route('/categories/<int:category_id>/update/', methods=['GET', 'POST'])
def updateCategory(category_id):
    if 'username' not in login_session:
        flash("You need to log in to update your category.")
        return redirect('/login')
    updatedOne = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        categories = session.query(Category).all()
        name = request.form['name']
        isSame = False
        for cat in categories:
            if cat.name == name:
                isSame = True
        if not name:
            flash("The name cannot be blank.")
            return render_template(
                'updateCategory.html', category=updatedOne)
        elif isSame:
            flash("There is already a category with the name '" + name + "'.")
            return render_template(
                'updateCategory.html', category=updatedOne)
        else:
            updatedOne.name = name
            session.add(updatedOne)
            session.commit()
            flash("The category updated!")
            return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template(
            'updateCategory.html', category=updatedOne)


# Delete a category

@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
        flash("You need to log in to delete your category.")
        return redirect('/login')
    deletedOne = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    if request.method == 'POST':
        session.delete(deletedOne)
        for item in items:
            session.delete(item)
        session.commit()
        flash("The category deleted!")
        return redirect(
            url_for('showCategories'))
    else:
        return render_template('deleteCategory.html', category=deletedOne)


# CRUD & JSON for Item Table

# Create a new item

@app.route('/categories/<int:category_id>/items/create/',
           methods=['GET', 'POST'])
def addItem(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        flash("You need to log in to add a new item.")
        return redirect('/login')
    if request.method == 'POST':
        items = session.query(Item).filter_by(category_id=category_id).all()
        title = request.form['title']
        description = request.form['description']
        isSame = False
        for item in items:
            if item.title == title:
                isSame = True
        if not title or not description:
            flash("The title or description cannot be blank.")
            return render_template('additem.html',
                                   category_id=category_id, category=category)
        elif isSame:
            flash("There is already an item with the title '" + title +
                  "' in this category.")
            return render_template('additem.html',
                                   category_id=category_id, category=category)
        else:
            newItem = Item(title=title,
                           description=description,
                           category_id=category_id,
                           user_id=login_session['user_id'])
            session.add(newItem)
            session.commit()
            flash("New item added!")
            return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('additem.html',
                               category_id=category_id, category=category)


# Read one item

@app.route('/categories/<int:category_id>/items/<int:item_id>/')
def showItem(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    owner = getUserInfo(item.user_id)
    if 'username' not in login_session or owner.id != login_session['user_id']:
        registeredUser = False
    else:
        registeredUser = True
    return render_template('item.html', category=category,
                           item=item, registeredUser=registeredUser)


@app.route('/categories/<int:category_id>/items/<int:item_id>/JSON')
def oneItemJSON(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item=item.serialize)


# Update an item

@app.route('/categories/<int:category_id>/items/<int:item_id>/update',
           methods=['GET', 'POST'])
def updateItem(category_id, item_id):
    if 'username' not in login_session:
        flash("You need to log in to update your item.")
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    updatedOne = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        items = session.query(Item).filter_by(category_id=category_id).all()
        title = request.form['title']
        description = request.form['description']
        isSame = False
        for item in items:
            if item.title == title:
                isSame = True
        if not title or not description:
            flash("The title or description cannot be blank.")
            return render_template(
                'updateItem.html', category_id=category_id, item_id=item_id,
                category=category, item=updatedOne)
        elif isSame:
            flash("There is already an item with the title '" + title +
                  "' in this category.")
            return render_template(
                'updateItem.html', category_id=category_id, item_id=item_id,
                category=category, item=updatedOne)
        else:
            updatedOne.title = title
            updatedOne.description = description
            session.add(updatedOne)
            session.commit()
            flash("The item updated!")
            return redirect(url_for('showItem',
                                    category_id=category_id, item_id=item_id))

    else:
        return render_template(
            'updateItem.html', category_id=category_id, item_id=item_id,
            category=category, item=updatedOne)


# Delete an item

@app.route('/categories/<int:category_id>/items/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    if 'username' not in login_session:
        flash("You need to log in to delete your item.")
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    deletedOne = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(deletedOne)
        session.commit()
        flash("the item deleted!")
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('deleteItem.html', category_id=category_id,
                               category=category, item=deletedOne)

# Login page


@app.route('/login/')
def login():
    if 'username' in login_session:
        flash("Already logged in! Keep going to log in another account.")
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# gconnect & gdisconnect taken from Part 3 Lesson 11 - Udacity FSND and edited

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print 'Token\'s client ID does not match app\'s.'
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                 'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    flash("Logged in!")
    return "Done!"

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps(
                                 'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/')
    else:
        response = make_response(json.dumps('Failed to revoke token \
                                                for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we
        have to split the token first on commas and select the first index
        which gives us the key : value for the server access token then we
        split it on colons to pull out the actual token value and replace
        the remaining quotes with nothing so that it can be used directly
        in the graph api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    flash("Now logged in as %s" % login_session['username'])
    return "Done!"


def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
          facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "Done!"


# Disconnect based on provider


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['access_token']
            del login_session['gplus_id']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategories'))


# Run the website on the port 5000


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
