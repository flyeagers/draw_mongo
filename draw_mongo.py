import sys
import pandas as pd
import pymongo
from pandas import Series
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as nm
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def init_plot_coordinator():
    plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%.7f'))
    plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.7f'))
    plt.xlabel('Longitude')
    plt.ylabel('latitude')


def read_gps_file(name):
    fp = open(name)
    lat_list = []
    lon_list = []
    try:
        while 1:
            line = fp.readline()
            if not line:
                break
            new_line = line.split()
            latitude = new_line[4]
            longitude = new_line[5]

            lat_list.append(latitude)
            lon_list.append(longitude)
    finally:
        fp.close()
        return zip(lon_list, lat_list)


def draw_gps_pic(positions):
    cur_lat = ''
    cur_lon = ''
    gps_cnt = 0

    for gps_cnt, position in enumerate(positions):
        cur_lon, cur_lat = position
        try:
            next_lon, next_lat = positions[gps_cnt+1]
            plt.plot((cur_lon, next_lon), (cur_lat, next_lat), 'b')
            plt.plot((cur_lon, next_lon), (cur_lat, next_lat), 'or')
        except IndexError:
            pass
    print 'plot gps_tracker over'


def draw_double_gps(positions1, positions2):
    for gps_cnt, position in enumerate(positions2):
        cur_lon, cur_lat = position
        try:
            next_lon, next_lat = positions1[gps_cnt+1]
            plt.plot((cur_lon, next_lon), (cur_lat, next_lat), 'b')
        except IndexError:
            pass
    print 'over'


def draw_gps_data(positions, color_name):
    cur_lat = ''
    cur_lon = ''
    gps_cnt = 0

    for gps_cnt, position in enumerate(positions):
        cur_lon, cur_lat = position
        try:
            next_lon, next_lat = positions[gps_cnt+1]
            plt.plot((cur_lon, next_lon), (cur_lat, next_lat), color_name)
            plt.plot((cur_lon, next_lon), (cur_lat, next_lat), 'or')
        except IndexError:
            pass
    #print 'plot gps data over'


def draw_line_gps_data(positions, color_name):
    cur_lat = ''
    cur_lon = ''
    gps_cnt = 0

    for gps_cnt, position in enumerate(positions):
        cur_lon, cur_lat = position
        try:
            next_lon, next_lat = positions[gps_cnt+1]
            plt.plot((cur_lon, next_lon), (cur_lat, next_lat), color_name)
            #plt.plot((cur_lon, next_lon), (cur_lat, next_lat), 'or')
        except IndexError:
            pass
    #print 'plot gps data over'


def draw_point_gps_data(positions, colors):
    cur_lon, cur_lat = positions
    try:
        next_lon, next_lat = positions
        #plt.plot((cur_lon, next_lon), (cur_lat, next_lat), color_name)
        plt.plot((cur_lon, next_lon), (cur_lat, next_lat), colors)
    except IndexError:
        pass
    #print 'plot gps data over'


def draw_plane_data(col_name, bd_id, fl_index, color):
    plane_len = db[col_name].find({"bd_id": bd_id, "floor_index": fl_index}).count()

    cursor_plane = db[col_name].find({"bd_id": bd_id, "floor_index": fl_index})
    plane_id_list = [it_val['plane_id'] for it_val in cursor_plane]
    print 'plane_id_list is got'

    for i in xrange(plane_len):
        plane_gps_list = []
        cursor_plane = db[col_name].find({"bd_id": bd_id, "floor_index": fl_index, "plane_id": plane_id_list[i]})
        plane_data = cursor_plane.next()
        plane_gps = zip(plane_data[u'plane_gps'])
        for j in range(len(plane_gps)):
            gps_data = plane_gps[j][0]
            gps_data[0] = str(gps_data[0])
            gps_data[1] = str(gps_data[1])
            new_gps_data = tuple(gps_data)
            plane_gps_list.append(new_gps_data)

        draw_line_gps_data(plane_gps_list, color)

    print 'plane data is over'


def draw_pass_data(col_name, bd_id, fl_index):
    pass_len = db[col_name].find({"bd_id": bd_id, "floor_index": fl_index}).count()
    color_name = 'or'

    cursor_pass = db[col_name].find({"bd_id": bd_id, "floor_index": fl_index})
    pass_id_list = [it_val['pass_id'] for it_val in cursor_pass]
    print 'pass_id_list is got'

    for i in xrange(pass_len):
        cursor_pass = db[col_name].find({"bd_id": bd_id, "floor_index": fl_index, "pass_id": pass_id_list[i]})
        pass_data = cursor_pass.next()
        pass_gps = pass_data[u'pass_gps']

        draw_point_gps_data(pass_gps, color_name)

    print 'pass data is over'


def draw_node_data(col_name, bd_id, fl_index):
    node_len = db[col_name].find({"bd_id": bd_id, "floor_index": fl_index}).count()
    color_name = 'om'

    cursor_node = db[col_name].find({"bd_id": bd_id, "floor_index": fl_index})
    node_id_list = [it_val['node_id'] for it_val in cursor_node]
    print 'pass_id_list is got'

    for i in xrange(node_len):
        cursor_node = db[col_name].find({"bd_id": bd_id, "floor_index": fl_index, "node_id": node_id_list[i]})
        node_data = cursor_node.next()
        node_gps = node_data[u'node_gps']

        draw_point_gps_data(node_gps, color_name)

    print 'node data is over'


def draw_link_data(col_name, bd_id, fl_index, color):
    link_len = db[col_name].find({"bd_id": bd_id, "floor_index": fl_index}).count()

    cursor_link = db[col_name].find({"bd_id": bd_id, "floor_index": fl_index})
    link_id_list = [it_val['link_id'] for it_val in cursor_link]
    print 'link_id_list is got'

    for i in xrange(link_len):
        link_gps_list = []
        cursor_link = db[col_name].find({"bd_id": bd_id, "floor_index": fl_index, "link_id": link_id_list[i]})
        link_data = cursor_link.next()
        link_gps = zip(link_data[u'link_gps'])
        for j in range(len(link_gps)):
            gps_data = link_gps[j][0]
            gps_data[0] = str(gps_data[0])
            gps_data[1] = str(gps_data[1])
            new_gps_data = tuple(gps_data)
            link_gps_list.append(new_gps_data)

        draw_line_gps_data(link_gps_list, color)

    print 'link data is over'


def draw_border_data(col_name_fl, col_name_bd, bd_id, fl_index):
    floor_len = db[col_name_fl].find({"bd_id": bd_id, "floor_index": fl_index}).count()

    cursor_floor = db[col_name_fl].find({"bd_id": bd_id, "floor_index": fl_index})
    floor_gps_list = []
    floor_data = cursor_floor.next()
    floor_gps = zip(floor_data[u'floor_gps'])
    for j in range(len(floor_gps)):
        fgps_data = floor_gps[j][0]
        fgps_data[0] = str(fgps_data[0])
        fgps_data[1] = str(fgps_data[1])
        new_fgps_data = tuple(fgps_data)
        floor_gps_list.append(new_fgps_data)
    colors_fl = 'r'
    draw_gps_data(floor_gps_list, colors_fl)

    cursor_builds = db[col_name_bd].find({"bd_id": bd_id})
    builds_gps_list = []
    builds_data = cursor_builds.next()
    builds_gps = zip(builds_data[u'bd_gps'])
    for j in range(len(builds_gps)):
        bgps_data = builds_gps[j][0]
        bgps_data[0] = str(bgps_data[0])
        bgps_data[1] = str(bgps_data[1])
        new_bgps_data = tuple(bgps_data)
        builds_gps_list.append(new_bgps_data)
    color_bd = 'r'
    draw_gps_data(builds_gps_list, color_bd)

    if bd_id is "BKKJDS000001":
        draw_double_gps(floor_gps_list, builds_gps_list)


if __name__ == '__main__':
    # connecting the database of mongodb
    print 'Connecting...'
    try:
        client = MongoClient('localhost', 27017)
        db_name = "beacon_nav"
        db = client[db_name]
    except ConnectionFailure, e:
        sys.stderr.write('Could not connection to mongodb: %s' % e)
        sys.exit(1)
    print 'connection successful!\n'

    init_plot_coordinator()

    # init some variable
    #build_id = "BKKJDS000001"
    #build_id = "CDFSKEQDQ000001"
    #build_id = "SHSZCYY000001"
    build_id = "CDLTK000002"
    floor_index = "-1"
    plt.title(build_id)


    # draw the floor plane data pic
    collect_name = "plane_collection"
    print 'Draw the plane picture\n'
    color_p = 'g'
    draw_plane_data(collect_name, build_id, floor_index, color_p)

    # draw the pass data
    collect_name = "pass_collection"
    print 'Draw the pass picture\n'
    draw_pass_data(collect_name, build_id, floor_index)

    # draw the  node data
    collect_name = "node_collection"
    print 'Draw the node picture\n'
    draw_node_data(collect_name, build_id, floor_index)

    # draw the  link data
    collect_name = "link_collection"
    print 'Draw the link picture\n'
    color_l = 'k:'
    draw_link_data(collect_name, build_id, floor_index, color_l)

    # draw the floor border and building border
    fl_col_name = "floor_collection"
    bd_col_name = "bd_collection"
    cur_bd_id = build_id
    cur_fl_index = floor_index
    draw_border_data(fl_col_name, bd_col_name, cur_bd_id, cur_fl_index)

    # read the GPS tracker
    read_gps_list = []
    gps_file_name = 'OnePlus_position2.txt'
    read_gps_list = read_gps_file(gps_file_name)
    #draw_gps_pic(read_gps_list)

    plt.show()

    client.close()
