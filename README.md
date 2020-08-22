# blog_md

This is the source code for my website, which is currently hosted at [andrewgclark.info](http://andrewgclark.info).

The website is built using the Flask framework for Python.
It includes a blog using markdown formatting (hence the project title "blog_md").
I have also added a number of other pages and features, so it's more than just a blog in this form.
If you would like to use this as a template, feel free to download or clone this repo.
In order for you to serve this application, you will have to first create a couple of extra config files (I have left these out of the repo because they contain sensitive information).

instance/config.py :

    from blog_md import app
    
    app.config['SECRET_KEY'] = 'your_secret_key' 
        
config/development.py :

    from blog_md import app
    
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///relative/path/to/db'
    app.config['SECRET_KEY'] = 'dev'
    
Once you have created these files, you can set up your virtual environment.
While in outer blog_md folder, run `python3 -m venv venv` to set up your virtual environment.
Then you can use pip to get the additional packages you need.
For that, just run `pip install -r requirements.txt`.
The requirements file is already included in the repo.

Activate your virtual environment by executing `source venv/bin/activate`.
Then just run `python run.py`, and your website should be served on local host!

I currently host this website on a droplet from [digital ocean](http://digitalocean.com).
For an overview on setting up hosting, I wrote a blog entry about that [here](http://andrewgclark.info/posts/2020-07-16_flask_apache_do_deployment/).
