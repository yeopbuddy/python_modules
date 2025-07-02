# python_modules

`python_modules`는 파이썬 프로젝트에서 공통적으로 사용되는 유틸리티 함수들을 모아놓은 저장소입니다. 파일 처리, 이미지 시각화 등 다양한 작업을 위한 모듈을 제공합니다.

## 포함된 모듈

### `filehandle_m.py`

이 모듈은 파일 시스템 작업을 위한 다양한 함수를 제공합니다.

#### 기능:

* **파일 및 디렉토리 탐색:**
    * `create_file_dict(data_dir, ext)`: 지정된 디렉토리에서 특정 확장자를 가진 파일들의 사전(키: 파일 이름, 값: 파일 경로)을 생성합니다.
    * `create_image_dict(data_dir, ext)`: 지정된 디렉토리에서 특정 이미지 확장자를 가진 파일들의 사전(키: 파일 이름, 값: 파일 경로)을 생성합니다.
    * `create_file_list(data_dir, ext)`: 지정된 디렉토리에서 특정 확장자를 가진 파일들의 리스트를 생성합니다.
* **파일 읽기:**
    * `read_json(json_path)`: JSON 파일을 읽어 Python 객체로 반환합니다.
    * `read_csv(csv_path)`: CSV 파일을 읽어 pandas DataFrame으로 반환합니다 (EUC-KR 인코딩).
    * `read_excel(excel_path)`: Excel 파일을 읽어 pandas DataFrame으로 반환합니다.
    * `read_xml(xml_path)`: XML 파일을 읽어 Python 사전으로 반환합니다.
    * `read_txt(txt_path)`: 텍스트 파일을 읽어 각 줄을 리스트 요소로 반환합니다.
    * `read_image(image_path)`: 이미지 파일을 읽어 OpenCV(cv2) 이미지 배열로 반환합니다.
* **파일 저장:**
    * `save_image(image_path, save_dir, image)`: 이미지를 지정된 디렉토리에 저장합니다.
    * `save_image_foldertree(image_path, save_dir, new_file_dir, image)`: 이미지를 지정된 디렉토리 내의 새로운 하위 디렉토리에 저장합니다.
    * `write_excel(save_dir, file_name, df_list)`: pandas DataFrame 리스트를 병합하여 Excel 파일로 저장합니다.
    * `write_csv(save_dir, file_name, df_list)`: pandas DataFrame 리스트를 병합하여 CSV 파일로 저장합니다 (UTF-8-SIG 인코딩).
    * `write_json(json_save_path, output_json, indent=4)`: Python 객체를 JSON 파일로 저장합니다.
    * `write_txt(txt_save_path, txt_data)`: 텍스트 데이터를 TXT 파일로 저장합니다.
    * `write_xml(xml_save_path, xml_data, indent=' ')`: Python 사전을 XML 파일로 저장합니다.
* **유틸리티:**
    * `make_logger(out_path)`: 로그 파일을 생성하고 설정합니다.
    * `close_logger(logger, log_file_path)`: 로거를 닫고, 빈 로그 파일은 삭제합니다.
    * `get_polygon_iou(polygon1, polygon2)`: 두 폴리곤 간의 IoU(Intersection over Union)를 계산합니다.
    * `get_bbox_iou(pred_box, gt_box)`: 두 바운딩 박스 간의 IoU를 계산합니다.
    * `copy_file(logger, ori_file_path, new_file_path)`: 파일을 복사하고 실패 시 로깅합니다.

### `visualization_m.py`

이 모듈은 이미지에 주석을 달고 시각화하는 데 유용한 함수를 제공합니다. OpenCV와 Pillow 라이브러리를 활용합니다.

#### 기능:

* **기본 이미지 생성:**
    * `get_empty_cv2(width, height, black=False)`: 지정된 크기의 빈 OpenCV 이미지(흰색 또는 검은색)를 생성합니다.
* **그리기 함수:**
    * `seg(img, seg, thickness, color, alpha=None)`: 이미지에 폴리곤 세그멘테이션을 그립니다. 선택적으로 투명도를 적용할 수 있습니다.
    * `bbox(img, tl, br, thickness, color)`: 이미지에 바운딩 박스를 그립니다.
    * `point(img, center, radius, thickness, color)`: 이미지에 원형 포인트를 그립니다.
* **이미지 합성:**
    * `place_image(bg_cv2, img_cv2, org)`: 배경 이미지 위에 다른 이미지를 지정된 위치에 배치합니다.
* **텍스트 추가:**
    * `label(img, text, size, color, org, alpha)`: 이미지에 텍스트 레이블을 추가합니다. 배경에 투명도를 적용할 수 있습니다. (한글 폰트 `malgunbd.ttf` 필요)
    * `gen_newline(line, width)`: 긴 텍스트 줄을 지정된 너비에 맞춰 여러 줄로 나눕니다.
    * `gen_paragraph(line_list, width)`: 텍스트 줄 리스트를 단락으로 포맷팅합니다.
    * `paragraph(img_cv2, line_list, size, color, org, width)`: 이미지에 단락 텍스트를 추가합니다. (한글 폰트 `malgunbd.ttf` 필요)

## 설치

이 모듈들을 사용하려면 다음 라이브러리들이 설치되어 있어야 합니다:

```bash
pip install opencv-python pandas xmltodict Pillow numpy