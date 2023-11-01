# -*- coding: utf-8 -*-
from requests.auth import HTTPBasicAuth
import requests
import json
from datetime import datetime

from odoo.addons.portal.controllers.portal import pager as portal_pager, CustomerPortal
from odoo import http, _, fields
from odoo.http import request


class MercantilPayment(CustomerPortal):
    pass
