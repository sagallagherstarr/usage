# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 12:21:49 2021

@author: scott
"""

from ..main import setupMasterApp
    
def test_app1():
    masterApp = setupMasterApp()
    
    assert masterApp is not None

def test_window1():
    masterApp = setupMasterApp()
    
    assert masterApp is not None
    
    assert masterApp.getMainWindow() is not None
