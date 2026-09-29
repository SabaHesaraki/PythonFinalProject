
import platform
from backend import get_process_getter_class

os_name = platform.system()
process_getter = get_process_getter_class(os_name)()
print(process_getter.get_process_list())
