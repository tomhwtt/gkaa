from PIL import Image

def resize_image(img,desired_size):

    img_copy = img.copy()

    # set the image_copy height and width
    img_width, img_height = img_copy.size

    # which side is the biggest (width or height)
    # not currently used
    max_side = max(img_copy.size)

    # which side is the smallest (width or height)
    min_side = min(img_copy.size)

    # calculate the resize percent
    resize_percent = desired_size / min_side

    # set the new resize width and height
    resize_width = int(img_width * resize_percent)
    resize_height = int(img_height * resize_percent)

    # resize the image
    img_copy = img_copy.resize(
        (resize_width, resize_height),
        Image.ANTIALIAS
        )

    # set the new image's width and height
    img_width, img_height = img_copy.size

    # if the image is wider than the desired_size
    # crop the width
    if img_width > desired_size:

        # get the left side
        left_side = round(((img_width - desired_size)/2))

        # set the crop sizes
        left = left_side
        top = 0
        right = left_side + desired_size #left + desired_size
        bottom = desired_size

    # if the image is taller than the desired_size
    # crop the height
    elif img_height > desired_size:

        # set the top side
        top_side = round(((img_height - desired_size)/2))

        # set the crop sizes
        left = 0
        top = top_side
        right = desired_size
        bottom = top_side + desired_size

    # crop the image to the desired_size
    img_copy = img_copy.crop((left,top,right,bottom))

    # return the image
    return img_copy
