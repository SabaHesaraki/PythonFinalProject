
import platform
import subprocess


class GenericProcessGetter:
    cmd = []

    def get_process_list(self):
        if self.cmd:
            return subprocess.check_output(self.cmd, text=True)
        else:
            raise NotImplementedError


class LinuxProcessGetter(GenericProcessGetter):
    cmd = ['ps', '-e', '--format', 'comm', '--no-heading']


class MacBsdProcessGetter(GenericProcessGetter):
    cmd = ['ps', '-e', '-o', 'comm=""', '-c']


class WindowsProcessGetter(GenericProcessGetter):
    cmd = ['tasklist', '/nh', '/fo', 'CSV']


def get_process_getter_class(os_name):
    process_getters = {
        'Linux': LinuxProcessGetter,
        'Darwin': MacBsdProcessGetter,
        'Windows': WindowsProcessGetter,
        'freebsd7': MacBsdProcessGetter,
    }
    try:
        return process_getters[os_name]
    except KeyError:
        raise NotImplementedError("No backend for OS")
