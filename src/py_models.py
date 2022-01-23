from pandas.core.indexes.datetimes import DatetimeIndex
from pydantic import BaseModel
from datetime import datetime


class Unit(BaseModel):
    size: float
    suffix: str


class ComputerInfo(BaseModel):
    system: str
    total_cores: int
    cpu_usage: float
    max_cpu_freq: float
    total_ram: Unit
    used_ram: Unit
    used_ram_percent: float
    gpu_name: str
    gpu_all_mem: float
    gpu_used_mem: float
    gpu_usage: float
    gpu_temperature: float
    data_sent: Unit
    date_receive: Unit
    time: datetime


class FigTimeline(BaseModel):
    dates_msec_freq: DatetimeIndex
    date_sec_daily: DatetimeIndex
    dates_str: list
    base_datetime: list

    class Config:
        arbitrary_types_allowed = True
