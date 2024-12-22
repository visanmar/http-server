from .response import HttpResponseCodes
from .utils import decodeUrl, utcDatetime


class HttpRequestHeaders():
    def requestHeaders(self, httpHeaders):
        result = {}
        request_resource, headers = httpHeaders.split('\r\n', 1)
        req_method, req_resource, req_version = request_resource.split(' ')
        result['_request'] = {'method':req_method, 'resource':decodeUrl(req_resource), 'version':req_version}
        headers = headers.split('\r\n')
        result['cookies'] = {}
        for header in headers:
            header, value = header.split(':', 1)
            if header.lower() == 'cookie':
                key, value = value.strip().split('=', 1)
                value = value.split(';')[0]
                result['cookies'][key] = decodeUrl(value)
            else:
                result[header.lower()] = value.strip()
        return result
    

class HttpResponseHeaders():

    #region PRIVATE FUNCTIONS

    def __joinHeaders(self, headers={}):
        result = ''
        for key, value in headers.items():
            result += str(key) + ': ' + str(value) + '\r\n'
        return result[:-2]
    
    #endregion

    #region PUBLIC FUNCTIONS

    def get(self, server, responseCode, contentType, contentSize, cookies=[], responseheaders={}):
        responseHeaders = self.responseHeaders(server, responseCode, contentType, contentSize, cookies=[], responseheaders={})
        return self.encodeResponseHeaders(responseCode, responseHeaders)

    
    def responseHeaders(self, server, responseCode, contentType, contentSize, cookies=[], responseheaders={}):
        if contentType.split('/')[0] == 'text':
            contentType += '; charset=utf-8'
        headers = {
        'Content-Type': contentType,
        'Content-Size': contentSize,
        'Conection': 'Keep-Alive',
        'Server': server,
        'Date': utcDatetime(),
        **responseheaders,
        'cookies': cookies
        }
        return headers

    def encodeResponseHeaders(self, responseCode, headers={}):
        cookieStr = ''
        if headers['cookies']:
            for cookie in headers['cookies']:
                cookieKey, cookieValue, cookieParams = cookie
                cookieStr += f'Set-Cookie: {cookieKey}={cookieValue}; {cookieParams}\r\n'
        del headers['cookies']
        responseStatus = HttpResponseCodes[responseCode]
        responseHeaders = f'HTTP/1.1 {responseStatus}\r\n' + self.__joinHeaders(headers) + '\r\n' + cookieStr
        return responseHeaders.encode()
    
    #endregion
