import os
from videoprops import get_video_properties
from math import sqrt

convertedFolder = 'D:\\Photos Converted'
downscaledFolder = 'D:\\Photos Downscaled'


def isImage(filename):
    return filename.split('.')[1].lower() in ['arw', 'cr2', 'dng', 'gpr', 'nef', 'jpg', 'jpeg', 'png']


def isVideo(filename):
    return filename.split('.')[1].lower() in ['avi', 'mov', 'mpg', 'mp4']


def isRaw(filename):
    return filename.split('.')[1].lower() in ['arw', 'cr2', 'dng', 'gpr', 'nef']


def isJpg(filename):
    return filename.split('.')[1].lower() in ['jpg', 'jpeg']


def isPng(filename):
    return filename.split('.')[1].lower() == 'png'



def convertImage(foldername, filename):
    if isRaw(filename):
        if not os.path.exists(os.path.join(downscaledFolder, foldername, filename.split('.')[0] + '.jpg')):
            os.system('convert "{}" -resize 2073600@> -quality 88 "{}"'.format(
                os.path.join(convertedFolder, foldername, filename.split('.')[0] + '.dng'),
                os.path.join(downscaledFolder, foldername, filename.split('.')[0] + '.jpg')
            ))
    if isJpg(filename):
        if not os.path.exists(os.path.join(convertedFolder, foldername, filename.split('.')[0] + '.jpg')):
            os.system('copy "{}" "{}"'.format(
                os.path.join(sourceFolder, foldername, filename),
                os.path.join(convertedFolder, foldername, filename.split('.')[0] + '.jpg')
            ))
        if not os.path.exists(os.path.join(downscaledFolder, foldername, filename.split('.')[0] + '.jpg')):
            os.system('convert "{}" -resize 2073600@> -quality 88 "{}"'.format(
                os.path.join(convertedFolder, foldername, filename.split('.')[0] + '.jpg'),
                os.path.join(downscaledFolder, foldername, filename.split('.')[0] + '.jpg')
            ))
    if isPng(filename):
        if not os.path.exists(os.path.join(convertedFolder, foldername, filename)):
            os.system('copy "{}" "{}"'.format(
                os.path.join(sourceFolder, foldername, filename),
                os.path.join(convertedFolder, foldername, filename)
            ))
        if not os.path.exists(os.path.join(downscaledFolder, foldername, filename.split('.')[0] + '.jpg')):
            os.system('convert "{}" -resize 2073600@> -quality 88 "{}"'.format(
                os.path.join(convertedFolder, foldername, filename),
                os.path.join(downscaledFolder, foldername, filename.split('.')[0] + '.jpg')
            ))


def convertVideo(foldername, filename):
    if not os.path.exists(os.path.join(convertedFolder, foldername, ('VID' + filename[3:]).split('.')[0] + '.mp4')):
        os.system('ffmpeg -n -hwaccel auto -i "{}" -c:v hevc_nvenc -rc constqp -qp 24 -b:v 0K -c:a aac -b:a 384k -vf yadif "{}"'.format(
            os.path.join(sourceFolder, foldername, filename),
            os.path.join(convertedFolder, foldername,
                         ('VID' + filename[3:]).split('.')[0] + '.mp4')
        ))
    if not os.path.exists(os.path.join(downscaledFolder, ('VID' + filename[3:]).split('.')[0] + '.mp4')):
        props = get_video_properties(os.path.join(sourceFolder, foldername, filename))
        width = int(props['width'])
        height = int(props['height'])
        scaling = sqrt(2073600 / (width * height))
        if scaling < 1:
            width *= scaling
            height *= scaling
        if 'tags' in props.keys():
            if 'rotate' in props['tags'].keys():
                if props['tags']['rotate'] == '90':
                    width, height = height, width
        framerate = min(30, int(props['nb_frames']) / float(props['duration']))   
        os.system('ffmpeg -n -hwaccel auto -i "{}" -c:v hevc_nvenc -rc constqp -qp 30 -b:v 0K -c:a aac -b:a 384k -vf yadif=1,scale={}:{} -r {} "{}"'.format(
            os.path.join(sourceFolder, foldername, filename),
            width,
            height,
            framerate,
            os.path.join(downscaledFolder, foldername,
                         ('VID' + filename[3:]).split('.')[0] + '.mp4')
        ))


if not os.path.exists(os.path.join(downscaledFolder)):
    os.mkdir(os.path.join(downscaledFolder))

if not os.path.exists(os.path.join(convertedFolder)):
    os.mkdir(os.path.join(convertedFolder))


for foldername in os.listdir(os.path.join(sourceFolder)):
    if not os.path.exists(os.path.join(convertedFolder, foldername)):
        os.mkdir(os.path.join(convertedFolder, foldername))
    if not os.path.exists(os.path.join(downscaledFolder, foldername)):
        os.mkdir(os.path.join(downscaledFolder, foldername))
    for filename in os.listdir(os.path.join(sourceFolder, foldername)):
        print('Doing', foldername, filename)
        if isImage(filename):
            convertImage(foldername, filename)
        elif isVideo(filename):
            convertVideo(foldername, filename)