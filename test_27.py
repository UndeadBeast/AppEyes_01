#!/usr/bin/env python -tt
# -*- coding:  utf-8 -*-
import ConfigParser
from selenium import webdriver
from applitools.eyes import Eyes, BatchInfo

# This is your api key, make sure you use it in all your tests.
Eyes.api_key = '3Z1sOfalzP1QClQrzmHJaU5BbKiR0AFZlDsBPoVB3Uk110'
eyes = Eyes()
batch = BatchInfo("BackYard batch test")
eyes.batch = batch

# Read configs from file
configParser = ConfigParser.RawConfigParser()
configFilePath = r'config.cfg'
configParser.read(configFilePath)
baseurl = configParser.get('common', 'baseurl')
username = configParser.get('common', 'admin')
password = configParser.get('common', 'password')
accountNameSearch = configParser.get('common', 'accountNameSearch')

# assign xPath variables for web-forms under test
xpaths = {'usernameTxtBox': "//input[@name='username']",
          'passwordTxtBox': "//input[@name='password']",
          'submitButton': "/html/body/div/form/div/div[1]/button",
          'DashBoard_bckWOWPMain': "/html/body/div[1]/div/div[2]/div/ul/li[5]/a",
          'bckWOWP_accountsPage': "/html/body/div[3]/div[16]/div/div[1]/ul/li[1]/a",
          'bckWOWP_accounts_searchType': "/html/body/div[3]/div[17]/div/div/div/form/div[1]/fieldset[1]/div/select/" +
                                         "option[4]",
          'bckWOWP_accounts_searchValue': "/html/body/div[3]/div[17]/div/div/div/form/div[1]/fieldset[1]/div/input",
          'bckWOWP_accounts_searchStart': "/html/body/div[3]/div[17]/div/div/div/form/div[2]/button",
          'bckWOWP_accounts_firstLink': "/html/body/div[3]/div[17]/div/div/form/div[2]/table/tbody/tr/td[6]/a",
          'bckWOWP_account_gold': "/html/body/div[3]/div[17]/div/table[3]/tbody/tr[11]/td/a",
          'bckWOWP_gold_amount': "/html/body/div[3]/div[17]/div/form/fieldset/div[1]/div/input",
          'bckWOWP_gold_comment': "/html/body/div[3]/div[17]/div/form/fieldset/div[7]/div/div/textarea",
          'bckWOWP_gold_submit': "/html/body/div[3]/div[17]/div/form/div/input"
}

# Get a selenium web driver object.
driver = webdriver.Firefox()

try:
    # Array of resolutions to test. Example : viewSizeArray = [[width, height],[...]...]
    # viewSizeArray = [[1920, 1080], [1600, 1200], [1280, 1024], [1024, 768], [800, 600]]
    viewSizeArray = [[1024, 768]]

    for viewSize in viewSizeArray:
        viewSizeForAppliTools = {'width': viewSize[0], 'height': viewSize[1]}
        driver = eyes.open(driver=driver,
                           app_name='Applitools',
                           test_name='Basic Backyard test: resolution - ' + str(viewSize[0]) + 'x' + str(viewSize[1]),
                           viewport_size=viewSizeForAppliTools)
        driver.get(baseurl)
        eyes.check_window('Login page')
        # driver.maximize_window()
        # Clear Username, Password TextBoxs if already allowed "Remember Me". Fill with new values. Sign in
        driver.find_element_by_xpath(xpaths['usernameTxtBox']).clear()
        driver.find_element_by_xpath(xpaths['usernameTxtBox']).send_keys(username)
        driver.find_element_by_xpath(xpaths['passwordTxtBox']).clear()
        driver.find_element_by_xpath(xpaths['passwordTxtBox']).send_keys(password)
        driver.find_element_by_xpath(xpaths['submitButton']).click()
        eyes.check_window('Dashboard main')

        # Go to WOWP backyard
        driver.find_element_by_xpath(xpaths['DashBoard_bckWOWPMain']).click()
        eyes.check_window('Dashboard WOWP')

        # Go to account
        driver.find_element_by_xpath(xpaths['bckWOWP_accountsPage']).click()
        driver.find_element_by_xpath(xpaths['bckWOWP_accounts_searchType']).click()
        driver.find_element_by_xpath(xpaths['bckWOWP_accounts_searchValue']).send_keys(accountNameSearch)
        driver.find_element_by_xpath(xpaths['bckWOWP_accounts_searchStart']).click()
        eyes.check_window('Accounts. Some value found')
        driver.find_element_by_xpath(xpaths['bckWOWP_accounts_firstLink']).click()
        eyes.check_window('Account. Manage WOWP page')

        # Some Account check
        driver.find_element_by_xpath(xpaths['bckWOWP_account_gold']).click()
        eyes.check_window('Gold. Manage gold of user')
        driver.find_element_by_xpath(xpaths['bckWOWP_gold_amount']).send_keys(password)
        driver.find_element_by_xpath(xpaths['bckWOWP_gold_comment']).send_keys(password)
        driver.find_element_by_xpath(xpaths['bckWOWP_gold_submit']).click()

        # End visual testing. Validate visual correctness.
        test_results = list()
        test_results.append(eyes.close(False))

    # Do something with test results..
    print('And the result is...')
    for result in test_results: print(result)

finally:
    driver.quit()
    eyes.abort_if_not_closed()
