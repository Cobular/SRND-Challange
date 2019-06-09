# Jake Cover's SRND Challenge

This web app displays the code day data in a SQLite database in a useful way, using Flask and SQLAlchemy.

## Instructions for Use

This uses docker-compose for deployment, so first make sure you have both docker and docker-compose on your system. See the docker documentation for instructions.

1. Make sure to put the database file in the root directory of the project, right next to this file. The app expects it to be called `codeday.db3`. If you are getting this in a tarball from me, it will already be there, but it is not there if you are cloning this from github
2. Just run `docker-compose up` and the service will start. 
3. If you want to run the app outside the docker container w/ `flask run`, there are a few more steps:
    1. Setup a venv (`python3 -m venv ./venv`, `source venv/bin/activate`) and install the requirements from requirements.txt (`pip install -r requirements.txt`)
    2. Set the `$FLASK_APP` environmental variable to `run` so the next command will know where to look to start the aoo
    3. Run the command `flask run`. You can add the optional arguments `-h localhost` and `-p 8080` to the end of the command to change the address and port the app is listening on.  
4. You can also use the `run.sh` file locally if you want to run the webapp with gunicorn handeling some of the stuff
    1. Setup a venv and install the requirements from the requirements.txt, then install gunicorn `pip install gunicorn`
    2. Run `./run.sh`, and the server should start up
5. Go to `localhost:8080` to view the site
6. Happy data viewing!


## Filesystem Explanation

Generally speaking, I made this project in Flask and heavily used SQLAlchemy and Bootstrap.

* A few things live in the root directory of the project: 
    * `config.py` stores some configuration for the flask app. 
    * `Dockerfile` and `docker-compose.yml` handle the docker deploying of the project
    * `run.py` is the python script that invokes the app factory and starts the flask app
    * `run.sh` is ran by the `Dockerfile`, it runs the gunicorn command that starts Flask. It's here so I can tun the app locally without waiting for Docker every time even though it could be built in to the `Dockerfile`
    * `requirements.txt` is just the pip requirements file.
* `srndchalengepackage/` contains most of the Flask app:
    * `__init__.py` contains the app factory and initializes a few important things related to the `app`, namely SQLAlchemy and Flask-Bootstrap
    * `models.py` contains the code that SQLAlchemy needs to get running. Since the database already exists, we simply need to look at the schema as they are already, which is accomplished with teh first line of both classes. The SQLAlchemy code for the table schema is present in the functions in the comments fo convince.
    * `main/` contains the routes that make up the meat of the app, as well as the blueprint boilerplate that allows this structure to work
        * `__init__.py` simply creates the `blueprint` that, among other things, lets this structure work
        * `routes.py` is the meat of the app. It contains all the SQLAlchemy queries and logic used to organize the data and formats it to be sent into the templates
    * `templates/` contains all the HTML for the app, broken up into blocks that make working with the HTML much easier
        * `base.html` is the base HTML template, and itself loads up the bootstrap base that comes preloaded with a bunch of bootstrap things already.
        * `results.html` is the template used by the main page. It doesnt do much by itself, but does import the data templates and loads up the custom css
        * `data_templates/` contains the templates used to present all the data
            * `panel.html` is the template that has all the template boilerplate that I stuff the data into, which makes everything look consistent
            * `early_birds.html` contains logic for presenting the number of early birds per event
            * `moneys.html` is really simple, just renders the made/lost template
            * `promos.html` renders the promo code information
            * `registrations.html` handles the display of the promo codes
    * `static/` contains the static files, like images and css.
        * `custom.css` contains the custom css that I use to override some of the bootstrap css in order to make the page look how I want
        * `avenir-next.css` defines the avenir next font and is imported in `custom.css`
        * `favicon-32x32` is the site favicon, it's a combination of a database logo and the codeday logo

That's pretty much it, hope you enjoy!
