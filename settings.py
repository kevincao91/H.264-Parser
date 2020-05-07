import tkinter
import tkinter.messagebox
import os
import sys
import platform
import json

# 设置VLC库路径，需在import vlc之前
os.environ['PYTHON_VLC_MODULE_PATH'] = r"./lib/vlc-3.0.8-win64"
# os.environ['PYTHON_VLC_LIB_PATH'] = r"./lib/vlc-3.0.8-win64/libvlc.dll"
import vlc


class Settings:
    # 配置程序所有的设置数据
    def __init__(self):
        #  初始化程序的设置
        self.display_info = None
        self.display_index = 0
        # 系统程序路径
        self.pro_path_list = [r'./lib/ffmpeg.exe',
                              r'./lib/FlvParser.exe',
                              r'./lib/vlc-3.0.8-win64/vlc.exe',
                              r'./lib/H264/码流测试软件.exe',
                              r'./lib/Bitrate Viewer 2.3/BitrateViewer.exe']
        # 外部配置文件路径
        self.outer_config_file_path = './lib/configs.txt'
        # 默认值
        self.config_dict = {"ip": "192.168.9.95",
                            "user": "swjtu-9423",
                            "pswd": "9423",
                            "path": "/home/swjtu-9423/http_test/https_test_v%d/ret/f_record.txt",
                            "factory": "undefined",
                            "model": "undefined",
                            "parameter": "undefined",
                            "count": "undefined",
                            "factory_d": {"1": "undefined", },
                            "parameter_d": {"1": "undefined", },
                            "count_d": {"1": "undefined", },
                            "is_test": "False"}

    # GUI上显示的滚动行
    def print_gui(self, string):
        self.display_info.insert(self.display_index, string)
        self.display_info.see(self.display_index)
        self.display_info.select_clear(0, 'end')
        self.display_info.select_set(self.display_index)
        self.display_info.update()
        self.display_index += 1

    # 前提条件检查
    def sys_log_check(self):
        # 显示信息
        string = '系统自检中 ... ...'
        self.print_gui(string)
        # 判断各类表是否存在
        for pro_path in self.pro_path_list:
            if os.path.exists(pro_path):
                string = '存在文件：' + pro_path
                # self.print_gui(string)
            else:
                print('have no ' + pro_path + '!')
                string = '缺失文件：' + pro_path
                self.print_gui(string)
                tkinter.messagebox.showerror(title='错误', message=string)  # 提出错误对话窗
                sys.exit()
        # 显示信息
        string = '系统自检中 ... ... 成功！'
        self.print_gui(string)

    # 加载外部配置文件
    def load_outer_configs(self):
        # 显示信息
        string = '加载外部配置 ... ...'
        self.print_gui(string)
        # 判断是否存在
        if os.path.exists(self.outer_config_file_path):
            # string = '存在外部配置文件 ... ...'
            # self.print_gui(string)
            # 加载json配置文件
            f = open(self.outer_config_file_path, encoding="gbk")
            outer_dic = json.load(f)
            print(outer_dic)
            for key in outer_dic:
                value = outer_dic[key]
                string = '加载外部配置 ... ... %s: %s' % (key, value)
                self.print_gui(string)
            self.config_dict.update(outer_dic)
        else:
            string = '缺少外部配置 ... ... 已加载默认设置。'
            self.print_gui(string)
        # 显示信息
        string = '加载外部配置 ... ... 成功！'
        self.print_gui(string)
        string = '系统自检成功，载入数据完成！请完成 <测试配置> 后开始测试'
        self.print_gui(string)


class Player:
    """
        args:设置 options
    """

    def __init__(self, *args):
        if args:
            instance = vlc.Instance(*args)
            self.media = instance.media_player_new()
        else:
            self.media = vlc.MediaPlayer()

    # 设置待播放的url地址或本地文件路径，每次调用都会重新加载资源
    def set_uri(self, uri):
        self.media.set_mrl(uri)

    # 播放 成功返回0，失败返回-1
    def play(self, path=None):
        if path:
            self.set_uri(path)
            return self.media.play()
        else:
            return self.media.play()

    # 暂停
    def pause(self):
        self.media.pause()

    # 恢复
    def resume(self):
        self.media.set_pause(0)

    # 停止
    def stop(self):
        self.media.stop()

    # 释放资源
    def release(self):
        return self.media.release()

    # 是否正在播放
    def is_playing(self):
        return self.media.is_playing()

    # 已播放时间，返回毫秒值
    def get_time(self):
        return self.media.get_time()

    # 拖动指定的毫秒值处播放。成功返回0，失败返回-1 (需要注意，只有当前多媒体格式或流媒体协议支持才会生效)
    def set_time(self, ms):
        return self.media.get_time()

    # 音视频总长度，返回毫秒值
    def get_length(self):
        return self.media.get_length()

    # 获取当前音量（0~100）
    def get_volume(self):
        return self.media.audio_get_volume()

    # 设置音量（0~100）
    def set_volume(self, volume):
        return self.media.audio_set_volume(volume)

    # 返回当前状态：正在播放；暂停中；其他
    def get_state(self):
        state = self.media.get_state()
        if state == vlc.State.Playing:
            return 1
        elif state == vlc.State.Paused:
            return 0
        else:
            return -1

    # 当前播放进度情况。返回0.0~1.0之间的浮点数
    def get_position(self):
        return self.media.get_position()

    # 拖动当前进度，传入0.0~1.0之间的浮点数(需要注意，只有当前多媒体格式或流媒体协议支持才会生效)
    def set_position(self, float_val):
        return self.media.set_position(float_val)

    # 获取当前文件播放速率
    def get_rate(self):
        return self.media.get_rate()

    # 设置播放速率（如：1.2，表示加速1.2倍播放）
    def set_rate(self, rate):
        return self.media.set_rate(rate)

    # 设置宽高比率（如"16:9","4:3"）
    def set_ratio(self, ratio):
        self.media.video_set_scale(0)  # 必须设置为0，否则无法修改屏幕宽高
        self.media.video_set_aspect_ratio(ratio)

    # 设置窗口句柄
    def set_window(self, wm_id):
        if platform.system() == 'Windows':
            self.media.set_hwnd(wm_id)
        else:
            self.media.set_xwindow(wm_id)

    # 注册监听器
    def add_callback(self, event_type, callback):
        self.media.event_manager().event_attach(event_type, callback)

    # 移除监听器
    def remove_callback(self, event_type, callback):
        self.media.event_manager().event_detach(event_type, callback)
