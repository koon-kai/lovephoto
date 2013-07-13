#!/usr/bin/env python
#coding=utf-8

import time
import Image
import os
import config
import StringIO

def make_thumb(photo, size=75):

    timestamp = str(time.time()).split('.')[0]
    #photo_name = timestamp + "_" + "%sx%s"%(str(size),str(size)) + ".jpg"
    photo_name = timestamp + ".jpg"
    photo_dir = config.UPLOAD_PHOTO_DIR + photo_name

    try:
        im = Image.open(photo)
    except IOError:
        return

    mode = im.mode
    if mode not in ('L', 'RGB'):
        if mode == 'RGBA':
            # 透明图片需要加白色底
            alpha = im.split()[3]
            bgmask = alpha.point(lambda x: 255-x)
            im = im.convert('RGB')
            # paste(color, box, mask)
            im.paste((255,255,255), None, bgmask)
        else:
            im = im.convert('RGB')

    width, height = im.size
    if width == height:
        region = im
    else:
        if width > height:
            delta = (width-height)/2
            box = (delta,0,delta+height,height)
        else:
            delta = (height - width)/2
            box = (0,delta,width,delta+width)
        region = im.crop(box)

    #for size in sizes:
    #    filename = photo_name+"_"+"%sx%s"%(str(size),str(size))+".jpg"
    #    thumb = region.resize((size,size),Image.ANTIALIAS)
    #    thumb.save(config.UPLOAD_PHOTO_DIR+filename,quality=100)

    thumb = region.resize((size,size),Image.ANTIALIAS)
    thumb.save(photo_dir,quality=100)

    return photo_name

def get_thumb(photo,p_width=215,p_height=185):


    try:
        im = Image.open(photo)
    except IOError:
        return

    mode = im.mode
    if mode not in ('L', 'RGB'):
        if mode == 'RGBA':
            # 透明图片需要加白色底
            alpha = im.split()[3]
            bgmask = alpha.point(lambda x: 255-x)
            im = im.convert('RGB')
            # paste(color, box, mask)
            im.paste((255,255,255), None, bgmask)
        else:
            im = im.convert('RGB')

    width, height = im.size
    if width == height:
        region = im
    else:
        if width > height:
            delta = (width-height)/2
            box = (delta,0,delta+height,height)
        else:
            delta = (height - width)/2
            box = (0,delta,width,delta+width)
        region = im.crop(box)

    output = StringIO.StringIO()
    thumb = region.resize((p_width,p_height),Image.ANTIALIAS)
    thumb.save(output,"JPEG",quality=100)
    img_date = output.getvalue()
    output.close()

    return img_date

def del_thumb(file_dir):

    if os.path.isfile(file_dir):
        os.remove(file_dir)
    else:
        raise Exception('Error: %s file is not found.' % file_dir)
