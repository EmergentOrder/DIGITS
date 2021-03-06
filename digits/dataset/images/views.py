# Copyright (c) 2014-2015, NVIDIA CORPORATION.  All rights reserved.

import os.path
from cStringIO import StringIO

from flask import request
import PIL.Image

from digits import utils
from digits.webapp import app
import classification.views

NAMESPACE = '/datasets/images'

@app.route(NAMESPACE + '/resize-example', methods=['POST'])
def image_dataset_resize_example():
    """Returns a string of png data"""
    try:
        import digits
        example_image_path = os.path.join(os.path.dirname(digits.__file__), 'static', 'images', 'mona_lisa.jpg')
        image = utils.image.load_image(example_image_path)

        width = int(request.form['width'])
        height = int(request.form['height'])
        channels = int(request.form['channels'])
        resize_mode = request.form['resize_mode']
        encoding = request.form['encoding']

        image = utils.image.resize_image(image, height, width,
                channels=channels,
                resize_mode=resize_mode,
                )

        if encoding == 'none':
            length = len(image.tostring())
        else:
            s = StringIO()
            if encoding == 'png':
                PIL.Image.fromarray(image).save(s, format='PNG')
            elif encoding == 'jpg':
                PIL.Image.fromarray(image).save(s, format='JPEG', quality=90)
            else:
                raise ValueError('unrecognized encoding "%s"' % encoding)
            s.seek(0)
            image = PIL.Image.open(s)
            length = len(s.getvalue())

        data = utils.image.embed_image_html(image)

        return '<img src=\"' + data + '\" style=\"width:%spx;height=%spx\" />\n<br>\n<i>Image size: %s</i>' % (
                width,
                height,
                utils.sizeof_fmt(length)
                )
    except Exception as e:
        return '%s: %s' % (type(e).__name__, e)

