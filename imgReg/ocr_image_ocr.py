import os
from fnmatch import fnmatch
import ddddocr


def image_reg():
    ocr = ddddocr.DdddOcr(show_ad=False)
    filedir = './imgReg/easy_img/img_to_reg.jpg'
    with open(filedir, 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    return res


def main():
    ocr = ddddocr.DdddOcr(show_ad=False)
    filedir = './easy_img'
    for file in os.listdir(filedir):
        if fnmatch(file, '*.*'):
            with open('./easy_img/%s' % file, 'rb') as f:
                img_bytes = f.read()
            res = ocr.classification(img_bytes)
            print('识别为：%s' % res)


if __name__ == '__main__':
    main()
