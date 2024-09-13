import json
import heapq
from collections import defaultdict
from graphviz import Digraph

class Station:
    def __init__(self, name, lines):
        self.name = name  # 站点名称
        self.lines = lines  # 经过的线路
        self.neighbors = []  # 邻居站点信息

    def add_neighbor(self, neighbor, distance, speed, time, neighbor_lines):
        # 添加邻近站点
        self.neighbors.append({
            'station': neighbor,  # 邻近站点对象
            'distance': distance,  # 到邻近站点的距离
            'speed': speed,  # 在这段距离上的平均速度
            'time': time,  # 到达邻近站点所需时间
            'lines': neighbor_lines  # 邻近站点的线路
        })

    def __repr__(self):
        # 用于显示站点及其相关信息
        neighbor_info = [f'{neighbor["station"].name} ({neighbor["distance"]})' for neighbor in self.neighbors]
        return f'Station(name={self.name}, lines={self.lines}, neighbors={neighbor_info})'

def parse_stations_from_file(file_path):
    stations = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            stations_dict = json.load(file)

            for station_name, station_info in stations_dict.items():
                station = Station(station_name, station_info['lines'])

                for edge in station_info['edge']:
                    neighbor_name = edge['station']
                    distance = edge['distance']
                    speed = edge['speed']
                    time = edge['time']
                    neighbor_lines = edge['line']

                    if neighbor_name not in stations:
                        neighbor_station = Station(neighbor_name, neighbor_lines)
                        stations[neighbor_name] = neighbor_station

                    station.add_neighbor(stations[neighbor_name], distance, speed, time, neighbor_lines)

                stations[station_name] = station

    except FileNotFoundError:
        print(f"文件 {file_path} 不存在！")
    except IOError as e:
        print(f"读取文件时发生错误: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")

    return stations

def draw_metro_map(stations, output_file="metro_map.png"):
    dot = Digraph(comment='北京地铁图', format='png')
    dot.attr('node', fontname='Microsoft YaHei')  # 使用支持中文的字体

    # 添加节点
    for station in stations.values():
        label = f"<{station.name}<BR/>{'<BR/>'.join(station.lines)}>"
        dot.node(station.name, label=label, shape='plaintext')

    # 添加边
    for station in stations.values():
        for neighbor in station.neighbors:
            neighbor_name = neighbor['station'].name
            label = f"{neighbor['distance']}m<br/>{neighbor['time']}s"
            color = 'black'
            if not set(station.lines).intersection(set(neighbor['station'].lines)):
                color = 'red'  # 换乘线路用红色表示

            dot.edge(station.name, neighbor_name, label=label, color=color)

    # 渲染图形
    dot.render(output_file, view=True)

# 加载站点信息
stations = parse_stations_from_file('stations.json')  # 假设站点信息存储在 'stations.json' 文件中

# 绘制地铁图
draw_metro_map(stations)