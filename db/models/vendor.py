# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 12:37:12 2021

@author: scott
"""

"""Model for a vendor, which contains all the information necessary to
make the SUSHI connection.  Supported reports/COUNTER versions is in a
separate table.

Fields:
    -- vendor name
    -- vendor identifier (this helps to separate multiple accounts
                          per vendor)
    -- vendor description
    -- contact information
    -- status [ active/inactive ]
    -- SUSHI request URL template
    -- SUSHI fields:
        -- Requester ID
        -- Customer ID
        -- Requester Name
        -- Customer Name
        -- User Name
        -- Password
        -- Requester Email
        -- API Key
        -- Platform
"""

""" local data, do not distribute!
vendor name = "Annual Reviews"
vendor identifier = "AnnualReviews"
vendor description = "Multiple annual review titles"
contact information = "iops@annualreviews.org"
status = active
SUSHI request URL template = "https://www.annualreviews.org/reports/<COUNTER5 report id>?requestor_id=sgallagherstarr&customer_id=224197&<other parameters>"
Requester ID = "sgallagherstarr"
Customer ID = "224197"
"""
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.debug("begin vendor.py")

from peewee import CharField

from db.models import ModelBase

class VendorModel(ModelBase):
    name = CharField()
    identifier = CharField(unique=True)
    description = CharField(null=True)
    contact = CharField(null=True)
    status = CharField()
    url_template = CharField(null=False)
    requester_id = CharField()
    customer_id = CharField()
    requester_name = CharField()
    customer_name = CharField()
    user_name = CharField()
    password = CharField()
    requester_email = CharField()
    api_key = CharField()
    platform = CharField()
    
    headerNames = [ "Vendor Name",
                    "Vendor Identifier",
                    "Description",
                    "Contact Info",
                    "Status",
                    "URL or URL template",
                    "Requester ID",
                    "Customer ID",
                    "Requester Name",
                    "Customer Name",
                    "User Name",
                    "Password",
                    "Requester Email",
                    "API Key",
                    "PLatform"
                  ]
    
if __name__ == "__main__":
    from db import registerModel, DatabaseConnection
    
    test_db = "./vendor_model.db"
    dbConnection = DatabaseConnection(test_db)
    dbConnection.prepareConnection()
    
    registerModel(VendorModel)
    
    dbConnection.createTables(drop_first=True)
    
    bob = VendorModel(name="Friendly",
                      identifier="FRIENDLY",
                      description="",
                      contact="",
                      status="",
                      url_template="",
                      requester_id="",
                      customer_id="",
                      requester_name="",
                      customer_name="",
                      user_name="",
                      password="",
                      requester_email="",
                      api_key="",
                      platform="")
    
    print("bob is %s\n%r", bob, bob)