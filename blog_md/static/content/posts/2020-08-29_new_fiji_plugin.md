title: New FIJI Plugin (Largest Rectangle Algorithm Continued)
date: 2020-08-29
tag: image analysis
summary: I recently wrote a jython script that can be used as an ImageJ/FIJI plugin. The plugin will automatically crop black edges away from images using the largest rectangle algorithm. 

In a [previous post](https://www.andrewgclark.info/posts/2020-05-02_rectangle_algorithm/), I discussed using the largest rectangle (a.k.a. largest histogram) algorithm to automatically crop crooked images (i.e. images with non-straight black boundaries).
I finally got around to writing a jython script to use this algorithm in ImageJ/FIJI.

This was the first jython script I have written in several years, as I have moved to using primarily python for image and data analysis (though I still use the ImageJ Macro language for most of my pre-processing).
I thought this particular function may be useful for other people as well, since a lot of people are doing image registration for timelapse images.
I spent quite a bit of time going back and forth between doing this in jython or rewriting it in java to make a plugin.
In the end, it was a lot more efficient to do it in jython, since it was already written in python (although I had to make it work without numpy).
It did take a little effort to figure out how to do the basic input/output and convert between data types for ImageJ, but probably less effort than trying to refresh my java skills enough to rewrite it.
I guess I can always do it in java in the future if I have the gumption.

Anyway, I hope it will be useful for other people as well!
You can find the plugin with instructions for installation and use on [github](https://github.com/agclark12/autocrop_black_edges).
