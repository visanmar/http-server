from urllib.parse import unquote
from datetime import (datetime, timedelta)
from .response import MimeTypes
import ipaddress


def decodeUrl(url):
    return unquote(url.replace('+', ' '))

def getQueryValues(urlQuery, fieldSep='&', dataSep='='):
    if not urlQuery:
        return False
    dic = {}
    for field in urlQuery.split(fieldSep, 1):
        key, value = field.split(dataSep, 1)
        dic[key.lower()] = value.strip()
    return dic

def getQueryParams(requestedResource):
    if not requestedResource:
        return None
    urlParams = requestedResource.split('?')
    if len(urlParams) > 1:
        urlParams = urlParams[1]
    else:
        urlParams = ''
    urlParams = urlParams.split('#')
    return urlParams[0]

def getUrlResource(requestedResource):
    return requestedResource.split('?')[0]

def getMimeTypeFromFile(filepath):
    file_extension = filepath.split('.')[-1]
    try:
        return MimeTypes[file_extension]
    except:
        return 'undefined'

def utcDatetime(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    now = datetime.datetime.utcnow()
    #now = datetime.datetime.now()
    date = now + timedelta(days, seconds, microseconds, milliseconds, minutes, hours, weeks)
    return date.strftime('%a, %d %b %Y %H:%M:%S UTC')

def validateNetConnectionAddress(ip):
    try:
        ip_object = ipaddress.ip_address(ip)
        return True
    except:
        return False

def validateNetConnectionPort(port=0):
    if int(port) >= 49152 and int(port) <= 64738:
        return True
    else:
        False
