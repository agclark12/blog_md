title: Largest Rectangle Algorithm
date: 2020-05-02
tag: image analysis
summary: Notes on using the largest rectangle algorithm for automatically cropping crooked images.

Most of my research deals in some way live microscopy data and the analysis thereof.
As biological samples (and microscopes for that matter) tend to be unstable over time, and the samples appear to wobble around.
Here is an image series where the object of interest (the white square) moves around over time:

<video class="research-video" preload controls muted src={{url_for("static", filename="content/posts/media/stk_adj.mp4")}} poster="{{ url_for('static', filename='content/posts/media/stk_adj_t0.jpg') }}" alt="registered stack"></video>
&nbsp;

It is often necessary to "register" image series in order to keep things in focus.
There are nicely working plugins for this in FIJI/ImageJ, and the idea is that the algorithm goes through each frame and adjusts the image so that it bests matches the initial image or prevoius frame.
Here is the same image series from above registred with TurboReg in FIJI:

<video class="research-video" preload controls muted src={{url_for("static", filename="content/posts/media/stk_adj_reg.mp4")}} poster="{{ url_for('static', filename='content/posts/media/stk_adj_reg_t0.jpg') }}" alt="registered stack"></video>
&nbsp;

This is certainly an improvement, since our object of interest says in place.
However, we are left black edges that dance around the outside of the image.
In order to get rid of the black edges, one needs to crop the image stack.
For a handful of images, this is easy to do by hand, but for a lot of images, one needs an automated solution to run in batch.

I had written a little script in FIJI a while ago to do this for translation-based image registration (i.e. without rotation), where the registered part of the image remained square with vertical or horizontal images.
However, I recently needed to do some rigid-body registration including rotation, and my algorithm for cropping the black edges didn't work for this.  
After playing around with this for a while, I realized that what I was really trying to do was to crop out the largest possible square in the image.

As it turns out, this problem is apparently related to a really classic problem in algorithm development for finding the largest rectangle in a histogram, with an O(n) solution.
After reading more about this problem and its solutions, I could write an algorithm to do this in Python that takes an image and gives the top left coordinates, width and height of the largest zero rectangle: 

    import numpy as np

    def find_largest_rectangle_2D(array):
        """Gets the coordinates of the largest rectangle of 1s in a 2D binary array"""
    
        #first get the sums of successive vertical pixels
        vert_sums = (np.zeros_like(array)).astype('float')
        vert_sums[0] = array[0]
        for i in range(1,len(array)):
            vert_sums[i] = (vert_sums[i-1] + array[i]) * array[i]
    
        #declare some variables for keeping track of the largest rectangle
        max_area = -1
        pos_at_max_area = (0,0)
        height_at_max_area = -1
        x_end = 0
    
        #go through each row of vertical sums and find the largest rectangle
        for i in range(len(vert_sums)):
            positions = []  # a stack
            heights = []  # a stack
            for j in range(len(vert_sums[i])):
                h = vert_sums[i][j]
                if len(positions)==0 or h > heights[-1]:
                    heights.append(h)
                    positions.append(j)
                elif h < heights[-1]:
                    while len(heights) > 0 and h < heights[-1]:
                        h_tmp = heights.pop(-1)
                        pos_tmp = positions.pop(-1)
                        area_tmp = h_tmp * (j - pos_tmp)
                        if area_tmp > max_area:
                            max_area = area_tmp
                            pos_at_max_area = (pos_tmp,i) #this is the bottom left
                            height_at_max_area = h_tmp
                            x_end = j
                    heights.append(h)
                    positions.append(pos_tmp)
            while len(heights) > 0:
                h_tmp = heights.pop(-1)
                pos_tmp = positions.pop(-1)
                area_tmp = h_tmp * (j - pos_tmp)
                if area_tmp > max_area:
                    max_area = area_tmp
                    pos_at_max_area = (pos_tmp,i) #this is the bottom left
                    height_at_max_area = h_tmp
                    x_end = j
    
        top_left = (int(pos_at_max_area[0]),int(pos_at_max_area[1] - height_at_max_area) + 1)
        width = int(x_end - pos_at_max_area[0])
        height = int(height_at_max_area - 1)
    
        return top_left,width,height
    
For the input image, you can threshold all of the non-zero values with `(stk > 0).astype('uint8')` and do a minimum projection of your timeseries using `np.min(stk,axis=0)`.
Be sure to fill in any holes using `scipy.ndimage.morphology.binary_fill_holes`.

In the first step, the columns in the vertical direction to one-dimensionalize the data.
Then, one can apply the algorithm to find the largest rectangle in a histogram.
There is a very nice video <a href="https://youtu.be/VNbkzsnllsU">here</a> that walks through the algorithm if you are interested.

Running this on the registered image series from above, we get a nicely cropped image:

<video class="research-video" preload controls muted src={{url_for("static", filename="content/posts/media/stk_adj_reg_crop.mp4")}} poster="{{ url_for('static', filename='content/posts/media/stk_adj_reg_crop_t0.jpg') }}" alt="registered stack"></video>
