from viclib.settingsParser import SettingsParser

class ServerSettins(SettingsParser):
    def __init__(self, settingsFile='http_server.config', check=False):
        super().__init__(settingsFile, check)

    def _init_settings(self):
        self._settings['address'] = ()
        self._settings['max_connextions'] = 5
        self._settings['client_receive_size'] = 2048
        self._settings['root_path'] = '.'
        self._settings['document_index'] = ('index.html',)
        self._settings['directory_listing'] = False
        self._settings['file_handler'] = []
        self._settings['http_connection_live'] = 'keep-alive'
        self._settings['client_connection_timeout'] = 10
        self._settings['header'] = []
        self._settings['cookie'] = []
        self._settings['server_name'] = True
        self._settings['loggers'] = ('console',)
        self._settings['logger_level'] = 'INFO'

    

