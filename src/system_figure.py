import asyncio
import io
import os
from time import sleep

import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import make_interp_spline

from src.py_models import ComputerInfo, FigTimeline
from src.system_info import SystemMonitor


# THIS CODE IN PROCESS DEVELOPING

class SystemInfoGraphicCreator:

    def __init__(self, pc_info: list[ComputerInfo]):
        self.colors = {}
        self.usage = []
        self.pc_info = pc_info.copy()
        self.timeline = asyncio.run(self.create_timeline())
        self.usages = {'cpu': '1'}

    @staticmethod
    async def create_data_array(pc_info: list[ComputerInfo], keyword: str):
        return [day.dict()[keyword] for day in pc_info]

    async def create_timeline(self) -> FigTimeline:
        dates_msec_freq = pd.date_range(self.pc_info[0].time, self.pc_info[-1].time, freq='50ms')
        date_sec_daily = pd.date_range(self.pc_info[0].time, self.pc_info[-1].time, freq='S')
        dates_str = [moment.time.time() for moment in self.pc_info]
        base_datetime = [moment.time.time() for moment in self.pc_info]
        timeline = FigTimeline(dates_msec_freq=dates_msec_freq, date_sec_daily=date_sec_daily,
                               dates_str=dates_str, base_datetime=base_datetime)
        return timeline

    async def create_usage_axe(self):
        for name, color in self.usages.items():
            values = await self.create_data_array(self.pc_info, name)
            color = '#' + color
            spl = make_interp_spline(self.timeline.date_range_daily, values, k=2)

    async def create_figure(self):

        fig_size = (192.0, 108.0)  # размер всей картинки
        fig = plt.figure(figsize=fig_size)
        fig, axes = plt.subplots(nrows=2, ncols=2)

        # plt.subplots_adjust(left=0.05, bottom=0.15, top=0.96, right=0.98)  # место графика на картинке
        # ax = plt.subplot(111)
        # ax.axis([base_datetime[0], base_datetime[-1], 40, 70])
        # plt.grid(linestyle=':')

        for row in fr_sorted_wr:
            fraction = list(row.keys())[0]
            values = await self.create_fraction_wr_array(pc_info, fraction)
            color = '#' + self.colors[fraction]
            wr = row[fraction][0]
            # returns a function that accepts new index value for interpolaction
            spl = make_interp_spline(date_range_daily, values, k=2)
            # return values imteprolated up to certain edge value we passed
            values_interp = spl(dates_hourly_freq)

            frequent_date_time = [pd.to_datetime(d) for d in dates_hourly_freq]

            # draw markers based on initial values
            if values[-1] == 00.00:
                continue
            plt.scatter(base_datetime, values, color=color, edgecolors='#ffffff')
            # draw the main interpolated plot
            plt.plot(frequent_date_time, values_interp, label=f'{fraction} {wr}', color=color, linewidth=1.3)
            plt.xticks(base_datetime, labels=dates_str, rotation=45, ha="right")

        plt.yticks(rotation=90)  # даты
        plt.xlabel('Dates DD\\MM')
        plt.ylabel('Winrate (%)')
        if user:
            plt.title(f'WR statistics for {name} by t.me/gw_helper_2_bot')
        plt.title(f'WR statistics from {name} ({players} players) by t.me/gw_helper_2_bot')
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12),
                   fancybox=True, shadow=None, ncol=6, edgecolor='w')
        plt.savefig(f'configs/{name}.png')
        plt.close()

        with Image.open(f'configs/{name}.png').convert("RGBA") as img:
            with Image.open('configs/sompicF.png').convert("RGBA") as watermark:
                img.paste(watermark, (950, 500), watermark)
                img.save(f"configs/{name}.png")
        with io.BytesIO() as output:
            img.save(output, format="webp")
            contents = output.getvalue()
        os.remove(f"configs/{name}.png")
        return contents


if __name__ == '__main__':
    monitor = SystemMonitor()
    monitor.start()
    sleep(120)
    creator = SystemInfoGraphicCreator(monitor.data_pool)
    print()
    # asyncio.run(SystemInfoGraphicCreator(monitor.data_pool).create_figure())
