# coding = utf-8
# Author = zhaoge
# Date: 2021/6/24 10:31 上午

import os
import pickle
import random
import string
from selenium.webdriver.common.by import By
from time import sleep,strftime,localtime,time
from lib.ShowapiRequest import ShowapiRequest
from PIL import Image
import pytesseract
from lib.baidu_api_sdk.aip import AipOcr
import requests
import base64
import json


def screenshot(driver):
    """
    截图方法，将截屏的图保存到相应目录
    :param driver: WebDriver实例
    :return:
    """
    st = strftime("%Y-%m-%d %H-%M-%S",localtime(time()))
    file_name = st + '.png'
    path = os.path.abspath("../screenshot")
    img_path = path + '/' + file_name
    driver.get_screenshot_as_file(img_path)
    return img_path

def get_code_img_path(driver,id):
    """
    验证码识别方法
    :param driver: WebDriver实例
    :param id: 验证码id属性
    :return:
    """
    '''driver传入screenshot获取整个页面截图，返回截图路径'''
    img_path = screenshot(driver)
    '''定位到验证码'''
    code_location = driver.find_element(By.ID,id)
    '''获取定位到的验证码的左定点坐标'''
    left = code_location.location['x']
    top = code_location.location['y']
    '''获取验证码右底点坐标'''
    right = code_location.size['width'] + left
    height = code_location.size['height'] + top
    '''获取当前屏幕缩放比率系数，在后面抠图的时候传入'''
    dpr = driver.execute_script('return window.devicePixelRatio')
    '''打开前面整张截图文件，这里用到的是PILLOW图像包，需要安装PILLOW包，然后从PIL里导入Image'''
    im = Image.open(img_path)
    '''抠图，里面抠的位置是左定点坐标到右底点，然后都需要乘以当前屏幕分辨率的缩放系数dpr'''
    code_img = im.crop((left*dpr,top*dpr,right*dpr,height*dpr))
    st = strftime("%Y-%m-%d %H-%M-%S",localtime(time()))
    path = os.path.abspath("../screenshot")
    code_img_path = path + '/' + st + 'code.png'
    '''将抠出的图片按照处理的路径保存'''
    code_img.save(code_img_path)
    return code_img_path

def binary_image(driver,id):
    code_img_path = get_code_img_path(driver, id)
    code_image = Image.open(code_img_path)
    code_image = code_image.convert('L')
    threshold = 150
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    code_image = code_image.point(table, "1")
    code_image.show()
    st = strftime("%Y-%m-%d %H-%M-%S", localtime(time()))
    path = os.path.abspath("../screenshot")
    binary_img_path = path + '/' + st + 'binary_code.png'
    code_image.save(binary_img_path)
    return binary_img_path


def identify_verification_code_by_ocr(driver,id):
    code_img_path = get_code_img_path(driver,id)
    code_image = Image.open(code_img_path)
    code_image = code_image.convert('L')
    threshold=150
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    code_image=code_image.point(table,"1")
    # code_image.show()
    cerification_code = pytesseract.image_to_string(code_image)
    return cerification_code

def identify_verification_code_by_ShowAI(driver,id):
    code_img_path = get_code_img_path(driver, id)
    '''调用第三方验证码识别AI的接口，将保存的验证码图片传进去，然后处理一下接口返回的数据，返回识别出的验证码'''
    r = ShowapiRequest("http://route.showapi.com/184-4","272526","a924d4e982ae404b8a068b4d1c7784f2" )
    r.addFilePara("image", code_img_path)
    r.addBodyPara("typeId", "34")
    r.addBodyPara("convert_to_jpg", "0")
    r.addBodyPara("needMorePrecise", "0")
    res = r.post()
    text = res.json()['showapi_res_body']
    code = text['Result']
    return code

def identify_verification_code_by_BaiduAI(driver,id):
    """ 你的 APPID AK SK """
    APP_ID = '24445779'
    API_KEY = 'PnETgMU07BqkyWnm5PZRS52y'
    SECRET_KEY = 'e0seGaCUG31NK2YtgfUNUcNYNz4IX4tu'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    code_img_path = get_code_img_path(driver, id)
    def get_file_content(filePath):
        with open(filePath,'rb') as fp:
            return fp.read()
    code_image = get_file_content(code_img_path)
    options={}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"
    print(client.basicGeneral(code_image))

def identify_verification_code_by_ttshitu(driver,id):
    code_img_path = binary_image(driver, id)
    def base64_api(img):
        with open(img, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            b64 = base64_data.decode()
            return b64
    b64 = base64_api(code_img_path)
    data = {"username": 'zhaoge555', "password": 'zhaoge555', "typeid": 3, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]


def random_string(lenth=8):
    """
    随机字符串生成方法，默认生成8位字符串,字母数字组合
    :param lenth: int类型，默认8位
    :return:
    """
    rand_str = ''.join(random.sample(string.ascii_letters + string.digits,lenth))
    return rand_str

def save_cookie(driver,path):
    with open(path,'wb') as filehandler:
        cookies = driver.get_cookies()
        print(cookies)
        pickle.dump(cookies,filehandler)

def load_cookie(driver,path):
    with open(path,'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)



