# catalog-app
a web application that provides a list of items within a variety of categories and integrate third party user registration and authentication. Authenticated users should have the ability to post, edit, and delete their own items.  

**!!![Under Construction]!!!***  

### How to use  
- Start you virtual machine and login  
-- Using [the same environment](https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile) is recommended.  
-- vagrant up & vagrant ssh
- Setup your database  
-- run db_setup.py  
-- (Database has two tables: Category (id, name) & Item (id, title, description, category))
- Add data_sample to your database  
-- run data_sample.py  
-- (data_sample is a simple .py file importing data for the categories in the database. You can see the websites/articles which the data are taken here: 
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
  

### Routes  
  
**Show all categories & the JSON of all**  
localhost:5000/  
../categories/  
../categories/JSON  
  
**CRUD & JSON for Category table**    
../categories/create/  
../categories/<int:category_id>/  
../categories/<int:category_id>/items/  
../categories/<int:category_id>/JSON  
../categories/<int:category_id>/update/  
../categories/<int:category_id>/delete/  
  
**CRUD & JSON for Item table**  
../categories/<int:category_id>/items/create/  
../categories/<int:category_id>/items/<int:item_id>/  
../categories/<int:category_id>/items/<int:item_id>/JSON  
../categories/<int:category_id>/items/<int:item_id>/update  
../categories/<int:category_id>/items/<int:item_id>/delete
