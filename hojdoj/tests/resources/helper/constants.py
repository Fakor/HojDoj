import os

SQUARE = '{}/resources/square.png'.format(os.environ['TEST_FOLDER'])

CONFIG={
    "image_templates":{
        "SQUARE": SQUARE
    },
    "fillers":{
    },
    "gravity": 5,
    "default_image": "SQUARE",
    "default_color": [0,0,0]
}
