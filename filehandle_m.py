import os
from pathlib import Path
import shutil

import cv2
import json
import numpy as np
import pandas as pd

import logging
import traceback

try:
    import xmltodict
except:
    os.system('pip install xmltodict')
    import xmltodict


def create_file_dict(data_dir, ext):
    file_dict = {}
    for (root, _, files) in os.walk(data_dir):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix == ext:
                file_dict[file_path.stem] = file_path
    return file_dict

def create_image_dict(data_dir, ext):
    file_dict = {}
    for (root, _, files) in os.walk(data_dir):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix in ext:
                file_dict[file_path.stem] = file_path
    return file_dict

def create_file_list(data_dir, ext):
    file_list = []
    for (root, _, files) in os.walk(data_dir):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix == ext:
                file_list.append(file_path)
    return file_list

def read_json(json_path):
    with open(json_path, encoding='utf-8') as f:
        json_data = json.load(f)
    return json_data

def read_csv(csv_path):
    csv_data = pd.read_csv(csv_path, encoding='euc-kr', dtype=str)
    return csv_data

def read_excel(excel_path):
    excel_data = pd.read_excel(excel_path, dtype=str)
    return excel_data

def read_xml(xml_path):
    with open(xml_path, 'r', encoding='utf-8', errors='ignore') as f:
        xml_data = f.read()
    xml_dict = xmltodict.parse(xml_data)
    return xml_dict

def read_txt(txt_path):
    with open(txt_path, encoding='utf-8-sig') as f:
        lines = f.readlines()
    return lines

def read_image(image_path):
    image_array = np.fromfile(image_path, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image

def save_image(image_path, save_dir, image):
    save_path = Path(save_dir) / image_path.name
    os.makedirs(save_path.parent, exist_ok=True) # 저장 디렉토리가 존재하지 않는 경우 생성
    
    result, encoded_img = cv2.imencode(image_path.suffix, image)
    if result:
        with open(save_path, mode='w+b') as f:
            encoded_img.tofile(f)

def save_image_foldertree(image_path, save_dir, new_file_dir, image):
    save_dir = Path(save_dir) / new_file_dir
    os.makedirs(save_dir, exist_ok=True)
    file_name = image_path.name
    save_path = save_dir / file_name
    result, encoded_img = cv2.imencode(image_path.suffix, image)
    if result:
        with open(save_path, mode='w+b') as f:
            encoded_img.tofile(f)

def write_excel(save_dir, file_name, df_list):
    if df_list:
        df = pd.concat(df_list)
        save_path = Path(save_dir) / file_name
        df.to_excel(save_path, index=False)

def write_csv(save_dir, file_name, df_list):
    if df_list:
        df = pd.concat(df_list)
        save_path = Path(save_dir) / file_name
        df.to_csv(save_path, index=False, encoding='utf-8-sig')

def write_json(json_save_path, output_json, indent=4):
    with open(json_save_path, 'w', encoding='utf-8') as f:
        json.dump(output_json, f, indent=indent, ensure_ascii=False)

def write_txt(txt_save_path, txt_data):
    with open(txt_save_path, 'w', encoding='utf-8-sig') as f:
        f.writelines(txt_data)

def write_xml(xml_save_path, xml_data, indent='  '):
    with open(xml_save_path, 'w', encoding='utf-8-sig') as f:
        f.write(xmltodict.unparse(xml_data, indent=indent, pretty=True))

def make_logger(out_path):
    logger = logging.getLogger()

    if len(logger.handlers) > 0:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('\n%(filename)s:%(lineno)d|[%(asctime)s]\n-------------------------\n%(message)s\n-------------------------\n')

    file_handler = logging.FileHandler(out_path, encoding='utf-8', mode='w')
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

def close_logger(logger, log_file_path):
    if logger is None:
        return
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)

    if os.path.getsize(log_file_path) == 0:
        os.remove(log_file_path)

def get_polygon_iou(polygon1, polygon2):
    if polygon1.intersects(polygon2): 
        intersect = polygon1.intersection(polygon2).area
        union = polygon1.union(polygon2).area
        return intersect / union
    return 0

def get_bbox_iou(pred_box, gt_box):
    ixmin = max(pred_box[0], gt_box[0])
    ixmax = min(pred_box[2], gt_box[2])
    iymin = max(pred_box[1], gt_box[1])
    iymax = min(pred_box[3], gt_box[3])

    iw = np.maximum(ixmax-ixmin+1., 0.)
    ih = np.maximum(iymax-iymin+1., 0.)

    inters = iw * ih

    uni = ((pred_box[2] - pred_box[0]+1.) * (pred_box[3] - pred_box[1]+1.) +
           (gt_box[2] - gt_box[0] + 1.) * (gt_box[3] - gt_box[1] + 1.) - inters)

    iou = inters / uni
    return iou

def copy_file(logger, ori_file_path, new_file_path):
    try:
        shutil.copy2(src=ori_file_path, dst=new_file_path)
    except:
        logger.error(f'Failed {ori_file_path} copy to {new_file_path}\n\n{traceback.format_exc()}')