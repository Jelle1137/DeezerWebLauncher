import subprocess
import xbmcgui
import xbmc
import os

def launch_browser():
    try:
        # Path to the watcher script
        watcher_script_path = os.path.join(os.path.dirname(__file__), 'browser_home_exit.py')

        # Start watcher script in background
        subprocess.Popen(['sudo', '/usr/bin/python3', watcher_script_path])

        # Launch Firefox in fullscreen mode with Deezer
        subprocess.call(['/usr/bin/firefox', '--kiosk', 'https://www.deezer.com'])
    except Exception as e:
        xbmcgui.Dialog().ok("Error Launching Browser", str(e))

if __name__ == '__main__':
    launch_browser()
