# Python HTTP server

Example of using sockets in Python to create a package Python HTTP server.

> [!CAUTION]
> This project is currently developing.
> Sometimes this project cannot be executed or done incorrectly.

## What does this project use?
- Python 3  (used 3.13)
- Python sockets
- Python threads using threading library
- Python logging library
- Other library needed

## Requirements
No additional libraries needed. Currently only those incorporated by Python.

The httpdocs directory is used to serve server content.

## Task tracking
- [x] Create basic HTTP server
- [x] Add logging
- [x] Create Python package
- [x] Add some header responses
- [x] Add serve all files types
- [x] Add command line options
- [x] Add cookies
- [x] Add command shell command line options to start server as a Python module
- [x] Create main HTTP server thread
- [ ] Handle clients with threads
- [ ] Add parser to load settings file
- [ ] Add handlers for serve script languages
- [ ] Add more features???

## How to use it?
At project directory use:
```cmd
python -m vlsm_http.server [-a ip_address] [-p port] [-d root_directory]* [-c config_file]* [-h]
```
Default command line params:
- ip_address: 127.0.0.1
- port: 8000
- root_directory*
- config_file*

\* developing it
