#!/usr/bin/env python3


import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from pandas import json_normalize
import json
from pytz import timezone
import pytz
from dateutil import parser
from optparse import OptionParser

class SpeedCheckData:
    def __init__(self):
        self.df = None
        
    @staticmethod 
    def bps_to_mbps(bit):
        return bit / 125000

    @staticmethod
    def utc_to_jtc(utc):
        try:
            # dt = parser.parse(utc).astimezone(timezone('Asia/Tokyo'))
            utc = parser.parse(utc);
            jst = utc.astimezone(timezone('Asia/Tokyo'))
            dt = jst.strftime('%m/%d\n%H:%M')
        except TypeError:
            dt = 'nan'
        
        return dt
#        dt_utc = datetime.datetime.strptime(utc, '%Y-%m-%dT%H:%M:%SZ')
#        dt_jst = dt_utc.astimezone(datetime.timezone(datetime.timedelta(hours=+9)))
#        return datetime.datetime.strftime(dt_jst, '%Y-%m-%d %H:%M:%S.%f')


        
    def load(self, path):
        with open(path) as f:
            lines = f.readlines();
            js = '{\"Results\":['+ ','.join(lines) + ']}'
        self.df = json_normalize(json.loads(js)['Results'])
        # bps -> Mbps
        self.df['download.bandwidth'] = self.df['download.bandwidth'].map(lambda x: x / 125000)
        self.df['upload.bandwidth'] = self.df['upload.bandwidth'].map(lambda x: x / 125000)
        # UTC -> LocalTime
        self.df['timestamp'] = self.df['timestamp'].map(lambda x: self.utc_to_jtc(x))
        print(self.df['isp'])
        print(self.df['server.host'])
    def dump(self):
        print(self.df)

    def draw_graph(self):
        ax = self.df.plot(x='timestamp', y='download.bandwidth')
        self.df.plot(y='upload.bandwidth', ax=ax)
        ax.set_xlabel('DateTime')
        ax.set_ylabel('Mbps')
        print('download.bandwidth(max)=', self.df['download.bandwidth'].max())
        print('download.bandwidth(min)=', self.df['download.bandwidth'].min())
#        ax.grid(which = "major", axis = "x", color = "blue", alpha = 0.8,
#                linestyle = "--", linewidth = 1)
#        ax.grid(which = "major", axis = "y", color = "green", alpha = 0.8,
#                linestyle = "--", linewidth = 1)
        plt.plot(grid=True)
        plt.title("Speedtest")

        plt.show()
        # plt.savefig('graph.png')
        # plt.close()
        
def main():
    parser = OptionParser()
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="verbose mode")
    (options, args) = parser.parse_args()
    data = SpeedCheckData()
    if len(args) == 0:
        data.load('/var/log/speedtest')
    else:
        data.load(args[0])
    if options.verbose:
        data.dump()
    data.draw_graph()
    
if __name__ == "__main__":
    main()
