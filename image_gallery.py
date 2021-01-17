# encoding: utf-8

import os
from itertools import zip_longest
import sys
import argparse

def str2file(filepath, s):
    with open(filepath, mode='w') as f:
        f.write(s)

def get_filelist(basedir):
    ret = []
    for path, dirnames, filenames in os.walk(basedir):
        for filename in filenames:
            fullpath = os.path.join(path, filename)
            ret.append(fullpath)
    return ret


conf_image_x = 500
conf_image_y = 500
conf_image_count_per_line = 3
conf_images_per_page = 50

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

galleries_generated = []

def generate_gallery_with_index(rootdir):
    filenames_all = get_filelist(rootdir)
    filenames_jpg = [filename for filename in filenames_all if filename.lower()[-4:] == '.jpg']
    filenames_curdir_removed = [filename.replace('{:}\\'.format(rootdir), '') for filename in filenames_jpg]
    filenames_slash_delim = [filename.replace('\\', '/') for filename in filenames_curdir_removed]

    print(filenames_slash_delim)
    print('{:} items.'.format(len(filenames_jpg)))
    for pagecount, page in enumerate(grouper(filenames_slash_delim, conf_images_per_page)):
        outstrs = ''
        for i,image_filepath in enumerate(page):
            url = image_filepath
            alttext = url

            image_html_template = '<a href="{href}" target="_blank"><img src="{src}" width="{width}px" height="{height}px"></a>'
            image_kwargs = {
                'href'   : url,
                'src'    : url,
                'width'  : conf_image_x,
                'height' : conf_image_y,
            }

            image_html = image_html_template.format(**image_kwargs)

            outstrs += image_html
            outstrs += '\n'
            if i%conf_image_count_per_line==(conf_image_count_per_line-1):
                outstrs += '<br>\n'

        html_template = """<html>
        <head>
            <title>Image Gallery</title>
            <meta charset="UTF-8">
        </head>
        <body>
        {:}
        </body>
        </html>"""

        html = html_template.format(outstrs)
        basename = "image_gallery_{}.html".format(pagecount)
        outfilename = os.path.join(rootdir, basename)
        str2file(outfilename, html)
        galleries_generated.append(basename)

    index_template = """<html>
        <head>
            <title>Image Galleries</title>
            <meta charset="UTF-8">
        </head>
        <body>
        {:}
        </body>
        </html>"""

    gallery_links = []
    for gallery in galleries_generated:
        gallery_links.append("<a href=\"{}\">Gallery {}</a>".format(gallery, gallery))
    html = index_template.format("<br/>".join(gallery_links))
    str2file(os.path.join(rootdir, "index.html"), html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("rootdir")
    args = parser.parse_args()
    generate_gallery_with_index(args.rootdir)
