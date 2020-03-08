# py-unzoomify
a python script for download a leaflet zoomify image

# usage
`py leaflet-unzoomify.py url`

fetches url and tries to find the leaflet zoomify parameters then downloads and creates image

`py leaflet-unzoomify.py tile-baseurl width height`

you can supply the tile base url and image size in pixels. 

`py leaflet-unzoomify.py tile-baseurl width height zoom`

you can supply the tile base url and image size in pixels and also some zoom level if you dont want the highest resolution

