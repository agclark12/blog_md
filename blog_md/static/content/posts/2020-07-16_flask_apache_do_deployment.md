title: Deploying a Python Flask app with Apache at Digital Ocean
date: 2020-07-16
tag: technical
summary: An overview of how I deployed this Flask-powered website on a virtual server at Digital Ocean using Apache.

As I had written in a <a href="http://www.andrewgclark.info/posts/2020-06-18_about_this_site/">previous post</a>,
I recently rebuilt this website using Python/Flask.
Although this wasn't my first Flask project, it was the first time I wanted to deploy an app on a production server to have it on the internet.
For some reason I thought most of the work was over once I had finished writing the app, and I seriously underestimated the deployment process.
Since this was all relatively new to me, I thought it might be nice to write a little overview of how I deployed this site in case it might be useful to anyone else.
As a disclaimer, I only really do this on a hobby basis, so you may want to consult other sources written by people that do this for a living, but maybe this will at least give you a start.

**1\. Picking a hosting service**

 I had previously hosted my site with A Small Orange, and I was pretty happy with the service, so I wanted to stay.
 My old site was just static pages, which was fine on a shared hosting account.
 However, it took me some time to figure out that deploying a Flask app would not really be possible on a shared hosing account.
 I also tried to set up the site at Bluehost using a shared hosting plan, but I quickly found out that this would be no different than on A Small Orange.
 In order to deploy and set things up as I wanted at A Small Orange or Bluehost, I would have had to get a VPS account, which was far out of my price range.
 In the end, I started a droplet over at [Digital Ocean](https://www.digitalocean.com/) for 5 bucks a month, which got a me a virtual server at a small fraction of the price at ASO or Bluehost.

**2\. Restructuring my app**

 One thing that helped early on was to change the structure of my app a little bit.
 I had originally written the app as a module (with everything in the same directory running under an `app.py` file) instead of a package (with a subdirectory containing an `__init__.py` file).
 Once I adopted a package structure, I moved all of the development-specific and production-specific configurations to different configuration files.
 This way, my app could use the dev-specific configurations on the development server (for testing on my local machine)
 and the production-specific configurations on the production server (on my virtual server).
 You can find a nice reference on how to structure you app using different configuration files [here](https://exploreflask.com/en/latest/configuration.html).
 I used a similar approach, but I just use `app.config.from_object()` for both the development and production config files and comment out whichever one I don't want, depending where I am running the app.
 You can see how I did this on the [github repo](https://github.com/agclark12/blog_md).
 You won't find the config files on github because they contain secret keys, etc.
 The main differences between the dev and production config files are the path to the database (which can be a relative path for the dev server, but must be an absolute path for the production server), and whether to run in debug mode or not (only for dev). 
 Once I had done this, I defined a new remote on git so I could push any changes to my server at Digital Ocean via ssh.
 
**3\. Start serving on Apache**

 Once I had my app on the server and configured for the production server, I installed Apache in a LAMP stack following [these instructions](https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-on-ubuntu).
 Then I installed Flask and my required packages in a virtual environment similar to [this walkthrough](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps).
 Note that for using Python 3.X, you must install the python3 version of mod_wsgi: `libapache2-mod-wsgi-py3`.
 For installing the virtual environment using python3, you can use `python3 -m venv venv`.
 This all assumes you are using the python 3 version already installed on the Digital Ocean server, which should be >3.5.
 You could also install your own version if you want to have more control over the interpreter.
 For installing packages into your virtual environment, you can use pip.
 It is a good idea to collect all of the packages you need (with versions specified) into a text file so you can run `pip install -r requirements.txt`.
 
 Another small change I had to make was to tell the wsgi file where to find my virtual environment by adding
    
    activate_this = '/var/www/app/venv/bin/activate_this.py'
    with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))
 
 just after `#!/usr/bin/python` as instructed [here](https://flask.palletsprojects.com/en/1.1.x/deploying/mod_wsgi/#working-with-virtual-environments).
 Note that the python3 virtual environment, for whatever reason does not ship with `activate_this.py`.
 According to [this SO answer](https://stackoverflow.com/questions/25020451/no-activate-this-py-file-in-venv-pyvenv#answers-header), you can just borrow `activate_this.py` from python2's `virtualenv`.
 You can find the source [here](https://github.com/pypa/virtualenv/blob/master/src/virtualenv/activation/python/activate_this.py) and just copy it into `var/www/app/venv/bin/activate_this.py`, and amazingly, it works!
 To get apache to use my virtual environment correctly, I had to add this to the apache config file, just below the `ServerAdmin` line:
 
    WSGIDaemonProcess app python-path=/var/www/app/ python-home=/var/www/app/venv
     
 Once you finish this and restart apache, you should be able to see your Flask app running at your droplet's IP address.
 It took me some time to figure all of this out, and so it is useful to know that the error log is stored at `/var/log/apache2/error.log` so you can try to identify what is going wrong while you set things up.
 
**4\. Domain transfer**

 Digital Ocean is not a domain registrar, so you can't register your domain directly with them.
 For now, my domain is still registered at A Small Orange.
 Digital Ocean gives specific instructions on [how to point your registered domain at your droplet's IP](https://www.digitalocean.com/community/tutorials/how-to-point-to-digitalocean-nameservers-from-common-domain-registrars).
 You'll have to update your apache conf file to use your domain as the `ServerName` if you had originally used your droplet's IP.
 Then you have to configure A records for your domain. Digital Ocean has a helpful guide on doing that [here](https://www.digitalocean.com/docs/networking/dns/how-to/manage-records/).
 
**5\. Security**

 Although I cannot say I really know much of anything about website security, I thought it would be at least a good idea to set up a firewall and secure the site by installing SSL certificates.
 Setting up a firewall using UFW is very easy following to [this guide](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-18-04).
 Getting SSL certificates is also pretty easy using Let's Encrypt following [this](https://www.digitalocean.com/community/tutorials/how-to-secure-apache-with-let-s-encrypt-on-ubuntu-18-04).
 Let's Encrypt's certbot will even update its own certificates regularly with this installation.
 Once I set up the SSL certificates, I redirected all HTTP traffic to HTTPS in the apache conf file.
 In the end, the full conf file looked like this:
 
    <IfModule mod_ssl.c>
    <VirtualHost *:80>
                    ServerName my.site
                    ServerAdmin user@email.com
                    ServerAlias www.my.site
                    Redirect permanent / https://my.site/
    </VirtualHost>
    <VirtualHost *:443>
            ServerName my.site
                    ServerAdmin user@email.com
                    ServerAlias www.my.site
                    WSGIDaemonProcess app python-path=/var/www/app/ python-home=/var/www/app/venv
                    WSGIProcessGroup app
                    WSGIApplicationGroup %{GLOBAL}
            WSGIScriptAlias / /var/www/app/app.wsgi process-group=app application-group=%{GLOBAL}
            <Directory /var/www/app/app/>
                Require all granted
                    </Directory>
            Alias /static /var/www/app/app/static
            <Directory /var/www/app/app/static/>
                Require all granted
            </Directory>
            ErrorLog ${APACHE_LOG_DIR}/error.log
            LogLevel warn
            CustomLog ${APACHE_LOG_DIR}/access.log combined
    
    Include /etc/letsencrypt/options-ssl-apache.conf
    SSLCertificateFile /etc/letsencrypt/live/my.site/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/my.site/privkey.pem
    </VirtualHost>
    </IfModule> 
 
**6\. Maintenance**

 Since I can just push my git repo to the server, maintaining the site is pretty easy.
 I also set up cron jobs to run regular updates, clear the logs and make backups.
 There is a nice tutorial on how to do that [here](https://www.digitalocean.com/community/tutorials/how-to-use-cron-to-automate-tasks-ubuntu-1804).
 
I think that about covers it. All in all, it was a nice learning experience, albeit sometimes frustrating.
I hope this overview might be useful to others as well.


