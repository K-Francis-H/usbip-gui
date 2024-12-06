if __name__ == "__main__":
    from .gui import start_app

    start_app()


# subprocess.call(["pkexec","--keep-cwd", "bash", "-c" ,f"DISPLAY={getenv('DISPLAY')} ; ", "python", "gui.py"])
# TODO now make a simple window to manage servers, devices on servers etc

# TODO also make a simple install script to fetch the usbip and linxu-tools-generic packages and modprobe the modules
