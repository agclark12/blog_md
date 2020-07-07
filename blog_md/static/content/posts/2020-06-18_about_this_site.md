title: About this site
date: 2020-06-18
tag: misc
summary: A few words about what went into making this site.

Once in a great while I come across something new or interesting (usually related to image analysis), and I feel the urge to share it.
Rather than creating and answering my own questions on Stack Overflow, I though a blog might be a nicer format to do this.
I had been thinking about adding a blog to this website for a while,
but I never really had the gumption. The old version of the site was just a bunch of static
html pages templated with the help of Jinja2. So it was kind of a pain to add new content.
I wanted to have something where formatting the content would be easy, so I opted to use Markdown.
 
Markdown formatting makes it very convenient, for example, to format lists

* 1
* 2
* 3

or 

>block quotes

and it is also handy for writing `inline code` as well as blocks of code:

    def foo():
        return "bar"

So I started a little Markdown-powered blog project using the Flask library for Python.
It was pretty straightforward using some nice online resources, in particular
<a href="https://www.jamesharding.ca/posts/simple-static-markdown-blog-in-flask/">this post from James Harding</a>.
Once I had finished that, well, I decided I could just redo the whole website, which I had been wanting to do for some time anyway.
It turned out to be a really fun little project.
And now I have even real backend for this website!
I'll try to post when I can about science, programming, books, etc.
Also, I'll make the git repo for the website public at some point once I clean it up a little.
You'll be able to find that on the <a href="{{url_for('resources' )}}">resources page</a>.
