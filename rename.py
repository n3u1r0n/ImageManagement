import os

convertedFolder = 'D:\\Photos Converted'
downscaledFolder = 'D:\\Photos Downscaled'

numbers = dict()

for foldername in os.listdir(convertedFolder):
  nIMG = 0
  nVID = 0
  for filename in os.listdir(os.path.join(convertedFolder, foldername)):
    name, extension = filename.split('.')
    n = None
    if name[:3] == 'IMG':
      nIMG += 1
      n = nIMG
    elif name[:3] == 'VID':
      nVID += 1
      n = nVID
    numbers[name] = n
    os.rename(os.path.join(convertedFolder, foldername, filename), os.path.join(convertedFolder, foldername, name[:11] + '_{:06}.'.format(n) + extension))

for foldername in os.listdir(downscaledFolder):
  for filename in os.listdir(os.path.join(downscaledFolder, foldername)):
    name, extension = filename.split('.')
    number = numbers[name]
    os.rename(os.path.join(downscaledFolder, foldername, filename), os.path.join(downscaledFolder, foldername, name[:11] + '_{:06}.'.format(number) + extension))