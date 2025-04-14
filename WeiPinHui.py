from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from lxml import etree
import time

driver = webdriver.Chrome()
driver.maximize_window()

def get_info(url, page):
    page = page + 1
    driver.get(url)
    driver.implicitly_wait(10)
    selector = etree.HTML(driver.page_source)
    infos = selector.xpath('//*[@id="J_goodsList"]/ul/li')  # 修改：确保正确找到商品列表
    for info in infos:
        price = info.xpath('div/div[3]/strong/i/text()')
        shop = info.xpath('div/div[7]/span/a/text()')
        if price and shop:
            print("价格:", price[0].strip() if price else "无价格")
            print("商店:", shop[0].strip() if shop else "无商店")
        print('-' * 20)

    if page < 5:  # 控制抓取页数
        NextPage(url, page)
    else:
        print("已抓取 5 页数据，停止！")
        driver.quit()


def NextPage(url, page):
    # 这里我们可以通过显式等待来确保翻页按钮被加载
    driver.get(url)
    driver.implicitly_wait(10)
    # 修改：点击分页按钮
    next_button = driver.find_element(By.XPATH, '//*[@id="J_bottomPage"]/span/a[3]')  # 这里是“下一页”按钮
    next_button.click()
    time.sleep(3)  # 等待页面加载
    driver.get(driver.current_url)
    driver.implicitly_wait(10)
    get_info(driver.current_url, page)


if __name__ == '__main__':
    page = 1
    url = 'https://search.jd.com/Search?keyword=手机&enc=utf-8'
    driver.get(url)
    driver.implicitly_wait(10)

    # 搜索框输入
    search_box = driver.find_element(By.ID, 'key')
    search_box.clear()
    search_box.send_keys('CD6404-104')  # 搜索关键词
    search_box.send_keys(Keys.RETURN)  # 使用回车键模拟点击搜索按钮
    time.sleep(3)  # 等待页面加载
    get_info(driver.current_url, page)
