# obsolete - used for migration from version < 1.0
CONTENT_LEADIMAGE_ANNOTATION_KEY = 'collective.contentleadimage'

# Please note, templates in browser directory uses field name directly
IMAGE_FIELD_NAME = 'leadImage'
IMAGE_CAPTION_FIELD_NAME = 'leadImage_caption'

# All upload images will be scaled to this size. 
# Thumbnail will be created to value set in the preferences - (81,67) by default
IMAGE_SCALE_NAME = 'leadimage'
IMAGE_SCALE_SIZE = (81,67)

IMAGE_SIZES = {'large'   : (768, 768),
               'preview' : (400, 400),
               'mini'    : (200, 200),
               'thumb'   : (128, 128),
               'tile'    :  (64, 64),
               'icon'    :  (32, 32),
               'listing' :  (16, 16),
               }
