import sys
import subprocess


def get_camera_name(camera_name):
    cmd = 'system_profiler SPCameraDataType | grep "^    [^ ]" | sed "s/    //" | sed "s/://" '
    res = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    ret = res.stdout.decode('utf-8')
    camera_list = list(filter(lambda a: a != "", ret.split('\n')))
    # print(camera_list)

    camera_list = []

    for index, row in enumerate(camera_list):
        if row is "FaceTime HD Camera":
            continue
        camera_list.append(index)
        print(index, row)
        # if row.find(camera_name) != -1:
        #   return index

    # raise Exception('no camera')
    return camera_list


get_camera_name('USB')
