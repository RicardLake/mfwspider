from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse
import re
import pymysql.cursors
import time




def get_url():
    #保存每个景点的链接
    fp = open("./href.txt", 'a')
    chromeOptions = webdriver.ChromeOptions()
    #创建浏览器对象
    driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    #获取首页内容
    driver.get("http://www.mafengwo.cn/jd/21536/gonglve.html")
    #获得首页的每个景点的url
    hrefs = driver.find_elements_by_xpath('//ul[@class="scenic-list clearfix"]//li//a')
    for href in hrefs:
        poi_url = str(href.get_attribute("href"))
        fp.write(poi_url+"\n")
    #获取景点列表页总页数
    page_num = int(driver.find_element_by_xpath("//span[@class='count']//span[1]").text)
    # 通过浏览器翻页，获取每一页的景点url
    for i in range(page_num-1):
        driver.find_element_by_xpath(u"//div[@class='m-pagination']//a[@title='后一页']").click()
        #通过设置延时，使得浏览器有充足的时间等待翻页后的js渲染完成，以防获取不到信息
        time.sleep(3)
        hrefs = driver.find_elements_by_xpath('//ul[@class="scenic-list clearfix"]//li//a')
        for href in hrefs:
            poi_url = str(href.get_attribute("href"))
            fp.write(poi_url + "\n")
    driver.quit()
    fp.close()
def test():


    # 连接数据库
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='153076',
        db='test',
        charset='utf8'
    )

    # 获取游标
    cursor = connect.cursor()

    # 插入数据
    sql = "INSERT INTO trade (city) VALUES ( '%s' )"
    data = ('雷军')
    cursor.execute(sql % data)
    connect.commit()
    print('成功插入', cursor.rowcount, '条数据')

def test2():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',
                              chrome_options=chrome_options)
    url='http://www.mafengwo.cn/poi/5515392.html'
    driver.get(url)
    b=''

    print(b)
    driver.close()

def test3():
    fr = open(r"D:\PyCharm\maatt\mafengwoatt\mafengwoatt/href.txt")
    urls=list()
    for i in fr.readlines():
        urls.append(i.strip())
    print(urls[47955])
if __name__ =="__main__":
    url = 'http://www.mafengwo.cn/jd/21536/gonglve.html'
    test3()