import platform
from datetime import datetime
from time import sleep
from threading import Thread

import GPUtil
import psutil

from src.py_models import ComputerInfo, Unit


class SystemMonitor(Thread):
    data_pool = []

    def __init__(self, timeout: float = 1.0, pool_size: int = 120):
        Thread.__init__(self)
        self.timeout = timeout
        self.pool_size = pool_size

    @staticmethod
    def unit(_bytes, suffix="B"):
        factor = 1024
        for _unit in ["", "K", "M", "G", "T", "P"]:
            if _bytes < factor:
                return {"size": round(_bytes, 2), 'suffix': f"{_unit}{suffix}"}
            _bytes /= factor

    def monitor(self) -> ComputerInfo:
        uname = platform.uname()
        mem = psutil.virtual_memory()
        gpu = GPUtil.getGPUs()[0]
        internet = psutil.net_io_counters()
        info = ComputerInfo(system=uname.system,
                            total_cores=psutil.cpu_count(logical=True),
                            cpu_usage=psutil.cpu_percent(),
                            max_cpu_freq=psutil.cpu_freq().max,
                            total_ram=Unit(**self.unit(mem.total)),
                            used_ram=Unit(**self.unit(mem.used)),
                            used_ram_percent=mem.percent,
                            gpu_name=gpu.name,
                            gpu_all_mem=gpu.memoryTotal,
                            gpu_used_mem=gpu.memoryUsed,
                            gpu_usage=gpu.load,
                            gpu_temperature=gpu.temperature,
                            data_sent=Unit(**self.unit(internet.bytes_sent)),
                            date_receive=Unit(**self.unit(internet.bytes_recv)),
                            time=datetime.now())
        return info

    def run(self):
        while True:
            sleep(self.timeout)
            self.data_pool.append(self.monitor())
            if len(self.data_pool) > self.pool_size:
                del self.data_pool[:-self.pool_size]


if __name__ == '__main__':
    SystemMonitor().start()
    sleep(30)
    print('+')
