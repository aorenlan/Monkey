import json
import os
import re
import subprocess
import sys
from datetime import time, datetime
from time import sleep
from wsgiref.validate import validator
import itchat

class MonkeyScreen:
    def __init__(self, devices):
        self.devices = devices
        self.now = str(datetime.now().strftime('%Y-%m-%d %H:%M')[:-1])+"0"
        self.now_sec = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    ##获取设备多台设备号列表
    def get_devices(self):
        str_init = ' '
        all_info = os.popen('adb devices').readlines()
        print('adb devices 输出的内容是：', all_info)
        for i in range(len(all_info)):
            str_init += all_info[i]
        devices_name = re.findall('\n(.+?)\t', str_init, re.S)
        print('所有设备名称：\n', devices_name)
        return devices_name

    def run_monkey(self, device):
        print(type(device))
        for i in device:
            print(i)
            os.popen("adb -s " + i + " shell monkey 1 -p com.chaozh.iReaderFree -v-v-v -s 2 -throttle 500")
        pass

    def monkey_screen(self, device):
        os.popen("adb -s "+ device +" shell screenrecord  --time-limit 60 /sdcard/"+self.now_sec+".mp4")

    def check_log(self, device):#传单个值
        log = os.popen("adb -s "+ device +" logcat -v time | findstr " + self.now)
        if "ANR" or "CRASH" in log:
            os.popen("adb -s "+device+" pull /sdcard/"+self.now_sec+"")
            os.popen("adb -s "+device+" rm /sdcard/"+self.now_sec+"")
            return False

    def delete_video(self):
        os.popen("adb shell rm")
        pass

    def create_video_doc(self):
        check_res = os.popen("adb shell ls /sdcard/monkeyVideo")
        if "No such file or directory" in check_res:
            os.popen("adb shell mkdir /sdcard/monkeyVideo")
        else:
            return "文件夹已存在"

    @itchat.msg_register(itchat.content.TEXT)
    def text_reply(msg):
        # print(msg)
        flag = 0
        # 发送内容
        message = msg['Text']
        # 接收者
        toName = msg['ToUserName']
        print(toName)

        itchat.send_video('要发送的视频路径和视频名',"filehelper")


if __name__ == "__main__":

    itchat.auto_login(True)
    itchat.send('hello', "filehelper")
    itchat.run()

    res = sys.argv
    newMonkey = MonkeyScreen()
    newMonkey.run_monkey(newMonkey.get_devices())
    while 1:
        # sleep(2)
        devices = newMonkey.get_devices()
        for device_screen in devices:
            newMonkey.monkey_screen(device_screen)

            newMonkey.check_log(i)
    # print(str(datetime.now().strftime('%Y-%m-%d %H:%M')[:-1]+"0"))

    pass
