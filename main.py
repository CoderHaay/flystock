import paddle
from paddleocr import PaddleOCR, draw_ocr

from Database import Database
from PIL import Image
from paddleocr import PaddleOCR, draw_ocr

def baidu_ocr():
    ocr = PaddleOCR(use_angle_cls=True, lang="en", show_log=False,
                    use_gpu=True)  # need to run only once to download and load model into memory
    img_path = 'ppocr_img/dfcf_bak/000001_crop_1.jpg'
    # img_path = './ppocr_img/dfcf/img.png'
    # img_path = './ppocr_img/dfcf/img_2.png'
    # img_path = './ppocr_img/bad_imgs/000035-2.png'
    # img_path = './ppocr_img/bad_imgs/36.png'
    # img_path = './ppocr_img/bad_imgs/38.png'
    # img_path = './ppocr_img/bad_imgs/39.png'
    # img_path = './ppocr_img/bad_imgs/40.png'
    # img_path = './ppocr_img/bad_imgs/3.png'
    img_path = './ppocr_img/dfcf/1_3.png'
    # 单独使用识别：设置--det为false
    result = ocr.ocr(img_path, det=False)
    # print(result)
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            print(line)


def show_ocr():
    # Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
    # 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`
    ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=True, show_log=False)  # need to run only once to download and load model into memory
    img_path = './ppocr_img/ch/ch.jpg'
    img_path = './ppocr_img/dfcf/1_2.png'
    result = ocr.ocr(img_path, cls=True)
    for line in result:
        print(line)

    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='/path/to/PaddleOCR/doc/simfang.ttf')
    im_show = Image.fromarray(im_show)
    # im_show.save('./ppocr_img/result.jpg')
    im_show.show("123")


def db_mysql():
    # db = Database(host="127.0.0.1", user="fastudy", db_password="fastudy", db_name="fastudyDB")
    db = Database(host="127.0.0.1", user="fastudy", db_password="fastudy", db_name="flystock")
    # res = db.insert("fa_dfcf",{
    #     "code": "1",
    #     "date": "23-12-12",
    #     "ddy": 1.2,
    #     "ddx": 2.2,
    # })
    db.connect_check()
    # date = "2023-1-1"
    # code = "000001"
    # ddy = -0.302
    # ddz = -12.38
    # # sql = "INSERT INTO fa_dfcf (code, date, ddy, ddz) VALUES (%s, %s, %s, %s)", (code, date, ddy, ddz)
    #
    # sql = 'INSERT INTO hm_capital_day (CODE, DATE, DDY, DDZ) VALUES ("%s", "%s", %s, %s)' % (code, date, ddy, ddz)
    # print(sql)
    # db.insert_by_sql(sql)
    # # db.close()
def ocr_custom_infer():

    # Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
    # 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`
    ocr = PaddleOCR(use_angle_cls=True,
                    # rec_model_dir="./pretrain_models/myddz_best/",
                    lang="en",
                    use_gpu=True,
                    show_log=False)  # need to run only once to download and load model into memory

    img_path = './ppocr_img/dfcf/1_5.png'
    result = ocr.ocr(img_path, rec=True, cls=False, det=False)
    for line in result:
        print(line)
    # ('ddz:-0.799', 0.987205982208252)
    # ('66/ 0-IZPP', 0.759840726852417)
if __name__ == '__main__':
    # paddle.utils.run_check()
    # baidu_ocr()
    ocr_custom_infer()
    # show_ocr()
    # db_mysql()
