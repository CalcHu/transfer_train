import connection
import config
import time


def query():
    start_station = input('请输入出发站名: ')
    end_station = input('请输入目的地站名：')
    is_transfer = input('是否需要中转：0，不需要；1，需要')
    if is_transfer in ['1']:
        transfer_station = input('请输入中转站名：')
    else:
        transfer_station = None

    print('st='+start_station)
    print('end='+end_station)
    station_dict = get_station_dict()
    check_station_available(station_dict, start_station, end_station, transfer_station)
    print_str = ''
    if is_transfer == '1':
        railway_info1 = get_railway_info(station_dict[start_station], station_dict[transfer_station])['data']['datas']
        railway_info2 = get_railway_info(station_dict[transfer_station], station_dict[end_station])['data']['datas']

        arrive_time1 = {}
        start_time2 = {}

        railway_info_dict1 = {}
        railway_info_dict2 = {}

        for i in railway_info1:
            hour_str, min_str = i['arrive_time'] .split(':')
            arrive_time1[i['station_train_code']] = 60*int(hour_str) + int(min_str)
            railway_info_dict1[i['station_train_code']] = i
        for i in railway_info2:
            hour_str, min_str = i['arrive_time'] .split(':')
            start_time2[i['station_train_code']] = 60*int(hour_str) + int(min_str)
            railway_info_dict2[i['station_train_code']] = i

        print_str += "{}    {}    {}    {}    {}    {}    {}    {}   {}".format('始发站', '出发时间', '车次',
                                                                                '终到时间', '中转站', '出发时间',
                                                                                '车次', '终到时间', '终到站')+"\n"
        for j in railway_info_dict1:
            for k in railway_info_dict2:
                delta = start_time2[k] - arrive_time1[j]
                if railway_info_dict1[j]['to_station_name'] == railway_info_dict2[k]['start_station_name'] and (((delta > 10) and (delta < 90)) or ((delta+1440 > 10 and delta+1440 < 90))):
                    print_str += "{}    {}    {}    {}    {}    {}    {}    {}   {}\n".format(
                        railway_info_dict1[j]['start_station_name'],
                        railway_info_dict1[j]['start_time'],
                        railway_info_dict1[j]['station_train_code'],
                        railway_info_dict1[j]['arrive_time'],
                        railway_info_dict1[j]['to_station_name'],
                        railway_info_dict2[k]['start_time'],
                        railway_info_dict2[k]['station_train_code'],
                        railway_info_dict2[k]['arrive_time'],
                        railway_info_dict2[k]['end_station_name'],
                    )

    if is_transfer == '0':
        railway_info = get_railway_info(station_dict[start_station], station_dict[end_station])['data']['datas']
        print_str += '{}    {}    {}    {}    {}'.format('始发站', '出发时间', '车次', '终到时间', '终点站') + "\n"
        for i in railway_info:
            print_str += '{}    {}    {}    {}    {}'.format(i['start_station_name'],
                                                             i['start_time'],
                                                             i['station_train_code'],
                                                             i['arrive_time'],
                                                             i['to_station_name'])
            print_str += "\n"

    print(print_str)


def check_station_available(station_dict, *args):
    for i in args:
        if i is not None and i not in station_dict:
            print(i + 'is not a legal station name')
            exit()


def get_station_dict():
    station_url = config.url_base + '/resources/js/framework/station_name.js'
    station_vars = connection.request_server(station_url, 'get', 'text')
    station_str = station_vars[21:-2]
    _list = station_str.split('@')
    return dict(i.split('|')[1:3] for i in _list)


def get_railway_info(start_station, end_station):
    query_uri = config.url_base + '/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'\
        .format(time.strftime('%Y-%m-%d', time.localtime(time.time()+86400)), start_station, end_station)
    return connection.request_server(query_uri)

if __name__ == '__main__':
    query()
