import sys, getopt, signal, platform
from os.path import isdir
from socket import (socket, AF_INET, SOCK_STREAM, SHUT_RDWR, SOL_SOCKET, SO_REUSEADDR)
from .utils import getQueryParams, getQueryValues, decodeUrl, validateNetConnectionAddress, validateNetConnectionPort
from .headers import HttpRequestHeaders, HttpResponseHeaders
import logging
from logging.handlers import TimedRotatingFileHandler
import traceback
from .serverWorker import __ServerWorker
from threading import (Thread, Event)
from time import sleep



class HttpServerSignal(Event):
    def __init__(self):
        Event.__init__(self)

_httpServerSignalStop = HttpServerSignal()


class Cliente(Thread):
    def __init__(self, socket):
        Thread.__init__(self)
        self.__stop_event = Event()
        self.__socket = socket
        self.__socket_addr = socket.getpeername()
        self.__socket.settimeout(5)

    #def __end__(self):
    #    if self.__socket:
    #        self.__socket.close()

    def run(self):
        print("Conectado cliente", self.__socket_addr)
        self.__socket.send(b'dsfsf sdfsfssaa')
        sleep(5)
        print("Cerrado cliente", self.__socket_addr)
        self.__socket.close()



class HttpServer(Thread):
    
    # region MAGIC METHODS
    
    def __init__(self, address, maxConn=5, configFile=''):
        Thread.__init__(self)
        self.deamon = True

        #region PRIVATE PROPERTIES

        self.__address = address
        self.__maxConn = maxConn
        self.__SOCKET = None
        self.__receiveSize = 1024
        self.__rootPath = '.'
        self.__documentIndex = ('index.html')
        self.__directoryListing = False
        self.__fileHandlers = {}
        self.__httpConnectionLive = 'keep-alive'
        self.__connectionTimeout = 10
        self.__extraHeaders = {}
        self.__cookies = []
        self.__logger = None
        self.__loggers = ['console']
        self.__loggerLevel = 'INFO'

        #endregion


        self.__setLogger()

        if configFile:
            try:
                self.__loadConfigFile(configFile)
            except Exception:
                print('ERROR', f'Fail to load config file: {configFile}')
        

    def __del__(self):
        try:
            pass
        except:
            pass

    def __str__(self):
        if not self.__SOCKET:
            return 'HTTP server not running.'
        else:
            return f'HTTP server running on {self.__address}'
        
    #endregion

    #region PROPERTIES

    @property
    def address(self):
        return self.__address
    @address.setter
    def address(self, value):
        print('#####', value)
        self.__address = value

    @property
    def receiveSize(self):
        return self.__receiveSize
    @receiveSize.setter
    def receiveSize(self, value):
        self.__receiveSize = value

    @property
    def rootPath(self):
        return self.__rootPath
    @rootPath.setter
    def rootPath(self, value):
        if value[0] != '.':
            value = '.' + value
        self.__rootPath = value

    @property
    def documentIndex(self):
        return self.__documentIndex
    @documentIndex.setter
    def documentIndex(self, value):
        self.__documentIndex = value

    @property
    def directoryListing(self):
        return self.__directoryListing
    @directoryListing.setter
    def directoryListing(self, value):
        self.__directoryListing = value

    @property
    def fileHandlers(self):
        return self.__fileHandlers
    @fileHandlers.setter
    def fileHandlers(self, value):
        for handler in value:
            fileExtension, hdlr = handler
            self.__fileHandlers[fileExtension] = hdlr

    @property
    def connectionLive(self):
        return self.__connectionLive
    @connectionLive.setter
    def connectionLive(self, value):
        self.__connectionLive = value

    @property
    def connectionTimeout(self):
        return self.__connectionTimeout
    @connectionTimeout.setter
    def connectionTimeout(self, value):
        self.__connectionTimeout = value

    @property
    def headers(self):
        return self.__extraHeaders
    @headers.setter
    def headers(self, value):
        self.__extraHeaders = value
        
    @property
    def loggers(self):
        return self.__loggers
    @loggers.setter
    def loggers(self, value):
        self.__loggers = value

    @property
    def loggerLevel(self):
        return self.__loggerLevel
    @loggerLevel.setter
    def loggerLevel(self, value):
        self.__loggerLevel = value

    #endregion


    #region PRIVATE FUNCTIONS

    def __loadConfigFile(self, configFile):
        pass


    def __recv(self, clientSocket):
        try:
            return clientSocket.recv(2048).decode()
        except TimeoutError as exc:
            print(exc, clientSocket.getpeername())
        except Exception as exc:
            traceback.print_exc()
            return None


    def __getRequestData(self, headerRequest, body):
        method, resource, version = headerRequest.values()
        method = method.upper()
        if method == 'GET':
            data = getQueryParams(resource)
            if not data:
                return (method, None)
            return (method, getQueryValues(data))
        elif method == 'POST':
            return (method, getQueryValues( decodeUrl(body) ))
        else:
            return (method, None)


    def __setLogger(self):
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(self.__loggerLevel)
        logger_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')
        if 'console' in self.__loggers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logger_formatter)
            self.__logger.addHandler(console_handler)
        if 'file' in self.__loggers:
            file_handler = TimedRotatingFileHandler('httpserver.log', when='D', interval=5, backupCount=3)
            file_handler.setFormatter(logger_formatter)
            self.__logger.addHandler(file_handler)


    def __HandleResponse(self, reaponse):
        pass


    def __log(self, logLevel, logMessage):
        if 'stdout' in self.__loggers:
            print(logMessage)
        if 'console' in self.__loggers or 'file' in self.__loggers:
            self.__logger.log(logging.getLevelNamesMapping()[logLevel], logMessage)

    #endregion


    #region PUBLIC FUNCTIONS

    def run(self):
        try:
            self.__log('INFO', f'Starting HTTP server on {self.__address}...')
            self.__SOCKET = socket(AF_INET, SOCK_STREAM)
            self.__SOCKET.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            self.__SOCKET.bind(self.__address)
            self.__SOCKET.listen(self.__maxConn)
            self.__log('INFO', f'Waiting for connections...')

            
            i = 1;
            while not _httpServerSignalStop.is_set():
            #while i < 10:
                print(_httpServerSignalStop)

                print(i)
                i += 1
                sleep(1)

                #try:
                #    client, client_addr = self.__SOCKET.accept()
                #    hiloCliente = Cliente(client)
                #    self.__log('DEBUG', f'Connected {client_addr}')
#
                #    hiloCliente.run()
                #except:
                #    traceback.print_exc()

                #data = self.__recv(self.__client)
                #if not data:
                #    continue
                #print('data =>', data)
                #self.__client.close()
                #self.__log('DEBUG', f'Connection clossed for {self.__client_addr}')

            self.__SOCKET.shutdown(SHUT_RDWR)
            self.__SOCKET.close()
            self.join()
            self.__log('INFO', 'HTTP server shutdown.')
           
        except OSError:
            pass
        except Exception:
            traceback.print_exc()


    def shutdown(self):
        _httpServerSignalStop.set()
        self.join()
        self.__log('INFO', 'HTTP server shutdown by user.')

    #endregion


if __name__ == '__main__':
    def __cmd_help(exit_code=0, help=''):
        print('exit code', exit_code)
        if help:
            print(f'Incorrect option: {help}\nserver.py [-a ip_address] [-p port] [-d root_directory] [-c config_file]')
            print('Default:', 'a=127.0.0.1', '/', 'p=8000')
        else:
            print('server.py [-a ip_address] [-p port] [-d root_directory] [-c config_file]')
        sys.exit(exit_code)

    argv = sys.argv[1:]
    print(argv)
    ip = '127.0.0.1'
    port = 8000
    rootDir = '.'
    configFile = None

    opt, arg = getopt.getopt(argv,"ha:p:d:c:")

    try:
        for opt, arg in opt:
            if opt == '-h':
                __cmd_help(1)
            elif opt == '-a':
                if not validateNetConnectionAddress(arg):
                    __cmd_help(2, 'a='+arg)
                else:
                    ip = arg
            elif opt == '-p':
                if not validateNetConnectionPort(arg):
                    __cmd_help(3, 'p='+arg)
                else:
                    port = arg
            elif opt == '-d':
                if not isdir(arg):
                    pass
                    #__cmd_help(4, 'c=root_directory')
                else:
                    rootDir = arg
            elif opt == '-c':
                if not isdir(arg):
                    __cmd_help(5, 'c=config_file')
                else:
                    configFile = arg

        if (configFile):
            print(f'Starting HTTP server (config file: {configFile})')
            http_server = HttpServer(configFile)
        else:
            def ctrlc_signal_handler(signum, frame):
                http_server.stop()

            if platform.system() == 'Windows':
                signal.signal(signal.SIGINT, signal.CTRL_C_EVENT)
            else:
                signal.signal(signal.SIGINT, ctrlc_signal_handler)

            http_server = HttpServer( (ip, int(port)) )
            try:
                http_server.rootPath = rootDir
                http_server.start()

                i = 1
                while i < 5:
                    print('>>>', i)
                    i += 1
                    sleep(1.5)
                #http_server.shutdown()
                
            except Exception as exc:
                traceback.print_exc()

    except getopt.GetoptError:
        traceback.print_exc()
        __cmd_help(99)


    

