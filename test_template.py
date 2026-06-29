"""测试模板加载 - 使用 stderr 避免截断"""
import sys
sys.path.insert(0, "sample/python")
from wild_exp import find_device, setup_tasker

def log(msg):
    sys.stderr.write("[TEST] " + msg + "\n")
    sys.stderr.flush()

controller = find_device()
if not controller:
    log("FAIL: 无设备")
    sys.exit(1)

tasker = setup_tasker(controller)
if not tasker or not tasker.inited:
    log("FAIL: 初始化失败")
    sys.exit(1)

log("运行 StartMatch ...")
try:
    detail = tasker.post_task("WildHs_StartMatch").wait().get()
    if detail:
        log("entry: " + str(detail.entry))
        log("succeeded: " + str(detail.status.succeeded))
        log("status: " + str(detail.status))
    else:
        log("detail is None")
except Exception as e:
    log("异常: " + str(e))

log("DONE")
sys.exit(0)