# coding = utf-8
# Author = zhaoge
# Date: 2021/6/26 10:36 上午

# from lib.ShowapiRequest import ShowapiRequest
#
# r = ShowapiRequest("http://route.showapi.com/184-4","272526","a924d4e982ae404b8a068b4d1c7784f2" )
# r.addFilePara("image", "test.png")
# r.addBodyPara("typeId", "34")
# r.addBodyPara("convert_to_jpg", "0")
# r.addBodyPara("needMorePrecise", "0")
# res = r.post()
# print(res.text) # 返回信息
from PIL import Image
from pytesseract import pytesseract
# from selenium import webdriver
# from utility_module import get_code_img_path,identify_cerification_code_by_ocr
# from utility_module import identify_verification_code_by_BaiduAI
#
# driver = webdriver.Chrome()
# driver.get("http://localhost:8080/jpress/user/register")
# driver.maximize_window()
# # get_code_img_path(driver,"captcha-img")
# identify_cerification_code_by_ocr(driver,"captcha-img")
# # identify_verification_code_by_BaiduAI(driver,"captcha-img")
# driver.quit()


from selenium import webdriver
from utility_module import identify_verification_code_by_ttshitu

driver = webdriver.Chrome()
driver.get("http://localhost:8080/jpress/user/register")
driver.maximize_window()
print(identify_verification_code_by_ttshitu(driver, "captcha-img"))
driver.quit()

