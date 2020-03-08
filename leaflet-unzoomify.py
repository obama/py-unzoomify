import sys, math, urllib.request, PIL.Image, os.path, re

url = False
width = 0
height = 0
tileSize = 256.
zoom = 1
maxZoom = 1
imageSizes = []
gridSizes = []



def main(argv):
    global width, height, url, zoom
    if len(argv) <= 2:
        url = argv[1]
        try:
            conn = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            print('HTTPError: {}'.format(e.code))
        except urllib.error.URLError as e:
            print('URLError: {}'.format(e.reason))
        else:
            # 200
            html = conn.readlines()
            pattern = r".+\.tileLayer\.zoomify\(\'(.+?)\',.*?\{.*?width:.+?(.+?),.*?height:.*?(.+?),.*?\}"
            match = re.search(pattern, str(html))
            if match:
                url  = match.groups()[0]
                width  = int(match.groups()[1])
                height  = int(match.groups()[2])
                print('Found leaflet zoomify. url: '+ str(url) + ' width: ' + str(width) + ' height: ' + str(height))
            else:
                print('No leaflet zoomify found.')
                sys.exit()
    elif len(argv) <= 3:
        print("usage: url width height <zoom>")
        sys.exit()
    else:
        width = int(argv[2])
        height = int(argv[3])
        url = argv[1]

    initialize()

    if (len(argv) == 4 or len(argv) == 2):
        zoom = maxZoom
    else:
        if (zoom > maxZoom):
            print("maximal zoom level: ", maxZoom)
            sys.exit()

    x_count = gridSizes[zoom][0]
    y_count = gridSizes[zoom][1]
    print('Downloading zoom level ' + str(zoom) + '. Amount of files: ' + str(x_count * y_count))
    
    for x in range(0, x_count):
        for y in range(0, y_count):
            if (os.path.isfile('_tmp_'+str(zoom)+'-'+str(x)+'-'+str(y)+'.jpg')):
                continue
            try:
                conn = urllib.request.urlopen(getTileUrl([x,y]))
            except urllib.error.HTTPError as e:
                print('HTTPError: {}'.format(e.code))
            except urllib.error.URLError as e:
                print('URLError: {}'.format(e.reason))
            else:
                # 200
                filename = '_tmp_' + str(zoom) + '-' + str(x) + '-' + str(y) + '.jpg'
                f = open(filename, 'wb')
                f.write(conn.read())
                #sys.exit()     

    print('Download complete. Stitching images..')       

    output = PIL.Image.new('RGB', (int(x_count * tileSize), int(y_count * tileSize)))
    for x in range(x_count):
        for y in range(y_count):
            input_img = PIL.Image.open('_tmp_' + str(zoom) + '-' + str(x) + "-" + str(y) + ".jpg")
            output.paste(input_img, (int(x * tileSize), int(y * tileSize)))
            input_img.close()
            
    output.save('out.jpg')

    print('done.')



def initialize():
    global imageSizes, gridSizes, maxZoom
    imageSize = [width, height]

    imageSizes = [imageSize]
    gridSizes = [_getGridSize(imageSize)]

    while (int(imageSize[0]) > tileSize or int(imageSize[1]) > tileSize):
       	imageSize = [imageSize[0] / 2, imageSize[1] / 2]
        imageSizes.append(imageSize)
        gridSizes.append(_getGridSize(imageSize))

    imageSizes.reverse()
    gridSizes.reverse()

    maxZoom = len(gridSizes) - 1


def _getGridSize(imageSize):
    return [math.ceil(imageSize[0] / tileSize), math.ceil(imageSize[1] / tileSize)]


def getTileUrl(tilePoint):
    return url + 'TileGroup' + str(_getTileGroup(tilePoint)) + '/' + str(zoom) + '-' + str(tilePoint[0]) + '-' + str(tilePoint[1]) + '.jpg'


def _getTileGroup(tilePoint):
    num = 0

    for z in range(0, zoom):
        gridSize = gridSizes[z]
        num += gridSize[0] * gridSize[1]

    num += tilePoint[1] * gridSizes[zoom][0] + tilePoint[0]
    return math.floor(float(num) / tileSize)


if __name__ == "__main__":
    main(sys.argv)
