# color segment

from PIL import Image, ImageFont, ImageDraw
import numpy as np
import cv2
# from matplotlib import pyplot as plt
# import os

def get_empty_cv2(width, height, black=False):
    img_cv2 = np.zeros([height,width,3],dtype=np.uint8)
    if black:
        img_cv2.fill(0)
    else:
        img_cv2.fill(255)

    return img_cv2

# seg = [[x, y], [x, y], ...]
def seg(img, seg, thickness, color, alpha=None):

    if alpha is None:
        np_array = np.array(seg, np.int32)

        # seg_on = np.zeros_like(img, np.uint8)
        result = cv2.polylines(img, [np_array], True, color, thickness, lineType=cv2.LINE_AA)
    
    else:
        np_array = np.array(seg, np.int32)

        seg_on = np.zeros_like(img, np.uint8)
        cv2.fillPoly(seg_on, [np_array], color)

        result = img.copy()
        mask = seg_on.astype(bool)
        result[mask] = cv2.addWeighted(img, alpha, seg_on, 1-alpha, 1.0)[mask]

    return result

def bbox(img, tl, br, thickness, color):

    # seg_on = np.zeros_like(img, np.uint8)
    tl = (int(tl[0]), int(tl[1]))
    br = (int(br[0]), int(br[1]))
    result = cv2.rectangle(img, tl, br, color, thickness, lineType=cv2.LINE_AA)
    return result

def point(img, center, radius, thickness, color):

    # seg_on = np.zeros_like(img, np.uint8)
    center = (int(center[0]), int(center[1]))
    result = cv2.circle(img, center, radius, color, thickness, lineType=cv2.LINE_AA)
    return result

def place_image(bg_cv2, img_cv2, org):

    img_pil = Image.fromarray(img_cv2)
    bg_pil = Image.fromarray(bg_cv2)

    bg_pil.paste(img_pil, org)
    result_cv2 = np.array(bg_pil)

    return result_cv2

# seg = [[x, y], [x, y], ...]
def label(img, text, size, color, org, alpha):


    font = ImageFont.truetype('malgunbd.ttf', size)

    # labeling
    pil_img = Image.fromarray(img)
    draw = ImageDraw.Draw(pil_img)

    # size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 20, 10)
    text_bbox = draw.textbbox((0, 0), text, font=font)

    size = (int((text_bbox[2] - text_bbox[0])),
            int((text_bbox[3] - text_bbox[1]) * 1.5))
    if org[0] < 0:
        org = (0, org[1])
    if org[1] < 0:
        org = (org[0], 0)

    width, height = pil_img.size
    if org[0] + size[0] > width:
        org = (width - size[0], org[1])
    if org[1] + size[1] > height:
        org = (org[0], height - size[1])

    top_left = (int(org[0]), int(org[1]))
    bottom_right = (int(org[0] + size[0]), int(org[1] + size[1]))

    sub_img = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    white_rect = np.ones(sub_img.shape, dtype=np.uint8) *255
    result = cv2.addWeighted(sub_img, 1-alpha, white_rect, alpha, 1.0)

    img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] = result

    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)

    draw.text(top_left, text, color, font=font)
    result = np.array(img)

    return result

def gen_newline(line, width):
    length = width
    if len(line) > length:
        return_line = ''
        while line:
            try:
                return_line = return_line + line[:length] + '\n'
                line = line[length:]
            except:
                return_line = return_line + line
                line = ''
    
        return return_line

    return line

def gen_paragraph(line_list, width):
    
    return_str = ''
    for line in line_list:
        return_str += gen_newline(line, width) + '\n'

    return return_str

def paragraph(img_cv2, line_list, size, color, org, width):

    font = ImageFont.truetype('malgunbd.ttf', size)

    img_pil = Image.fromarray(img_cv2)
    img_draw = ImageDraw.Draw(img_pil)

    img_draw.text(org, gen_paragraph(line_list, width), color, font=font)

    img_cv2 = np.array(img_pil)

    return img_cv2