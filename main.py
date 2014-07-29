#!/usr/bin/env python -tt
# -*- coding:  utf-8 -*-
import os
import sys

from selenium import webdriver
from applitools.eyes import Eyes, BatchInfo

# This is your api key, make sure you use it in all your tests.
Eyes.api_key = '3Z1sOfalzP1QClQrzmHJaU5BbKiR0AFZlDsBPoVB3Uk110'
eyes = Eyes()
batch = BatchInfo("WG portal batch")
eyes.batch = batch

# Get a selenium web driver object.
driver = webdriver.Firefox()

try:
    # viewSizeArray =[{'width': 1024, 'height': 768}, {'width': 1280, 'height': 1024}]
    # viewSizeArray = [[width, height],[...]...]
    viewSizeArray = [[1920, 1080], [1600, 1200], [1280, 1024], [1024, 768], [800, 600]]
    # viewSizeArray = [[1920, 1080], [1600, 1200]]
    # Make sure to use the returned driver from this point on.
    for viewSize in viewSizeArray:
        viewSizeForAppliTools = {'width': viewSize[0], 'height': viewSize[1]}
        driver = eyes.open(driver=driver,
                           app_name='Applitools',
                           test_name='Basic WG Portal test: resolution - ' + str(viewSize[0]) + 'x' + str(viewSize[1]),
                           viewport_size=viewSizeForAppliTools)
        driver.get('http://ru.wargaming.net/')
        # Visual validation point #1
        eyes.check_window('Main Page')
        wot_about = driver.find_element_by_link_text("О проекте")
        wot_about.click()
        # Visual validation point #2
        eyes.check_window('WOT about Page')

        # End visual testing. Validate visual correctness.
        test_results = list()
        test_results.append(eyes.close(False))

    #Do something with test results..
    print('And the result is...')
    for result in test_results: print(result)

finally:
    driver.quit()
    eyes.abort_if_not_closed()