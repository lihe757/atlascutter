#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import os.path
import shutil
from PIL import Image


def cut(filename):

    if filename.find('.png') != -1:
        filename = filename[:-4]

    pngName = filename + '.png'
    atlasName = filename + '.atlas'

    print "config:", pngName, atlasName

    big_image = Image.open(pngName)
    big_image.convert("RGBA")
    atlas = file(atlasName, "r")


    curPath = os.getcwd()  # 当前路径
    aim_path = os.path.join(curPath, filename)
    print "saving path:" + aim_path
    if os.path.isdir(aim_path):
        shutil.rmtree(aim_path, True)  # 如果有该目录,删除
        os.makedirs(aim_path)

    #解析坐标
    while True:
        line1 = atlas.readline()  # name
        if len(line1) == 0:
            break
        else:
            data = line1.split(" ")

            name = data[0] + ".png"

            width = int(data[1])
            height = int(data[2])

            startx = int(1024 * float(data[3]))
            starty = int(1024 * float(data[4]))

            print name, width, height, startx, starty

            #剪切小图
            rect_on_big = big_image.crop((startx, starty, startx+width, starty+height))

            #张贴并保存小图
            result_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            result_image.paste(rect_on_big, (0, 0, width, height))
            result_image.save(aim_path+'/'+name)

    atlas.close()
    del big_image


def main():
    argvs = sys.argv
    if len(argvs) < 2:
        print 'Usage: atlascutter.py <atlasname>'
        return

    files = argvs[1:]
    for f in files:
        if os.path.exists(f) == False:
            print 'File ' + f + ' is not exists!'
            return
        print 'cuting: ' + f
        cut(f)

if __name__ == "__main__":
    main()

