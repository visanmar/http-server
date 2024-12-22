from os import listdir
from os.path import isfile, isdir
import re



HttpResponseCodes = {
    200: '200 OK',
    301: '301 Moved Permanently',
    302: '302 Found',
    404: '404 Not Found',
    403: '403 Forbidden',
    500: '500 Server Error'
}

MimeTypes = {
    'html': 'text/html',
    'txt': 'text/plain',
    'css': 'text/css',
    'js': 'text/javascript',
	'json': 'application/json',
    'gif': 'image/gif',
    'png': 'image/png',
    'jpg': 'image/jepg',
    'jpeg': 'image/jpeg',
    'json': 'text/json'
}


def getMimeTypeFromFile(filepath):
    file_extension = filepath.split('.')[-1]
    try:
        return MimeTypes[file_extension]
    except:
        return 'undefined'

class HttpResponse():
    def __int__(self, rootPath, requestedResource, documentIndex=[], directoryListing=False):
        self.__rootpath = rootPath
        self.__requestedResource = requestedResource
        self.__documentIndex = documentIndex
        self.__directoryListing = directoryListing
        self.__fd = None

    def __end__(self):
        if self.__fd:
            self.__fd.close()


    #region PRIVATE FUNCTIONS

    def __LoadResource(self):
        #print('Resource:', self.__requestedResource)
        self.__fd = None
        try:
            if isdir(self.__requestedResource):
                foundDocIndex = False
                for docIndex in self.__documentIndex:
                    doc = self.__requestedResource + '/' + docIndex
                    if isfile(doc):
                        self.__requestedResource = doc
                        foundDocIndex = True
                        break
                if foundDocIndex:
                    pass # Hay un documentIndex en el directorio. Lo carga proque no retorna nada la función.
                elif self.__directoryListing:
                    dir_content_html = self.__getDirContentHtml(self.__requestedResource)
                    return (200, dir_content_html.encode(), 'text/html', len(dir_content_html))
                else:
                    # client does not have access rights
                    responseContent = f'<h1>{HttpResponseCodes[403]}</h1>'
                    return (403, responseContent.encode(), 'text/html', len(responseContent))
            mime = getMimeTypeFromFile(self.__requestedResource)
            if mime.split('/')[0] == 'text':
                self.__fd = open(self.__requestedResource, 'r', encoding='utf-8')
                file_content = self.__fd.read().encode()
            else:
                self.__fd = open(self.__requestedResource, 'rb')
                file_content = self.__fd.read()
            self.__fd.close()
            return (200, file_content, mime, len(file_content))
        except FileNotFoundError as exc:
            # file not exists error
            #print(exc)
            responseContent = f'<h1>{HttpResponseCodes[404]}</h1>'
            return (404, responseContent.encode(), 'text/html', len(responseContent))
        except IOError as exc:
            #file read error
            #print(exc)
            responseContent = f'<h1>{HttpResponseCodes[500]}</h1>'
            return (500, responseContent.encode(), 'text/html', len(responseContent))
        except Exception as exc:
            # file open error
            #print(exc)
            responseContent = f'<h1>{HttpResponseCodes[500]}</h1>'
            return (500, responseContent.encode(), 'text/html', len(responseContent))
        finally:
            if self.__fd:
                self.__fd.close()
    
    def __getDirContentHtml(self, requestedDir):
        real_path = requestedDir
        web_path = re.sub('^'+self.__rootpath, '', requestedDir)
        
        html = '<style>.directory_listiing{font-size:1.2em;}.dir-content{list-style:none;margin:0;padding:0;line-height:0;}.dir-content>li{padding:2px 0;}.dir-content>li>a{line-height:1em;}</style>'
        html += '<div class="directory_listiing">'
        html += f'<h3>{web_path}</h3>'

        if (web_path != '/'):
            parent_web_dir = '/'.join(web_path.split('/')[:-1])
            if len(parent_web_dir) == 0:
                parent_web_dir = '/'
            html += f'<a class="parent-dir" href="{parent_web_dir}">[parent dir]</a><br><br>'

        dir_content = listdir(real_path)
        if not dir_content:
            html += '<i>empty directory</i>'
        else:
            html += '<ul class="dir-content">'    
            for dir_entry in dir_content:
                entry_path = web_path+'/'+dir_entry
                if isdir(real_path+dir_entry):
                    css_class = 'is-dir'
                else:
                    css_class = 'is-file'
                html += f'<li class="{css_class}"><a href="{entry_path}">{dir_entry}</a></li><br>\r\n'
            html += '</ul>'

        html += '</div>'
        
        return html
    
    #endregion