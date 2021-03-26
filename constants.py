# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 16:24:17 2021

@author: scott
"""

# import sys
from pathlib import Path

databaseName = "usage-SUSHI"

currentDirectory = None
dbFile = "usage.db"


# The homeDirectory here is the directory in which the main app
# resides, even for apps in the experiments directory
homeDirectory = Path(__file__).parent

dbFileName = str(homeDirectory / dbFile)

iconHome = homeDirectory / "GUI" / "icons"
