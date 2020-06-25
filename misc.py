class Pages():
    """
    Still trying to figure out a pretty way to index a dictionary and put that into HTML without having a blob like so.
    This is my soution for now. Will work on it later! 
    """
    def PosterPage(d):
        """
        This function just makes things look a lot cleaner in the main file. 
        May add a lot more to it 
        """"

        return """<style>
                body {background-color: palevioletred;}
                h1   {color: blue;}
                p    {color: red;}
                
                .center {
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 25%;
                }
                
                </style>        """ + "<img src="+d['Poster']+" class=center><center><p style=\"font-family:Arial;font-size: 44px; \">Successfully added "+d['Title']+" to the movie list.</center>"
    def RandomPage(d):
        return """<style>
                body {background-color: palevioletred;}
                h1   {color: blue;}
                p    {color: red;}

                .center {
                  display: block;
                  margin-left: auto;
                  margin-right: auto;
                  width: 25%;
                }

                </style>        """ + "<img src=" + d[
        'Poster'] + " class=center><center><p style=\"font-family:Arial;font-size: 44px; \">Your movie for tonight is..." + d[
               'Title'] + " to the movie list.</center>"
