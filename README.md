# Art gallery

## Application features
Art gallery is a web application where users can share their artwork and interact with other artists.

* User can create an account and sign in to the application.
* Users can create posts consisting of an artwork image, a title, a description and one or more art forms.
* Each post represents a single artwork. The artwork image is uploaded when the post is created and cannot be changed afterwards. If the user wishes to replace the artwork, they can create a new post.
* Users can edit the title, description and art form selections of their posts, or delete the entire post.
* Users can browse all artwork shared in the application.
* Users can search posts by keyword and/or filter the results by category.
* Each user has a user page displaying their posts with simple statistics.
* Users can discuss posts and ideas by commenting. They can also edit and delete their own comments.


## Application setup

install the Flask library:

```
$ pip install flask
```

create the database table and load the intial data:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

start the application:

```
$ flask run
```
