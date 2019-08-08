from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
import os

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://'+staging_server
        
#    def tearDown(self):
#        self.browser.quit()
    
    def wait_for_row_in_list_table(self,row_text):
        start_time  = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text,[row.text for row in rows])
                return 
            except (AssertionError,WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT :
                    raise e
                time.sleep(0.5)
    def test_layout_and_styling(self):
        #伊迪斯访问首页，看到了输入框居中表示
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)
        
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] /2,
            512,
            delta = 10
        )
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta = 10
        )
    def test_can_start_a_list_and_retrieve_it_later(self):
        

        #伊迪丝听说
        #她去看了

        self.browser.get(self.live_server_url)
        #她注意到网页“To-Do"
        
        self.assertIn('To-Do',self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)
        #应用邀请她输入一个待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        #self.fail("finishi the test.")
        



#她输入了“购买孔雀羽毛”
#她的爱好是用假蝇钓鱼

        inputbox.send_keys('Buy peacock feathers')
#她按了回车键后，页面更新了
#待办事项显示“购买了孔雀羽毛”
        inputbox.send_keys(Keys.ENTER)
        #time.sleep(1)        
        self.wait_for_row_in_list_table('1:Buy peacock feathers')
        '''
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        #print(raws)
        self.assertTrue(
            any(row.text == '1:Buy peacock feathers' for row in rows),
            f"new to-do item did not appear in table.Contents were:\n{table.text}"
        )
        '''
#页面中有显示了一个文本框
#她输入了“使用羽毛做假蝇"
#她做事很有条理
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        #time.sleep(1)
#页面再次更新
#清单中显示了两个待办事项
        '''`
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1:Buy peacock feathers',[row.text for row in rows])
        self.assertIn('2:Use peacock feathers to make a fly',[row.text for row in rows])
        '''
        self.wait_for_row_in_list_table('1:Buy peacock feathers')
        self.wait_for_row_in_list_table('2:Use peacock feathers to make a fly')
#伊迪丝想知道这个网站是否会记住她的清单
#她看到网站为她生成了一个唯一的URL
#而且页面中有一些文字解释了这个功能
#她访问了那个URL
#她很满意，她去睡觉了
    def test_mutiple_user_can_start_lists_at_diff_urls(self):
#伊迪斯新建一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy peacock feathers')
#她注意到清单唯一url
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url , '/lists/.+')
#现在另一名弗朗西斯新用户访问了网站

##我们是用新的浏览器会话
##确保伊迪斯的信息不会泄露出去
        self.browser.quit()
        self.browser = webdriver.Firefox()
#弗朗西斯访问首页
#页面中不会看到伊迪斯的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertNotIn('make a fly' , page_text)
#他输入一个待办事项，建立一个清单
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy milk')
    
#他获得唯一的url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url , 'lists/.+')
        self.assertNotEqual(francis_list_url,edith_list_url)
#这个页面还是没有伊迪斯的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertIn('Buy milk' , page_text)
#他们都很满意，所以都去睡觉了        
        #self.fail('finish the rest')
if __name__ == '__main__':
    unittest.main(warnings = 'ignore')