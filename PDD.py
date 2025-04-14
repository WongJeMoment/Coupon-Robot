import uiautomator2 as u2
import time

d = u2.connect()  # connect to device
print(d.info)

class PDD:
    def __init__(self, shop, devices, account):
        """
        初始化PDD类，连接到设备并设置店铺名称。

        :param shop: 店铺名称
        :param devices: 设备的IP地址或序列号
        :param account: 要获取的商品数量
        """
        self.shop_name = shop
        self.device = devices  # 连接上手机并返回给 device
        self.account = account

    def _search(self):
        """
        在设备上执行搜索操作。
        """
        self.device(resourceId='com.xunmeng.pinduoduo:id/pdd').click()
        # self.device.send_keys(self.shop_name)
        self.device(text='搜索').click()
        time.sleep(1)

    def _slide(self):
        """
        滑动浏览页面，并获取符合条件的商品详细信息。
        """
        temp_account = 0
        recent_elements = []
        while 1:
            elems = self.device.xpath('//*[contains(@text, "¥")]/following-sibling::*[1]').all()
            for elem in elems:
                if elem.text and elem.text not in recent_elements:
                    if len(recent_elements) >= 3:
                        recent_elements.pop(0)  # 移除最早添加的元素
                    recent_elements.append(elem.text)
                    elem.click()
                    # 操作
                    self.get_detail()
                    # 返回到上一级页面
                    self.device.xpath(
                        '//*[@content-desc="顶部工具栏"]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]').click()
                if temp_account > self.account:
                    return recent_elements
                print(recent_elements)
                temp_account += 1  # 将该行移动到这里，确保每次处理都会增加计数器
            self.device.swipe_ext("up", 0.5)
            print('next')
            time.sleep(3)

    def get_detail(self):
        """
        获取商品的详细信息，包括价格、标题和店名。

        :return: 包含商品详细信息的字典
        """
        detail = {}
        # 获取价格
        price = ''
        price_elements = self.device.xpath(
            '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[2]').child(
            '//*').all()
        for elem in price_elements:
            if elem.text:
                price += elem.text
        detail['price'] = price

        # 获取标题
        title_elements = self.device.xpath(
            '//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[3]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]').child(
            '//android.widget.TextView').all()
        real_title = ''.join([elem.text for elem in title_elements if elem.text])
        detail['real_title'] = real_title

        # 向上滑动页面以获取更多内容
        self.device.swipe_ext("up", 1)

        # 获取店名
        store = ''
        store_name_elements = self.device.xpath(
            '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.support.v7.widget.RecyclerView[1]').child(
            '//*').all()
        for elem in store_name_elements:
            if '专营店' in elem.text or '旗舰店' in elem.text:
                store = elem.text
        detail['store'] = store
        return detail


def main():
    # 示例参数，可根据需要修改
    shop_name = "官方旗舰店"  # 要搜索的店铺名
    product_limit = 20  # 要抓取的商品数量

    # 创建 PDD 对象
    crawler = PDD(shop=shop_name, devices=d, account=product_limit)

    print("开始搜索店铺并抓取商品信息...")

    # 搜索店铺
    crawler._search()  # 调用单下划线方法

    # 开始滑动并抓取数据
    result = crawler._slide()  # 调用单下划线方法

    # 输出抓取结果
    print("\n抓取完成，商品信息如下：")
    for i, item in enumerate(result):
        print(f"{i + 1}. 商品名：{item}")


if __name__ == "__main__":
    main()