#Created by IrisLee on 2017/10/03
#Modify for HTMLTestRunner report on 2017/10/10


# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from HTMLTestRunner import HTMLTestRunner
import unittest, time, re, datetime



MyWebDrive = webdriver.Firefox()

class KKBOXTestCase(unittest.TestCase):
    def setUp(self):
        print('setUp')
        self.driver = MyWebDrive
        self.driver.implicitly_wait(30),
        self.base_url = "https://play.kkbox.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_login(self):
        '''測試:登入'''
        print('test_login')
        driver = self.driver
        driver.get(self.base_url + "")
        driver.find_element_by_id("uid").clear()
        driver.find_element_by_id("uid").send_keys("vdotn22@gmail.com")
        driver.find_element_by_id("pwd").clear()
        driver.find_element_by_id("pwd").send_keys("iris1234")
        driver.find_element_by_id("login-btn").click()
        time.sleep(5)
        driver.find_element_by_class_name("sidebar-nav")
        assert "我的音樂庫" in driver.page_source
        assert "線上精選" in driver.page_source
        assert "電台" in driver.page_source
        assert "一起聽" in driver.page_source

    def test_search(self):
        '''測試:關鍵字_清平調'''
        print('test_search')
        driver = self.driver
        driver.find_element_by_xpath("//input[@value='']").click()
        driver.find_element_by_xpath("//input[@value='']").clear()
        driver.find_element_by_xpath("//input[@value='']").send_keys(u"清平調")
        driver.find_element_by_id("search_btn_cnt").click()
        time.sleep(5)
        searchResult = driver.find_element_by_link_text(u"王菲&鄧麗君 (Faye Wong & Teresa Teng)").text
        assert "王菲&鄧麗君 (Faye Wong & Teresa Teng)" in searchResult


    def test_dislike(self):
        '''測試:電台_dislike按鈕'''
        print('test_dislike')
        driver = self.driver
        driver.find_element_by_link_text(u"電台").click()
        time.sleep(10)
        above = driver.find_element_by_xpath("//*[@id='promote-stations']/div/ul/li[1]/div/div[1]/a/img")
        ActionChains(driver).move_to_element(above).perform()
        driver.find_element_by_xpath("//*[@id='promote-stations']/div/ul/li[1]/div/div[1]/div/a").click()
        time.sleep(2)

        #若有重複播放提示時,同意切換裝置播放
        self.is_alert_present()
        time.sleep(5)

        song1 = driver.find_element_by_xpath("//*[@id='container']/div[2]/div/div[1]/div/div/div/div[1]/div/div/div/h3/a").text
        time.sleep(5)
        driver.find_element_by_xpath("//*[@id='container']/div[2]/div/div[1]/div/div/div/div[1]/div/div/div/div[2]/a[1]/i").click()
        time.sleep(5)
        song2 = driver.find_element_by_xpath("//*[@id='container']/div[2]/div/div[1]/div/div/div/div[1]/div/div/div/h3/a").text

        #將播放的歌名儲存
        log_path = ('./Report/')
        wfile = open(log_path + 'songList.txt','w')
        wfile.write('1.'+ song1 + '\n' + '2.' + song2)
        wfile.close()
        assert song1 != song2



    def test_logout(self):
        '''測試:登出_關Browser'''
        print('test_logout')
        driver = self.driver
        user_dropdown = driver.find_element_by_xpath("//*[@id='container']/header/div[2]/a/i")
        user_dropdown.click()
        ActionChains(driver).move_to_element(user_dropdown).perform()
        driver.find_element_by_xpath("//*[@id='container']/header/div[2]/ul/li[5]/a").click()
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)



    def is_alert_present(self):
        try:
            print('is_alert_present')
            self.driver.switch_to_alert().accept()
        except:
            pass



if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(KKBOXTestCase('test_login'))
    suite.addTest(KKBOXTestCase('test_search'))
    suite.addTest(KKBOXTestCase('test_dislike'))
    suite.addTest(KKBOXTestCase('test_logout'))
    report_path = ('./Report/')
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
    fp = open( report_path + st + '.html', 'wb')
    runner = HTMLTestRunner(stream = fp, title = u'自動化測試結果', description = u'案例執行情況')
    runner.run(suite)



