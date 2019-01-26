# encoding: utf-8

import os
import sys

def str2file(filepath, s):
    with open(filepath, encoding='utf8', mode='w') as f:
        f.write(s)

def get_filelist(basedir):
    ret = []
    for path, dirnames, filenames in os.walk(basedir):
        for filename in filenames:
            fullpath = os.path.join(path, filename)
            ret.append(fullpath)
    return ret

MYFULLPATH = os.path.abspath(sys.argv[0])
MYDIR = os.path.dirname(MYFULLPATH)

filenames_all = get_filelist(MYDIR)
filenames_jpg = [filename for filename in filenames_all if filename.lower()[-4:]=='.jpg']
filenames_curdir_removed = [filename.replace('{:}\\'.format(MYDIR), '') for filename in filenames_jpg]
filenames_slash_delim = [filename.replace('\\', '/') for filename in filenames_curdir_removed]

print(filenames_slash_delim)
print('{:} items.'.format(len(filenames_jpg)))

outfilename = 'image_gallery.html'
outstrs = ''

conf_image_x = 150
conf_image_y = 150
conf_image_count_per_line = 6

for i,image_filepath in enumerate(filenames_slash_delim):
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
str2file(outfilename, html)
