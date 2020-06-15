# catalog-app
A web application that provides a list of items within a variety of categories and integrate third party user registration and authentication. Authenticated users should have the ability to post, edit, and delete their own items.  

**Written in:** Python, HTML, CSS, PostgreSQL  
**Using:** VirtualBox, Vagrant, Flask, SQLAlchemy, Google Sign in, Facebook Sign in   

<img src="/img/main.png" alt="Home" width="400">  <img src="/img/login.png" alt="Login" width="400" >

## The Structure  
  
The catalog consists of the categories which consists of the items.  
  
<img src="/img/category.png" alt="Category" width="400">  <img src="/img/item.png" alt="Item" width="400" >  
  
The user can register/login via her Google or Facebook account.  
The registered users can create new categories and items.
They can update/delete their own categories and items.

<img src="/img/additem.png" alt="Add Item" width="400" > 

## How to use  
  
- Start your virtual machine and login  
-- Using [the same environment](https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile) is recommended.  
-- vagrant up & vagrant ssh
  
- Setup your database  
-- Run: python db_setup.py  
-- Database has three tables:  
-- User(id, name, email), Category (id, name, user_id) & Item (id, title, description, category, user_id)
  
- Add data_sample to your database  
-- Run: python data_sample.py  
-- data_sample is a simple .py file importing data for the categories in the database. You can see the websites/articles which the data are taken here: 
[Books](https://www.weforum.org/agenda/2015/11/the-20-most-influential-books-in-history/), 
[Movies](http://www.imdb.com/chart/top), 
[Musics](https://theculturetrip.com/north-america/articles/the-10-influential-songs-that-changed-the-world/), 
[Foods](http://www.cnn.com/travel/article/world-best-food-dishes/index.html), 
[Websites](https://en.wikipedia.org/wiki/List_of_most-popular_websites))  
  
- For Google sign in:  
-- Create an OAuth Client ID on the Google APIs Console and put in into the variable **data-clientid** in **login.html**  
-- Enter JavaScript origins ["http://localhost:5000/"]  
-- Enter redirect URIs ["http://localhost:5000/categories/","http://localhost:5000/"]  
-- Download JSON file and put into the project folder and make its name **client_secrets**  
  
- For Facebook sign in:  
-- Create an app on the Facebook developer console  
-- Put your **app_id** & **app_secret** in **fb_client_secrets.json**  
-- Enter Valid OAuth redirect URIs on the Facebook developer console:  
-- ["http://localhost:5000/"], ["http://localhost:5000/login/"]  
  
- Ready to go!  
-- Run: python project.py

### Routes  
  
**Show all categories & the JSON of all**  
localhost:5000/  
../categories/  
../categories/JSON  
  
**Login & Log out**  
../login  
../gconnect  
../fbconnect  
../disconnect  
  
**CRUD & JSON for Category table**    
../categories/create/  
../categories/<int:category_id>/  
../categories/<int:category_id>/items/  
../categories/<int:category_id>/JSON  
../categories/<int:category_id>/items/JSON  
../categories/<int:category_id>/update/  
../categories/<int:category_id>/delete/  
  
**CRUD & JSON for Item table**  
../categories/<int:category_id>/items/create/  
../categories/<int:category_id>/items/<int:item_id>/  
../categories/<int:category_id>/items/<int:item_id>/JSON  
../categories/<int:category_id>/items/<int:item_id>/update  
../categories/<int:category_id>/items/<int:item_id>/delete
