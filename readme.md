<h1 align="center">One Page Facebook Scraper</h1>

# Description

<p align="center">A simple scraping service for a facebook page: nintendo. 
</p>

<p align="center">
</p>


# Live Demo

In progress

# Built with:

- Fastapi
- Uvicorn
- Mongodb
- Docker

# How to reproduce the development environment:

1. Make sure you have this python-version==3.8.10 and the virtualenv package

    ```bash
    python --version 
    pip install virtualenv
    ```

2. Create your python environment

    ```
    python -m venv py_env
    ```

3. Activate your virtual environment and make sure the pip version is 20.2.4:

    ```
    source py_env/bin/activate #in Ubuntu 20.04 
    ./py_env/Scripts/activate #in Windows 10

    python -m pip install pip==20.2.4
    ```

4. While the py_env is active, use the requirements.txt with pip or these commands:

    ```
    pip install -r src/requirements.txt
    ```

5. Create an .env file and put these pieces of information:

    * DB_CONNECTION: "mongodb connection string"

5. To test the app locally with debug mode:
    ```
    uvicorn src.app.main:app --reload
    ```

# Database:

1. Install mongodb, make sure that mongod service (daemon) is running.
```
sudo systemctl status mongod
```
if that is not the case, use:

```
sudo systemctl start mongod.service
```

2. Run the mongo shell and add a user with read/write privileges. 
```
use admin

db.createUser({ user: "admin" , pwd: "admin", roles: ["userAdminAnyDatabase", "dbAdminAnyDatabase", "readWriteAnyDatabase"]})

```
4. Log in to mongo as the new user
```
mongo --port 27017 -u "admin" -p "admin" --authenticationDatabase "admin"

```
5. Use a new db named fb_scraper. Create a collection named posts and add a unique index to the 'post_id' field
```
use fb_scraper

db.createCollection("posts")

db.createIndex({"post_id":1},{unique:true})

```


# Dockerization:

Still in progress...

# Tests:

```
env PYTHONPATH=/src/app/ python -m unittest 
```

# Post data structure:
For reference, a  json object with these fields:

```
['post_id', 'text', 'post_text', 'shared_text', 'time', 'timestamp', 'image', 'image_lowquality', 'images', 'images_description', 'images_lowquality', 'images_lowquality_description', 'video', 'video_duration_seconds', 'video_height', 'video_id', 'video_quality', 'video_size_MB', 'video_thumbnail', 'video_watches', 'video_width', 'likes', 'comments', 'shares', 'post_url', 'link', 'links', 'user_id', 'username', 'user_url', 'is_live', 'factcheck', 'shared_post_id', 'shared_time', 'shared_user_id', 'shared_username', 'shared_post_url', 'available', 'comments_full', 'reactors', 'w3_fb_url', 'reactions', 'reaction_count', 'with', 'image_id', 'image_ids', 'was_live']
```

# Future updates:

- [x] API code
- [ ] Dockerization
- [ ] Expand the api 

# Contributors:

- Khaled Adrani: https://github.com/khaledadrani



# References:
Links that may help you:
* https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-20-04
* https://docs.docker.com/engine/install/ubuntu/
* https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units
* https://medium.com/bb-tutorials-and-thoughts/how-to-use-mongodb-docker-image-with-nodejs-rest-api-3411582c71e5
* https://docs.docker.com/compose/gettingstarted/
* https://stackoverflow.com/questions/38921414/mongodb-what-are-the-default-user-and-password
* https://stackoverflow.com/questions/7247474/how-can-i-tell-where-mongodb-is-storing-data-its-not-in-the-default-data-db
* https://github.com/markqiu/fastapi-mongodb-realworld-example-app


