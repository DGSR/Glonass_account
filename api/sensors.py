import csv
import ast
import json
import time
from copy import deepcopy
from pathlib import Path

from api.api_class import GSApi
from api.sensor_schema import SensorSchema


def read_csv(filename, command=False):
    """
    read csv template generated by GlonassSoft
    start from sensors
    finish on templates
    validate data with Sensor schema
    :param filename:
    :return: list of dicts (sensors)
    """
    print(filename)
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        raw_csv = []
        for rows in reader:
            if rows == ['sensors']:
                continue
            if rows == ['templates']:
                break
            print(rows)
            raw_csv.append(rows)

        res = []

        for rows in raw_csv[1:]:
            res.append({index: value for index, value in zip(raw_csv[0], rows)})
        data = []
        for i in res:
            temp = deepcopy(i)
            schema = SensorSchema()
            if not command:
                temp['custom'] = json.loads(temp['custom'])
                temp['gradesTables'] = json.loads(temp['gradesTables'])
                # for j in temp['gradesTables']:
                #     j['updateUserName'] = 'trajectoryspb'

            temp = schema.load(temp)
            t = str(temp['normalState'])
            temp['normalState'] = t[0].lower() + t[1:]
            temp['id'] = None
            data.append(temp)
        return data


def read_json(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    return data


# def add_sensors_to_object(name):  # ign, dut, block):
#     base_path = '/home/dev/Рабочий стол/Yandex.Disk/Загрузки/GLONASSSoft/Телтоника/'
#     out_path = str(Path(__file__).resolve().parent.parent) + '/JSONTemplates/'
#     base_name = 'Телтоника '
#     base_extension = '.csv'
#     sensors = []
#     commands = []
#
#     filename = base_path + base_name + name + base_extension
#     sensors.extend(read_csv(filename))
#
#     with open(base_path + base_name + name + '.json', 'w') as f:
#         json.dump(sensors, f, ensure_ascii=False)


def add_sensors_to_object(ign, dut, block):
    # base_path = '/home/dev/Рабочий стол/Yandex.Disk/Загрузки/GLONASSSoft/Телтоника/'
    base_path = str(Path(__file__).resolve().parent.parent) + '/JSON prod/'
    base_name = 'Телтоника '
    base_extension = '.json'
    sensors = []
    commands = []
    vehicle_id = '26c9e784-5dbf-4fd6-981c-857d715c33ab'
    commands_fields = {
        'OwnerGuid': 'a29f3c54-4d06-4964-a80e-8bc6bcd68e30',
        'VehicleGuid': vehicle_id
    }

    if ign != '':
        ign_filename = base_path + base_name + 'зажигание ' + ign + base_extension
        sensors.extend(read_json(ign_filename))

    if dut != 'Без ДУТ':
        dut_filename = base_path + base_name + dut + base_extension
        sensors.extend(read_json(dut_filename))

        if dut == 'CAN':
            command_filename = base_path + base_name + 'команды CAN' + base_extension
            commands.extend(read_json(command_filename))

    if block != 'Без блокировки':
        block_filename = base_path + base_name + block + base_extension
        sensors.extend(read_json(block_filename))
        command_filename = base_path + base_name + 'команды на блокировку' + base_extension
        commands.extend(read_json(command_filename))

        commands = [{**i, **commands_fields} for i in commands]
    res = None

    api = GSApi()
    res = api.add_sensor(vehicle_id, sensors)
    print(res)
    time.sleep(1)
    res = api.edit_commands(commands)

    return res


