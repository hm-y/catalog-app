# Import libraries, Connect DB, Set up session

from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///content.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# CRUD & JSON for Category Table

# Read all the categories

@app.route('/')
@app.route('/categories/')
def showCategories():
    categories = session.query(Category).all()
    return render_template('main.html', categories=categories)

@app.route('/categories/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in restaurants])

# Create new category

@app.route('/categories/create/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')


# Read One Category

@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/items/')
def showCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('category.html', items=items, category=category)

@app.route('/categories/<int:category_id>/JSON')
def oneCategoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(items=[i.serialize for i in items])


# Update a category

@app.route('/categories/<int:category_id>/update/', methods=['GET', 'POST'])
def updateCategory(category_id):
    updatedOne = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            updatedOne.name = request.form['name']
            return redirect(url_for('showCategories'))
    else:
        return render_template(
            'updateCategory.html', category=updatedOne)


# Delete a category

@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    deletedOne = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(deletedOne)
        session.commit()
        return redirect(
            url_for('showCategories', category_id=category_id))
    else:
        return render_template(
            'deleteCategory.html', category=deletedOne)


# CRUD & JSON for Item Table

# Create a new item

@app.route('/categories/<int:category_id>/items/create/', methods=['GET', 'POST'])
def addItem(category_id):
    if request.method == 'POST':
        newItem = Item(title=request.form['title'],
                            description=request.form['description'],
                            category_id=category_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCategory', category_id=category_id))

    else:
        return render_template('additem.html', category_id=category_id)
    # necessary ???
    return render_template('additem.html', category_id=category_id)


# Read one item

@app.route('/categories/<int:category_id>/items/<int:item_id>/')
def showItem(item_id):
    item = session.query(Item).filter_by(item_id=item_id).one()
    return render_template('item.html', item=item)

@app.route('/categories/<int:category_id>/items/<int:item_id>/JSON')
def oneItemJSON(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item=item.serialize)


# Update an item

@app.route('/categories/<int:category_id>/items/<int:item_id>/update', methods=['GET', 'POST'])
def updateItem(category_id, item_id):
    updatedOne = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['title']:
            updatedOne.name = request.form['title']
        if request.form['description']:
            updatedOne.description = request.form['description']
        session.add(updatedOne)
        session.commit()
        return redirect(url_for('showCategory', category_id=category_id))

    else:
        return render_template(
            'updateitem.html', category_id=category_id, item_id=item_id, item=updatedOne)


# Delete an item

@app.route('/categories/<int:category_id>/items/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    deletedOne = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(deletedOne)
        session.commit()
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('deleteItem.html', item=deletedOne)


# Run the website on the port 5000

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
