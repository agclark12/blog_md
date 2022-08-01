title: Multiple bibliographies in LaTeX (updated)
date: 2020-06-24
tag: latex etc
summary: How to use generate bibliographies in LaTeX to account for references used only in the supplementary information.

Most manuscripts nowadays (in my field anyway) have separate supplementary information that usually includes some additional references.
These may be to support supplementary/online-only methods or explanations about theory, etc.
I think I've solved this problem in a few different ways over the years, but I have finally found a solution that I am quite happy with, using the [multibib](https://ctan.org/pkg/multibib?lang=en) package for BibTeX.

I usually don't split my main and supplementary files in LaTeX.
Using one file just makes it easier to deal with figure references.
Once I'm finished typesetting everything, I just split it into two separate documents using pdfjam.

In `multibib` the default behavior is to continue numbering between the bibliographies, which is pretty standard practice in most journals.
But the thing that I really find cool about `multibib` is that there is a mechanism in place to make sure that references only show up in one bibliography.
If you cite the same article in the main and supplementary text, it only shows up in the main bibliography, and that number is used also used for the citations in the supplementary information.

Here's a minimal working example for making separate bibliographies for the main text and supplementary information:

    \documentclass{article}
    \usepackage{filecontents}
    \usepackage{multibib}
    \newcites{supp}{Supplementary References}
    
    %this just writes the bib file on the fly
    \begin{filecontents}{mybib.bib}
    @misc{A:2015,
      author = {Alpha, A.},
      year = {2015},
      title = {Title A},
    }
    @misc{B:2017,
      author = {Beta, B.},
      year = {2017},
      title = {Title B},
    }
    @misc{C:2019,
      author = {Charlie, C.},
      year = {2019},
      title = {Title C},
    }
    @misc{D:2020,
      author = {Delta, D.},
      year = {2020},
      title = {Title D},
    }
    \end{filecontents}
    
    \begin{document}
    
    \section*{Main Text}
    
    Here is the main text where you can cite some things \cite{A:2015}.
    You can also cite some other things \cite{B:2017}.
    
    \bibliographystyle{plain}
    \bibliography{mybib}
    
    \section*{Supplementary Information}
    
    Here in the supplementary information or appendix, you can cite some new things \citesupp{C:2019,D:2020}.
    Note that if you want to cite references that you already cited in the first section, you should use the cite command from the first section \cite{A:2015}.
    If you do not, the reference will still be cited according to the first numbering scheme, but it will show up in your second bibliography as well.
    
    \bibliographystylesupp{plain}
    \bibliographysupp{mybib}
    
    \end{document}
  
In order to typeset your document with the bibliographies, you will have to run the following:

    latex mydoc
    bibtex mydoc
    bibtex supp
    latex mydoc
    latex mydoc
    
Since it's kind of a pain to write all of these out each time you want to compile your document, here's a little bash function you can add to your .bash_profile:

    compile_multibib() {
      latex $1; bibtex $1; bibtex supp; latex $1; latex $1
    }
    
Then you can just run this with `compile_multibib mydoc`.
And voilà, the result:

&nbsp;
<img src={{url_for("static", filename="content/posts/media/two_bib.jpg")}} class="blog-img" style="width:70%"></img>

**Update (1 Aug. 2022):**

Apparently `multibib` does not play well with the `cite` package.
Using the two together will cause the citations that you re-use in your bibliography
(which should be numbered as in the main bibliography and not show up in the supplementary bibliography)
to also show up in the supplementary bibliography.

If you are currently using `cite` (for example for ordered numbered citations),
you can use [natbib](https://www.overleaf.com/learn/latex/Bibliography_management_with_natbib) instead.
Unlike `cite`, `natbib` will play nicely with `multibib`.




