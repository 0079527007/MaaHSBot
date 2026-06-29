"""极简测试 - 只初始化并运行 StartMatch"""
import sys, os, time
os.chdir(r"E:\1Maa\HSMaaBot")
sys.path.insert(0, "sample/python")

from maa.toolkit import Toolkit
from maa.controller import AdbController
from maa.resource import Resource
from maa.tasker import Tasker

f = open("test_minimal_out.txt", "w", encoding="utf-8", buffering=1)
def log(msg):
    f.write(msg + "\n")
    f.flush()

Toolkit.init_option("./")
resource = Resource()

adb_devices = Toolkit.find_adb_devices()
if not adb_devices:
    log("FAIL: 无 ADB 设备")
    f.close()
    sys.exit(1)

d = adb_devices[0]
log(f"DEVICE: {d.name} ({d.address})")
controller = AdbController(adb_path=d.adb_path, address=d.address,
    screencap_methods=d.screencap_methods,
    input_methods=d.input_methods, config=d.config)

log("CONNECT...")
controller.post_connection().wait()

log("LOAD RESOURCE...")
resource.post_bundle("sample/resource").wait()

log("BIND TASKER...")
tasker = Tasker()
tasker.bind(resource, controller)
if not tasker.inited:
    log("FAIL: tasker 初始化失败")
    f.close()
    sys.exit(1)

log("RUN StartMatch (timeout=30s)...")
start = time.time()
try:
    detail = tasker.post_task("WildHs_StartMatch").wait().get()
    elapsed = time.time() - start
    log(f"ELAPSED: {elapsed:.1f}s")
    if detail:
        log(f"entry: {detail.entry}")
        log(f"succeeded: {detail.status.succeeded}")
        log(f"done: {detail.status.done}")
    else:
        log("detail is None")
except Exception as e:
    log(f"EXCEPTION: {e}")
    import traceback
    traceback.print_exc(file=f)

log("DONE")
f.close()