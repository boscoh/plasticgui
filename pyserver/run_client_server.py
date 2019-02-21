from __future__ import print_function
import sys
import threading
import time
from six.moves import urllib
import webbrowser
import subprocess
from server import config

urlopen = urllib.request.urlopen

def open_page_if_server():
    elapsed = 0
    is_server_not_running = True
    while is_server_not_running:
        try:
            url = 'http://localhost:' + str(config.PORT)
            response_code = urlopen(url).getcode()
            if response_code < 400:
                webbrowser.open(url)
                is_server_not_running = False
        except:
            time.sleep(1)
            elapsed += 1
            print("Waiting", elapsed, "s for", url, " on server")

# creates a thread to poll server before opening client
threading.Thread(target=open_page_if_server).start()

# creates new process for flask in threaded debug mode
# so that it doesn't interfere with the thread
# for the web-browser polling
subprocess.call([sys.executable, "run_local.py"])