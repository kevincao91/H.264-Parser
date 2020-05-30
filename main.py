from settings import Settings, Player
import csv
import os
import tkinter
import tkinter.ttk
import tkinter.messagebox
import tkinter.font
import time
import subprocess
import shutil
import paramiko
import json

# 设置VLC库路径，需在import vlc之前
os.environ['PYTHON_VLC_MODULE_PATH'] = r"./lib/vlc-3.0.8-win64"
# os.environ['PYTHON_VLC_LIB_PATH'] = r"./lib/vlc-3.0.8-win64/libvlc.dll"
import vlc


# img1_gif = None
# img2_gif = None


class AppGUI(object):
    def __init__(self):
        # 初始化参数
        self.pwd = os.getcwd()
        self.global_set = Settings()
        # 创建主窗口,用于容纳其它组件
        self.root_window = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root_window.title("贵州省高速公路视频云联网码流测试软件")
        self.root_window.geometry('1000x660+200+20')
        self.root_window.minsize(1000, 640)
        # self.root_window.resizable(0, 0)  # 防止用户调整尺寸
        ico_file = os.path.join(self.pwd, 'lib', '1.ico')
        self.root_window.iconbitmap(ico_file)
        self.root_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        # 创建配置窗口,用于容纳其它组件
        self.config_window = tkinter.Tk()
        self.config_window.geometry('666x370+300+100')
        self.config_window.minsize(666, 370)
        self.config_window.resizable(0, 0)  # 防止用户调整尺寸
        self.config_window.iconbitmap(ico_file)
        self.config_window.withdraw()
        self.config_window.protocol("WM_DELETE_WINDOW", self.subwin_on_closing)

        # 预定义显示对象
        self.display_info = None
        self.str_obj_1 = None
        self.str_obj_2 = None
        self.str_obj_3 = None
        self.button_1 = None
        self.button_2 = None
        self.button_3 = None
        self.button_4 = None
        self.button_5 = None
        self.min_entry = None
        self.avg_entry = None
        self.max_entry = None
        self.result_entry = None
        self.video_button_1 = None
        self.video_button_2 = None
        self.video_button_3 = None
        self.rtmp_url_combox_list = None
        self.sample_time_combox_list = None
        self.factory_combox_list = None
        self.parameter_combox_list = None
        self.count_combox_list = None
        self.canvas_video = None
        self.config_entry_1 = None
        self.config_entry_2 = None
        self.config_entry_3 = None
        self.config_entry_4 = None
        self.config_entry_5 = None
        self.config_entry_6 = None
        # copy config
        self.config_dict = self.global_set.config_dict
        # subprocess 消除CMD终端显示
        self.st = subprocess.STARTUPINFO
        self.st.dwFlags = subprocess.STARTF_USESHOWWINDOW
        self.st.wShowWindow = subprocess.SW_HIDE
        # video
        self.player = Player()
        # 变量
        self.save_dir_root = './data_records/'
        self.rtmp_url_list = []
        self.vinfo_1 = ""
        self.vinfo_2 = ""
        self.vinfo_3 = ""
        self.format = "播放状态：%-18s 播放时间：%12s s"

    # root窗口布局
    def root_gui_arrange(self):
        # 设置顶级窗体的行列权重，否则子组件的拉伸不会填充整个窗体
        self.root_window.rowconfigure(0, weight=1)
        self.root_window.rowconfigure(1, weight=4)
        self.root_window.rowconfigure(2, weight=1)
        self.root_window.rowconfigure(3, weight=1)
        self.root_window.rowconfigure(4, weight=4)
        self.root_window.rowconfigure(5, weight=1)
        self.root_window.rowconfigure(6, weight=5)
        self.root_window.columnconfigure(0, weight=1)
        self.root_window.columnconfigure(1, weight=2)
        # 指定字体名称、大小、样式
        ft0 = tkinter.font.Font(family='Fixdsys', size=12, weight=tkinter.font.BOLD)
        ft1 = tkinter.font.Font(family='Fixdsys', size=10, weight=tkinter.font.BOLD)
        ft2 = tkinter.font.Font(size=22, weight=tkinter.font.BOLD, underline=1)

        # 设定图片
        # global img1_gif
        # global img2_gif
        # img1_gif = tkinter.PhotoImage(file=r'./lib/swjtu.gif')
        # img_canvas_1 = tkinter.Canvas(self.root_window, width=200, height=200)
        # label_img_1 = tkinter.Label(self.root_window, image=img1_gif)
        # img2_gif = tkinter.PhotoImage(file=r'./lib/swjtu2.gif')
        # label_img_2 = tkinter.Label(self.root_window, image=img2_gif)

        # 设定标签
        step1_group = tkinter.LabelFrame(self.root_window, font=ft0, text="步骤 1:-> 获取RTMP视频流", padx=5, pady=5)
        step2_group = tkinter.LabelFrame(self.root_window, font=ft0, text="步骤 2:-> 提取H264码流", padx=5, pady=5)
        step3_group = tkinter.LabelFrame(self.root_window, font=ft0, text="步骤 3:-> 分析H264码流", padx=5, pady=5)
        step4_group = tkinter.LabelFrame(self.root_window, font=ft0, text="步骤 4:-> 分析H264码率", padx=5, pady=5)
        step5_group = tkinter.LabelFrame(self.root_window, text="--预览信息--", padx=5, pady=5)
        step6_group = tkinter.LabelFrame(step5_group, text="", padx=5, pady=5)

        # 设定标签
        show_label_0 = tkinter.Label(self.root_window, font=ft2, text='贵州省高速公路视频云联网码流测试软件')
        show_label_1 = tkinter.Label(step1_group, text='RTMP视频流采集地址->')
        show_label_2_0 = tkinter.Label(step1_group, text='RTMP视频流捕获时长->')
        show_label_2 = tkinter.Label(step1_group, text='请点击按钮获取RTMP视频流->')
        show_label_3 = tkinter.Label(step2_group, text='请点击按钮提取H264码流->')
        show_label_4 = tkinter.Label(step3_group, text='请点击按钮分析H264码流->')
        show_label_5 = tkinter.Label(step4_group, text='请点击按钮分析H264码率->')
        show_label_6_0 = tkinter.Label(step4_group, text='Min↓')
        show_label_6_1 = tkinter.Label(step4_group, text='Max↓')
        show_label_6_2 = tkinter.Label(step4_group, text='Avg↓ ->')
        show_label_7 = tkinter.Label(self.root_window, text='--系统信息--')
        show_label_8 = tkinter.Label(self.root_window,
                                     text='--版权信息-- Copyright '
                                          '© 2020 Southwest Jiaotong University. All rights reserved.')
        self.str_obj_1 = tkinter.StringVar()
        text = self.format % (self.vinfo_1 + self.vinfo_2, self.vinfo_3)
        self.str_obj_1.set(text)
        video_player_info_1 = tkinter.Label(step6_group, width=46, textvariable=self.str_obj_1)
        # 下拉列表
        self.rtmp_url_combox_list = tkinter.ttk.Combobox(step1_group, width=85)  # 初始化
        self.rtmp_url_combox_list.insert(0, '请输入或点击右侧箭头选择需要测试的视频流地址')

        self.rtmp_url_combox_list.bind('<<ComboboxSelected>>', self.rtmp_url_combox_list_change)
        self.rtmp_url_combox_list.bind('<Return>', self.rtmp_url_combox_list_change)
        # self.rtmp_url_combox_list.bind('<FocusOut>', self.rtmp_url_combox_list_change)

        self.sample_time_combox_list = tkinter.ttk.Combobox(step1_group, width=30)  # 初始化
        self.sample_time_combox_list.insert(0, '请点击右侧箭头选择视频流采集时长')
        self.sample_time_combox_list["values"] = ("10s", "30s", "60s", "90s")
        self.sample_time_combox_list.bind('<<ComboboxSelected>>', self.sample_time_combox_list_change)
        self.sample_time_combox_list.bind('<Return>', self.sample_time_combox_list_change)

        # 设定输入框
        self.min_entry = tkinter.Entry(step4_group, width=5)
        self.avg_entry = tkinter.Entry(step4_group, width=5)
        self.max_entry = tkinter.Entry(step4_group, width=5)
        self.result_entry = tkinter.Entry(step4_group, width=11)

        # 设定按钮
        self.button_1 = tkinter.Button(step1_group, font=ft1, text='开始捕获！', command=self.get_flv_btn_fun)
        self.button_2 = tkinter.Button(step2_group, font=ft1, text='开始提取！', command=self.get_h264_btn_fun)
        self.button_3 = tkinter.Button(step3_group, font=ft1, text='分析码流！', command=self.parse_h264code_btn_fun)
        self.button_4 = tkinter.Button(step4_group, font=ft1, text='分析码率！', command=self.parse_h264bitrate_btn_fun)
        # self.button_5 = tkinter.Button(step4_group, font=ft1, text='计算波动！', command=self.calculate_btn_fun)
        self.button_5 = tkinter.Button(step4_group, font=ft1, text='计算波动！', command=self.calculate_new_btn_fun)
        # 创建一个Listbox
        self.display_info = tkinter.Listbox(self.root_window, height=6, width=50)
        self.global_set.display_info = self.display_info
        # 创建匹配的Scrollbar
        y_scrollbar_1 = tkinter.Scrollbar(self.root_window)
        self.display_info.config(yscrollcommand=y_scrollbar_1.set)
        y_scrollbar_1.config(command=self.display_info.yview)
        # 创建视频画布
        # self.canvas_video = tkinter.Canvas(step5_group, width=466, height=210, bg="black")
        self.canvas_video = tkinter.Canvas(step5_group, bg="black")
        self.video_button_1 = tkinter.Button(step5_group, width=4, text="播放", command=lambda: self.video_click(0))
        self.video_button_2 = tkinter.Button(step5_group, width=4, text="暂停", command=lambda: self.video_click(1))
        self.video_button_3 = tkinter.Button(step5_group, width=4, text="停止", command=lambda: self.video_click(2))

        # 布局
        show_label_0.grid(row=0, column=0, columnspan=2, padx=5, ipadx=5, pady=5, ipady=5, sticky=tkinter.NSEW)
        # step1_group
        step1_group.grid(row=1, column=0, columnspan=2, padx=5, ipadx=5, pady=5, ipady=5, sticky=tkinter.NSEW)
        step1_group.rowconfigure(0, weight=1)
        step1_group.rowconfigure(1, weight=1)
        step1_group.columnconfigure(0, weight=1)
        step1_group.columnconfigure(1, weight=1)
        step1_group.columnconfigure(2, weight=1)
        step1_group.columnconfigure(3, weight=4)
        step1_group.columnconfigure(4, weight=1)
        show_label_1.grid(row=0, column=0, padx=3, ipadx=3, pady=0, ipady=5, sticky=tkinter.NSEW)
        self.rtmp_url_combox_list.grid(row=0, column=1, columnspan=4, padx=3, ipadx=3, pady=0, ipady=5,
                                       sticky=tkinter.NSEW)
        show_label_2_0.grid(row=1, column=0, padx=3, ipadx=3, pady=0, ipady=5, sticky=tkinter.NSEW)
        self.sample_time_combox_list.grid(row=1, column=1, columnspan=2, padx=3, ipadx=3, pady=0, ipady=5,
                                          sticky=tkinter.NSEW)
        show_label_2.grid(row=1, column=3, padx=3, ipadx=3, pady=0, ipady=5, sticky=tkinter.N + tkinter.S + tkinter.E)
        self.button_1.grid(row=1, column=4, padx=3, ipadx=3, pady=0, ipady=5, sticky=tkinter.NSEW)
        # step2_group
        step2_group.grid(row=2, column=0, padx=5, ipadx=5, pady=5, ipady=5, sticky=tkinter.NSEW)
        step2_group.rowconfigure(0, weight=1)
        step2_group.columnconfigure(0, weight=1)
        step2_group.columnconfigure(1, weight=3)
        show_label_3.grid(row=0, column=0, padx=3, ipadx=3, pady=0, ipady=0, sticky=tkinter.NSEW)
        self.button_2.grid(row=0, column=1, padx=3, ipadx=3, pady=0, ipady=0, sticky=tkinter.NSEW)
        # step3_group
        step3_group.grid(row=3, column=0, padx=5, ipadx=5, pady=5, ipady=5, sticky=tkinter.NSEW)
        step3_group.rowconfigure(0, weight=1)
        step3_group.columnconfigure(0, weight=1)
        step3_group.columnconfigure(1, weight=3)
        show_label_4.grid(row=0, column=0, padx=3, ipadx=3, pady=0, ipady=0, sticky=tkinter.NSEW)
        self.button_3.grid(row=0, column=1, padx=3, ipadx=3, pady=0, ipady=0, sticky=tkinter.NSEW)
        # step4_group
        step4_group.grid(row=4, column=0, padx=5, ipadx=5, pady=5, ipady=5, sticky=tkinter.NSEW)
        step4_group.rowconfigure(0, weight=1)
        step4_group.rowconfigure(1, weight=1)
        step4_group.rowconfigure(2, weight=1)
        step4_group.columnconfigure(0, weight=1)
        step4_group.columnconfigure(1, weight=1)
        step4_group.columnconfigure(2, weight=1)
        step4_group.columnconfigure(3, weight=1)
        show_label_5.grid(row=0, column=0, columnspan=2, padx=3, ipadx=3, pady=0, ipady=0, sticky=tkinter.NSEW)
        self.button_4.grid(row=0, column=2, columnspan=2, padx=3, ipadx=3, pady=0, ipady=0, sticky=tkinter.NSEW)
        show_label_6_0.grid(row=1, column=0, padx=3, ipadx=3, pady=0, ipady=0, sticky=tkinter.NSEW)
        show_label_6_1.grid(row=1, column=1, padx=3, ipadx=3, pady=0, ipady=0, sticky=tkinter.NSEW)
        show_label_6_2.grid(row=1, column=2, padx=3, ipadx=3, pady=0, ipady=0, sticky=tkinter.NSEW)
        self.button_5.grid(row=1, column=3, padx=3, ipadx=3, pady=0, ipady=0, sticky=tkinter.NSEW)
        self.min_entry.grid(row=2, column=0, padx=3, ipadx=3, pady=0, ipady=0, sticky=tkinter.NSEW)
        self.max_entry.grid(row=2, column=1, padx=3, ipadx=3, pady=0, ipady=0, sticky=tkinter.NSEW)
        self.avg_entry.grid(row=2, column=2, padx=3, ipadx=3, pady=0, ipady=0, sticky=tkinter.NSEW)
        self.result_entry.grid(row=2, column=3, padx=3, ipadx=3, pady=0, ipady=0, sticky=tkinter.NSEW)
        # step5_group
        step5_group.grid(row=2, column=1, rowspan=3, padx=5, ipadx=5, pady=5, ipady=5, sticky=tkinter.NSEW)
        step5_group.rowconfigure(0, weight=5)
        step5_group.rowconfigure(1, weight=1)
        step5_group.columnconfigure(0, weight=1)
        step5_group.columnconfigure(1, weight=1)
        step5_group.columnconfigure(2, weight=1)
        step5_group.columnconfigure(3, weight=3)
        step5_group.columnconfigure(4, weight=3)
        self.canvas_video.grid(row=0, column=0, columnspan=5, padx=3, ipadx=3, pady=0, ipady=0, sticky=tkinter.NSEW)
        self.player.set_window(self.canvas_video.winfo_id())
        self.video_button_1.grid(row=1, column=0, padx=3, ipadx=3, pady=0, ipady=0, sticky=tkinter.NSEW)
        self.video_button_2.grid(row=1, column=1, padx=3, ipadx=3, pady=0, ipady=0, sticky=tkinter.NSEW)
        self.video_button_3.grid(row=1, column=2, padx=3, ipadx=3, pady=0, ipady=0, sticky=tkinter.NSEW)
        step6_group.grid(row=1, column=3, columnspan=2, padx=3, ipadx=3, pady=0, ipady=0, sticky=tkinter.NSEW)
        video_player_info_1.grid(row=0, column=0, padx=3, ipadx=3, pady=0, ipady=0, sticky=tkinter.NSEW)
        # 底部
        show_label_7.grid(row=5, column=0, padx=5, sticky=tkinter.W)
        show_label_8.grid(row=5, column=1, padx=5, sticky=tkinter.W)
        self.display_info.grid(row=6, column=0, columnspan=2, padx=5, ipadx=5, pady=5, ipady=5, sticky=tkinter.NSEW)
        y_scrollbar_1.grid(row=6, column=1, padx=0, ipadx=0, pady=5, ipady=5, sticky=tkinter.N + tkinter.S + tkinter.E)
        # 图
        # img_canvas_1.grid(row=0, column=1, sticky=tkinter.NSEW)
        # pp = img_canvas_1.create_image(2, 2, image=img1_gif, anchor=tkinter.CENTER)
        # img_canvas_1.tag_raise(pp)
        # label_img_2.grid(row=1, column=1, rowspan=3)

        # 改变按键状态
        self.button_contrl(-3)

        # 创建菜单项
        menu_bar = tkinter.Menu(self.root_window)
        # 下拉菜单1
        menu_c1 = tkinter.Menu(self.root_window, tearoff=0)
        # 添加的是下拉菜单的菜单项
        menu_c1.add_command(label='步骤 1:-> 获取RTMP视频流', command=self.get_flv_btn_fun)
        menu_c1.add_command(label='步骤 2:-> 提取H264码流', command=self.get_h264_btn_fun)
        menu_c1.add_command(label='步骤 3:-> 分析H264码流', command=self.parse_h264code_btn_fun)
        menu_c1.add_command(label='步骤 4:-> 分析H264码率', command=self.parse_h264bitrate_btn_fun)
        # 下拉菜单2
        menu_c2 = tkinter.Menu(self.root_window, tearoff=0)
        # 添加的是下拉菜单的菜单项
        menu_c2.add_command(label='测试参数设置', command=self.config_menu_fun)
        menu_c2.add_command(label='服务器连接测试', command=self.server_ping_test)
        menu_c2.add_command(label='刷新RTMP视频流地址', command=self.get_rtmp_url_menu_fun)
        # 下拉菜单3
        menu_c3 = tkinter.Menu(self.root_window, tearoff=0)
        # 添加的是下拉菜单的菜单项
        menu_c3.add_command(label='访问RTMP流媒体捕获文件夹', command=self.open_output_dir_fun)
        menu_c3.add_command(label='开启VLC播放器', command=self.open_vlc_pro_fun)
        # 下拉菜单4
        menu_c4 = tkinter.Menu(self.root_window, tearoff=0)
        menu_c4.add_command(label='版权信息', command=self.show_info_fun)
        menu_c4.add_command(label='其他说明', command=self.show_info_fun)
        # 功能测试菜单
        # menu_c4.add_command(label='其他说明', command=self.calculate_new_btn_fun)
        # 指明父菜单
        menu_bar.add_cascade(label="测试步骤", menu=menu_c1)
        menu_bar.add_cascade(label="测试配置", menu=menu_c2)
        menu_bar.add_cascade(label="便捷访问", menu=menu_c3)
        menu_bar.add_cascade(label="关于", menu=menu_c4)
        # 菜单实例应用到大窗口中
        self.root_window['menu'] = menu_bar

        # 调整尺寸
        # self.root_window.bind('<Configure>', self.show_win_size)

    # config窗口布局
    def config_gui_arrange(self):
        # 给窗口设置标题内容
        self.config_window.title("测试参数设置")
        # 指定字体名称、大小、样式
        ft0 = tkinter.font.Font(family='Fixdsys', size=12, weight=tkinter.font.BOLD)
        ft1 = tkinter.font.Font(family='Fixdsys', size=10, weight=tkinter.font.BOLD)
        # 设定标签
        step1_group = tkinter.LabelFrame(self.config_window, text="服务器参数", padx=5, pady=5)
        step2_group = tkinter.LabelFrame(self.config_window, text="调试参数", padx=5, pady=5)
        step3_group = tkinter.LabelFrame(self.config_window, text="调试参数", padx=5, pady=5)
        # 设定标签
        show_label_1 = tkinter.Label(step1_group, text='测试服务器IP地址：')
        show_label_2 = tkinter.Label(step1_group, text='测试服务器登录账户：')
        show_label_3 = tkinter.Label(step1_group, text='测试服务器登录密码：')
        show_label_4 = tkinter.Label(step1_group, text='测试服务器接口文件路径：')
        show_label_5 = tkinter.Label(step2_group, text='%-22s' % '测试网关厂商：')
        show_label_6 = tkinter.Label(step2_group, text='%-22s' % '测试设备型号：')
        show_label_7 = tkinter.Label(step2_group, text='%-22s' % '测试码流配置：')
        show_label_8 = tkinter.Label(step2_group, text='%-22s' % '测试设备次数：')
        show_label_test = tkinter.Label(step3_group, text='%-26s' % '测试标志：')
        # 设定输入框
        self.config_entry_1 = tkinter.Entry(step1_group, width=65)
        self.config_entry_1.insert(0, self.config_dict["ip"])
        self.config_entry_2 = tkinter.Entry(step1_group, width=65)
        self.config_entry_2.insert(0, self.config_dict["user"])
        self.config_entry_3 = tkinter.Entry(step1_group, width=65, show="*")
        self.config_entry_3.insert(0, self.config_dict["pswd"])
        self.config_entry_4 = tkinter.Entry(step1_group, width=65)
        self.config_entry_4.insert(0, self.config_dict["path"])
        self.config_entry_5 = tkinter.Entry(step2_group, width=65)
        self.config_entry_5.insert(0, self.config_dict["model"])
        self.config_entry_6 = tkinter.Entry(step3_group, width=65)
        self.config_entry_6.insert(0, self.config_dict["is_test"])
        # 下拉列表
        self.factory_combox_list = tkinter.ttk.Combobox(step2_group, width=62)  # 初始化
        factory_d = self.config_dict["factory_d"]
        self.factory_combox_list["values"] = [str(i) + ' ' + factory_d[str(i)] for i in range(1, len(factory_d) + 1)]
        self.factory_combox_list.current(0)  # 选择第一个
        self.parameter_combox_list = tkinter.ttk.Combobox(step2_group, width=62)  # 初始化
        parameter_d = self.config_dict["parameter_d"]
        self.parameter_combox_list["values"] = [str(i) + ' ' + parameter_d[str(i)] for i in
                                                range(1, len(parameter_d) + 1)]
        self.parameter_combox_list.current(0)  # 选择第一个
        self.count_combox_list = tkinter.ttk.Combobox(step2_group, width=62)  # 初始化
        count_d = self.config_dict["count_d"]
        self.count_combox_list["values"] = [str(i) + ' ' + count_d[str(i)] for i in
                                            range(1, len(count_d) + 1)]
        self.count_combox_list.current(0)  # 选择第一个
        # 设定按钮
        button_1 = tkinter.Button(self.config_window, font=ft1, text='确定', command=self.set_config_btn_fun)
        button_2 = tkinter.Button(self.config_window, font=ft1, text='返回', command=self.back_config_btn_fun)

        # 布局
        # step1_group
        step1_group.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tkinter.W)
        show_label_1.grid(row=0, column=0, padx=5, sticky=tkinter.W)
        self.config_entry_1.grid(row=0, column=1, padx=5, sticky=tkinter.W)
        show_label_2.grid(row=1, column=0, padx=5, sticky=tkinter.W)
        self.config_entry_2.grid(row=1, column=1, padx=5, sticky=tkinter.W)
        show_label_3.grid(row=2, column=0, padx=5, sticky=tkinter.W)
        self.config_entry_3.grid(row=2, column=1, padx=5, sticky=tkinter.W)
        show_label_4.grid(row=3, column=0, padx=5, sticky=tkinter.W)
        self.config_entry_4.grid(row=3, column=1, padx=5, sticky=tkinter.W)
        # step2_group
        step2_group.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tkinter.W)
        show_label_5.grid(row=0, column=0, padx=5, sticky=tkinter.W)
        self.factory_combox_list.grid(row=0, column=1, padx=5, sticky=tkinter.W)
        show_label_6.grid(row=1, column=0, padx=5, sticky=tkinter.W)
        self.config_entry_5.grid(row=1, column=1, padx=5, sticky=tkinter.W)
        show_label_7.grid(row=2, column=0, padx=5, sticky=tkinter.W)
        self.parameter_combox_list.grid(row=2, column=1, padx=5, sticky=tkinter.W)
        show_label_8.grid(row=3, column=0, padx=5, sticky=tkinter.W)
        self.count_combox_list.grid(row=3, column=1, padx=5, sticky=tkinter.W)
        # step3_group
        step3_group.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tkinter.W)
        show_label_test.grid(row=0, column=0, padx=5, sticky=tkinter.W)
        self.config_entry_6.grid(row=0, column=1, padx=5, sticky=tkinter.W)
        # button
        button_1.grid(row=3, column=0, padx=5, sticky=tkinter.E)
        button_2.grid(row=3, column=1, padx=5, sticky=tkinter.W)

    # config窗口布局
    def update_gui_arrange(self):

        # 下拉列表
        factory_d = self.config_dict["factory_d"]
        self.factory_combox_list["values"] = [str(i) + ' ' + factory_d[str(i)] for i in range(1, len(factory_d) + 1)]
        self.factory_combox_list.current(0)  # 选择第一个

        parameter_d = self.config_dict["parameter_d"]
        self.parameter_combox_list["values"] = [str(i) + ' ' + parameter_d[str(i)] for i in
                                                range(1, len(parameter_d) + 1)]
        self.parameter_combox_list.current(0)  # 选择第一个

        count_d = self.config_dict["count_d"]
        self.count_combox_list["values"] = [str(i) + ' ' + count_d[str(i)] for i in
                                            range(1, len(count_d) + 1)]
        self.count_combox_list.current(0)  # 选择第一个

    # 通用 - 创建文件夹
    def mk_dir(self, dir_path):
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        if os.path.exists(dir_path):
            return True
        else:
            return False

    # 通用 - 获得存储文件夹
    def get_record_dir(self):
        string = '%s_%s_%s_%s' % (
            self.config_dict["factory"].split()[-1], self.config_dict["model"].split()[-1],
            self.config_dict["parameter"].split()[-1], self.config_dict["count"].split()[-1])
        save_dir_path = os.path.join(self.save_dir_root, string)
        return save_dir_path

    # 通用 - 存储测试文件
    def save_record_files(self):
        out = os.path.join(self.get_record_dir(), 'parser.h264')
        shutil.move("./output/parser.h264", out)
        out = os.path.join(self.get_record_dir(), 'test.flv')
        shutil.move("./output/test.flv", out)
        out = os.path.join(self.get_record_dir(), 'Stream Info.csv')
        shutil.move("./output/Stream Info.csv", out)
        string = '测试码流记录文件，已保存到%s。' % self.get_record_dir()
        self.global_set.print_gui(string)

    # 主界面 - 流地址检查功能
    def rtmp_url_check(self):
        # rtmp://58.200.131.2:1935/livetv/hunantv
        url_ori = self.rtmp_url_combox_list.get()
        print(url_ori)
        url_out, ipv4_out = None, None
        if " || " in url_ori:
            url = url_ori.split(" || ")[-1]
            if url.startswith("rtmp://"):
                url_out = url
                ipv4_out = url_out.replace("rtmp://", "").split(":")[0]
        else:
            if url_ori.startswith("rtmp://"):
                url_out = url_ori
                ipv4_out = url_out.replace("rtmp://", "").split(":")[0]
            else:
                tkinter.messagebox.showerror('错误', '地址格式错误！请重新输入或选择。')
        return url_out, ipv4_out

    # 主界面 - 采样时间检查功能
    def sample_time_check(self):
        str_ori = self.sample_time_combox_list.get()
        print(str_ori)
        time_out = None
        if "=>  " in str_ori:
            time_str = str_ori.split("=>  ")[-1]
            if time_str.endswith("s"):
                time_out = int(time_str.replace(' s', '').replace('s', ''))
        else:
            if str_ori.endswith("s"):
                time_str = str_ori
                if time_str.endswith("s"):
                    time_out = int(time_str.replace(' s', '').replace('s', ''))
            else:
                tkinter.messagebox.showerror('错误', '采集时间格式错误！请重新输入或选择。')
        return time_out

    # 主界面 - 获取RTMP流功能
    def get_flv_btn_fun(self):
        # 改变按键状态
        self.button_contrl(1, 1)
        # 获取用户输入
        url, _ = self.rtmp_url_check()
        print('url', url)
        sample_time = self.sample_time_check()
        if url and sample_time:
            # 去除旧文件
            if os.path.exists("./output/test.flv"):
                string = '存在历史flv文件，已清除。'
                self.global_set.print_gui(string)
                os.remove("./output/test.flv")
            sh = r'./lib/ffmpeg.exe'
            args = '-i ' + url + ' -acodec copy -vcodec copy -t %d -f flv ./output/test.flv' % sample_time
            try:
                string = '开始执行RTMP流媒体文件捕获命令 ... ...'
                self.global_set.print_gui(string)
                sub_p = subprocess.Popen(sh + ' ' + args, startupinfo=self.st)
                print(sub_p.poll())
                tt = 1
                while sub_p.poll() == None:
                    string = '执行操作用时 %d s' % tt
                    self.global_set.print_gui(string)
                    time.sleep(1)
                    tt += 1
                print('run over!')
                string = 'RTMP流媒体文件捕获完成。'
                self.global_set.print_gui(string)
            except:
                string = 'RTMP流媒体文件获取失败！'
                self.global_set.print_gui(string)
                tkinter.messagebox.showerror('错误', string)
            # check
            if not os.path.exists("./output/test.flv"):
                string = '流媒体文件不存在，请重新获取！'
                self.global_set.print_gui(string)
                tkinter.messagebox.showerror('错误', string)
            else:
                tkinter.messagebox.showinfo('提示', '获取RTMP流媒体文件成功，请继续执行第二步。')
                # 改变按键状态
                self.button_contrl(1)

    # 主界面 - 获取h264流功能
    def get_h264_btn_fun(self):
        # 改变按键状态
        self.button_contrl(2, 1)
        if os.path.exists("./output/parser.h264"):
            string = '存在历史h264文件，已清除。'
            self.global_set.print_gui(string)
            os.remove("./output/parser.h264")
        if not os.path.exists(r'./output/test.flv'):
            string = '缺少捕获的flv文件，请确认或重新执行第一步。'
            self.global_set.print_gui(string)
        else:
            string = '开始执行提取h264文件命令 ... ...'
            self.global_set.print_gui(string)
            sh = r'./lib/FlvParser.exe'
            args = r'./output/test.flv' + ' ./output/output.h264 '
            try:
                sub_p = subprocess.Popen(sh + ' ' + args, startupinfo=self.st)
                tt = 1
                while sub_p.poll() == None:
                    string = '执行操作用时 %d s' % tt
                    self.global_set.print_gui(string)
                    time.sleep(1)
                    tt += 1
                print('run over!')
                string = 'h264文件提取完成。'
                self.global_set.print_gui(string)
            except:
                string = 'h264文件提取失败！'
                self.global_set.print_gui(string)
                tkinter.messagebox.showerror('错误', string)
        # check
        if not os.path.exists("./parser.264"):
            string = 'h264文件不存在，请重新获取！'
            self.global_set.print_gui(string)
            tkinter.messagebox.showerror('错误', string)
        else:
            shutil.move("./parser.264", "./output/parser.h264")
            tkinter.messagebox.showinfo('提示', 'h264文件提取成功，请继续执行第三步。')
            # 改变按键状态
            self.button_contrl(2)

    # 主界面 - 分析h264码流功能
    def parse_h264code_btn_fun(self):
        # 改变按键状态
        self.button_contrl(3, 1)
        if not os.path.exists(r'./output/parser.h264'):
            string = '缺少h264文件，请确认或重新执行上一步。'
            self.global_set.print_gui(string)
            tkinter.messagebox.showerror('错误', string)
        else:
            if os.path.exists(r'./lib/H264/H264Recv.es'):
                string = '存在历史es文件，已清除。'
                self.global_set.print_gui(string)
                os.remove(r'./lib/H264/H264Recv.es')
            string = '导入es文件 ... ...'
            self.global_set.print_gui(string)
            shutil.copy("./output/parser.h264", "./lib/H264/H264Recv.es")
            string = '开始执行h264码流分析程序 ... ...'
            self.global_set.print_gui(string)
            sh = r'./lib/H264/码流测试软件.exe'
            args = r''
            try:
                sub_p = subprocess.Popen(sh + ' ' + args, cwd=r'./lib/H264/')
                tt = 1
                while sub_p.poll() == None:
                    string = '执行操作用时 %d s' % tt
                    tt += 1
                    print(string)
                    time.sleep(1)
                print('run over!')
            except:
                string = 'h264码流分析失败！'
                self.global_set.print_gui(string)
                tkinter.messagebox.showerror('错误', string)
        string = '已结束h264码流分析程序。'
        self.global_set.print_gui(string)
        tkinter.messagebox.showinfo('提示', 'h264码流分析完成，请继续执行第四步。')
        # 改变按键状态
        self.button_contrl(3)

    # 主界面 - 分析h264码率功能
    def parse_h264bitrate_btn_fun(self):
        # 改变按键状态
        self.button_contrl(4, 1)
        if not os.path.exists(r'./output/parser.h264'):
            string = '缺少提取的h264文件，请确认或重新执行第二步。'
            self.global_set.print_gui(string)
            tkinter.messagebox.showerror('错误', string)
        else:
            string = '开始执行h264码率分析程序 ... ...'
            self.global_set.print_gui(string)
            # sh = r'./lib/Bitrate Viewer 2.3/BitrateViewer.exe'
            sh = r'C:\Program Files (x86)\Elecard\Elecard StreamEye Studio\Elecard StreamEye\ESEyeApp_lite.exe'
            args = r''
            try:
                sub_p = subprocess.Popen(sh + ' ' + args, cwd=r'./output/')
                '''
                tt = 1
                while sub_p.poll() == None:
                    string = '执行操作用时 % ds' % tt
                    tt += 1
                    print(string)
                    time.sleep(1)
                print('run over!')
                '''
            except:
                string = 'h264码率分析失败！'
                self.global_set.print_gui(string)
                tkinter.messagebox.showerror('错误', string)
        # string = '已结束h264码率分析程序。'
        # self.global_set.print_gui(string)
        # tkinter.messagebox.showinfo('提示', '提取h264文件成功，可以进行码流分析！')

    # 主界面 - 计算h264码率波动功能
    def calculate_btn_fun(self):
        # 改变按键状态
        self.button_contrl(4, 2)
        string = '开始码率波动计算 ... ...'
        self.global_set.print_gui(string)
        result = -1
        check_flag = True
        try:
            min_value = int(self.min_entry.get())
            avg_value = int(self.avg_entry.get())
            max_value = int(self.max_entry.get())

            if max_value <= avg_value or avg_value <= min_value:
                check_flag = False

            d1 = max_value - avg_value
            d2 = avg_value - min_value
            d = d1 if d1 > d2 else d2
            result = d / avg_value
            print(min_value, avg_value, max_value, d1, d2, d, result)
        except:
            check_flag = False
        # check
        if check_flag:
            result_str = '{:.2%}'.format(result)
            self.result_entry.delete(0, tkinter.END)
            self.result_entry.insert(0, result_str)
            string = '码率波动计算完成，波动率为：%s。' % result_str
            self.global_set.print_gui(string)
            tkinter.messagebox.showinfo('提示', string)
            self.save_record_files()
            string = '已结束所有码流测试内容，请做好记录。\n如需开始新测试，请完成 <测试配置> 后进行。'
            self.global_set.print_gui(string)
            tkinter.messagebox.showinfo('提示', string)
            # 改变按键状态
            self.button_contrl(4)
        else:
            string = '码率波动计算失败。'
            self.global_set.print_gui(string)
            tkinter.messagebox.showerror('错误', '计算失败！请重新输入数值：')

    # 主界面 - 计算h264码率波动功能 NEW
    def calculate_new_btn_fun(self):
        # 改变按键状态
        self.button_contrl(4, 2)
        string = '开始码率波动计算 ... ...'
        self.global_set.print_gui(string)
        check_flag = True

        #
        avg_all = 0
        res_I = 0
        res_P = 0
        try:
            with open("./output/Stream Info.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                # 这里不需要readlines
                info_dict = {}
                for idx, line in enumerate(reader):
                    if idx == 10:
                        info_dict["avg"] = int(line[0].replace(' ', '').split(':')[-1])
                    if idx == 11:
                        avg_I, max_I = map(int, line[0].replace(' ', '').split(':')[-1].split('/'))
                        info_dict["avg_I"] = avg_I
                        info_dict["max_I"] = max_I
                    if idx == 12:
                        avg_P, max_P = map(int, line[0].replace(' ', '').split(':')[-1].split('/'))
                        info_dict["avg_P"] = avg_P
                        info_dict["max_P"] = max_P
                print(info_dict)

                # 平均码率
                avg_ = info_dict["avg"]
                avg_all = avg_ * 8 * 25 / 1000
                print('平均码率：{:.2f} Kbps'.format(avg_all))
                # I帧波动
                avg_I = info_dict["avg_I"]
                max_I = info_dict["max_I"]
                res_I = 100 * (max_I - avg_I) / avg_I
                print('I帧码率波动：{:.2f} %'.format(res_I))
                # I帧波动
                avg_P = info_dict["avg_P"]
                max_P = info_dict["max_P"]
                res_P = 100 * (max_P - avg_P) / avg_P
                print('P帧码率波动：{:.2f} %'.format(res_P))
        except:
            check_flag = False

        # check
        if check_flag:
            string = '码率分析计算完成，平均码率：{:.2f} Kbps\n' \
                     'I帧码率波动：{:.2f} %，P帧码率波动：{:.2f} %'.format(avg_all, res_I, res_P)
            self.global_set.print_gui(string)
            tkinter.messagebox.showinfo('提示', string)
            self.save_record_files()
            string = '已结束所有码流测试内容，请做好记录。\n如需开始新测试，请完成 <测试配置> 后进行。'
            self.global_set.print_gui(string)
            tkinter.messagebox.showinfo('提示', string)
            # 改变按键状态
            self.button_contrl(4)
        else:
            string = '码率波动计算失败。'
            self.global_set.print_gui(string)
            tkinter.messagebox.showerror('错误', '计算失败！请重新输入数值：')

    # 主界面 - 获取服务器记录文件操作
    def get_server_record(self):
        string = '开始连接服务器获取f_record.txt ...'
        self.global_set.print_gui(string)

        # get_file_path = self.config_dict["path"] % int(self.config_dict["factory"][0])
        # string = '获取文件：%s' % get_file_path
        # self.global_set.print_gui(string)

        remote_file = None
        remote_file_lines = []
        try:
            # connect server
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 服务器信息，主机名（IP地址）、端口号、用户名及密码
            hostname = self.config_dict["ip"]
            port = 22
            username = self.config_dict["user"]
            password = self.config_dict["pswd"]
            client.connect(hostname, port, username, password, compress=True)
            string = '服务器连接成功！'
            self.global_set.print_gui(string)
            # create sftp
            sftp_client = client.open_sftp()
            get_file_path = self.config_dict["path"] % int(self.config_dict["factory"][0])
            string = '获取文件：%s' % get_file_path
            self.global_set.print_gui(string)
            remote_file = sftp_client.open(get_file_path)  # 文件路径
            # print(remote_file)
            for line in remote_file:
                line = line.strip()
                remote_file_lines.append(line)
            string = '服务器f_record.txt获取成功！'
            self.global_set.print_gui(string)
        except:
            string = '获取f_record.txt失败！'
            self.global_set.print_gui(string)
            tkinter.messagebox.showerror('错误', string)
        finally:
            remote_file.close()
        return remote_file_lines

    # 主界面 - 获取服务器记录文件菜单操作
    def get_rtmp_url_menu_fun(self):
        # 非法判定
        if not self.config_dict["factory"]:
            string = '请先进行“测试参数设置”菜单操作！'
            self.global_set.print_gui(string)
            tkinter.messagebox.showerror('错误', string)
            return
        # 清空记录
        self.rtmp_url_list = []
        self.rtmp_url_combox_list["values"] = self.rtmp_url_list
        string = '开始获取服务器RTMP流媒体地址文件 ...'
        self.global_set.print_gui(string)

        if self.config_dict["is_test"] == "True":
            with open(r'./f_record.txt', 'r', encoding='UTF-8-sig') as f:
                lines = f.readlines()
                # print(lines)
        else:
            lines = self.get_server_record()
            # print(lines)
        if not lines:
            string = '获取f_record记录值为空！'
            self.global_set.print_gui(string)
            tkinter.messagebox.showerror('错误', string)
            return
        cnt = len(lines)
        for idx in range(cnt - 1):
            line1 = lines[idx]
            line2 = lines[idx + 1]
            print(idx, line1)
            print(idx, line2)
            if not line1.startswith("{") or not line2.startswith("{"):
                print("跳过")
                continue
            json_dict_1 = json.loads(line1)
            json_dict_2 = json.loads(line2)
            if "ip" in json_dict_1 and json_dict_2["code"] == 200:
                try:
                    serverIp = json_dict_1["in_data"]["command"]["serverIp"]
                    serverPort = json_dict_1["in_data"]["command"]["serverPort"]
                    pubName = json_dict_1["in_data"]["command"]["pubName"].strip('/')
                    cameraNum = json_dict_1["cameraNum"]
                    rtmp_url = "rtmp://%s:%s/%s/%s" % (serverIp, serverPort, pubName, cameraNum)
                    if rtmp_url not in self.rtmp_url_list:
                        self.rtmp_url_list.append(rtmp_url)
                        string = '获取新RTMP流媒体地址：' + rtmp_url
                        print(string)
                        self.global_set.print_gui(string)
                except:
                    print("跳过")
                    continue
        # reload
        self.rtmp_url_combox_list["values"] = self.rtmp_url_list

        string = '刷新RTMP流媒体地址列表成功！'
        self.global_set.print_gui(string)
        # 改变按键状态
        self.button_contrl(-2)

    # 主界面 - 版权功能
    def show_info_fun(self):
        string = '西南交通大学 2020 © 版权所有\nCopyright © 2020 Southwest Jiaotong University. All rights reserved.'
        self.global_set.print_gui(string)
        tkinter.messagebox.showinfo('提示', string)
        string = ''

    # 主界面 - 播放控制
    def video_click(self, action):
        if action == 0:
            if self.player.get_state() == 0:
                string = '恢复播放RTMP视频流。'
                self.global_set.print_gui(string)
                self.player.resume()
            elif self.player.get_state() == 1:
                pass  # 播放新资源
            else:
                url, _ = self.rtmp_url_check()
                if url:
                    string = '开始播放RTMP视频流：%s' % url
                    self.global_set.print_gui(string)
                    self.player.play(url)
                    self.player.add_callback(vlc.EventType.MediaPlayerBuffering, self.video_buffering_call_back)
                    self.player.add_callback(vlc.EventType.MediaPlayerPlaying, self.video_playing_call_back)
                    self.player.add_callback(vlc.EventType.MediaPlayerPaused, self.video_paused_call_back)
                    self.player.add_callback(vlc.EventType.MediaPlayerStopped, self.video_stopped_call_back)
                    self.player.add_callback(vlc.EventType.MediaPlayerTimeChanged, self.video_time_call_back)
        elif action == 1:
            if self.player.get_state() == 1:
                string = '暂停播放RTMP视频流。'
                self.global_set.print_gui(string)
                self.player.pause()
        else:
            self.player.stop()
            string = '停止播放RTMP视频流。'
            self.global_set.print_gui(string)
            '''
            self.player.remove_callback(vlc.EventType.MediaPlayerBuffering, self.video_buffering_call_back)
            self.player.remove_callback(vlc.EventType.MediaPlayerPlaying, self.video_playing_call_back)
            self.player.remove_callback(vlc.EventType.MediaPlayerPaused, self.video_paused_call_back)
            self.player.remove_callback(vlc.EventType.MediaPlayerStopped, self.video_stopped_call_back)
            self.player.remove_callback(vlc.EventType.MediaPlayerTimeChanged, self.video_time_call_back)
            '''

    # vlc state call back
    def video_time_call_back(self, event):
        print("call: time", self.player.get_time())
        self.vinfo_2 = ''
        self.vinfo_3 = '%.3f' % (self.player.get_time() / 1000)
        text = self.format % (self.vinfo_1 + self.vinfo_2, self.vinfo_3)
        self.str_obj_1.set(text)

    # vlc state call back
    def video_buffering_call_back(self, event):
        print("====> call: buffering", self.player.get_state())
        self.vinfo_2 = ' 缓冲中...'
        text = self.format % (self.vinfo_1 + self.vinfo_2, self.vinfo_3)
        self.str_obj_1.set(text)

    # vlc state call back
    def video_playing_call_back(self, event):
        print("====> call: playing")
        self.vinfo_1 = '正在播放'
        self.vinfo_2 = ''
        text = self.format % (self.vinfo_1 + self.vinfo_2, self.vinfo_3)
        self.str_obj_1.set(text)

    # vlc state call back
    def video_stopped_call_back(self, event):
        print("====> call: stopped", self.player.get_state())
        self.vinfo_1 = '已停止'
        self.vinfo_2 = ''
        text = self.format % (self.vinfo_1 + self.vinfo_2, self.vinfo_3)
        self.str_obj_1.set(text)

    # vlc state call back
    def video_paused_call_back(self, event):
        print("====> call: paused", self.player.get_state())
        self.vinfo_1 = '已暂停'
        self.vinfo_2 = ''
        text = self.format % (self.vinfo_1 + self.vinfo_2, self.vinfo_3)
        self.str_obj_1.set(text)

    # 主界面 - 连接测试
    def ping_test(self, url):
        _, ipv4 = self.rtmp_url_check()
        string = '开始测试：到 %s 的网络 ... ...' % ipv4
        self.global_set.print_gui(string)
        cmd = u"ping " + ipv4
        result = -1
        try:
            sub_p = subprocess.Popen(cmd)
            tt = 1
            while sub_p.poll() == None:
                string = '执行操作用时 %d s' % tt
                self.global_set.print_gui(string)
                tt += 1
                print(string)
                time.sleep(1)
            print('run over!')
            result = sub_p.returncode
            print(result)
        except:
            string = '连接测试失败！'
            self.global_set.print_gui(string)
            tkinter.messagebox.showerror('错误', string)
        if result == 0:
            string = '测试完成，到 %s 的网络通畅！' % ipv4
            print(string)
            self.global_set.print_gui(string)
            tkinter.messagebox.showinfo('提示', string)
        else:
            string = '测试完成，到 %s 的网络故障！' % ipv4
            print(string)
            self.global_set.print_gui(string)
            tkinter.messagebox.showerror('错误', string)
        return result

    # 主界面 - 服务器连接测试菜单操作
    def server_ping_test(self):
        ipv4 = self.config_dict["ip"]
        string = '开始测试：到 %s 的网络 ... ...' % ipv4
        self.global_set.print_gui(string)
        cmd = u"ping " + ipv4
        result = -1
        try:
            sub_p = subprocess.Popen(cmd)
            tt = 1
            while sub_p.poll() == None:
                string = '执行操作用时 %d s' % tt
                self.global_set.print_gui(string)
                tt += 1
                print(string)
                time.sleep(1)
            print('run over!')
            result = sub_p.returncode
            print(result)
        except:
            string = '连接测试失败！'
            self.global_set.print_gui(string)
            tkinter.messagebox.showerror('错误', string)
        if result == 0:
            string = '测试完成，到 %s 的网络通畅！' % ipv4
            print(string)
            self.global_set.print_gui(string)
            tkinter.messagebox.showinfo('提示', string)
        else:
            string = '测试完成，到 %s 的网络故障！' % ipv4
            print(string)
            self.global_set.print_gui(string)
            tkinter.messagebox.showerror('错误', string)
        return result

    # 主界面 - rtmp_url_combox_list控件操作
    def rtmp_url_combox_list_change(self, event=None):
        # 改变按键状态
        self.button_contrl(-1, 1)
        url = self.rtmp_url_combox_list.get()
        string = 'RTMP视频流采集地址选择为：' + url
        self.global_set.print_gui(string)
        result = self.ping_test(url)

        if result == 0:
            string = '请开始 <播放> RTMP视频流，或完成 <捕获时长> 设置后 开始 <捕获> RTMP视频流！'
            self.global_set.print_gui(string)
            # self.video_click(0)
            # 改变按键状态
            self.button_contrl(-1, 0)

    # 主界面 - sample_time_combox_list控件操作
    def sample_time_combox_list_change(self, event=None):
        # 改变按键状态
        self.button_contrl(0, 1)
        time_string = self.sample_time_combox_list.get()
        string = 'RTMP视频流捕获时长设置为：%s。' % time_string
        self.global_set.print_gui(string)
        string = '请开始 <播放> 或 <捕获> RTMP视频流！'
        self.global_set.print_gui(string)
        # 改变按键状态
        self.button_contrl(0)

    # 主界面 - 关闭窗口操作
    def on_closing(self):
        an = tkinter.messagebox.askyesno('提示', '要关闭测试程序吗？')  # 是/否，返回值true/false
        print(an)
        if an:
            # 停止视频播放
            self.video_click(2)
            self.player.release()
            self.config_window.destroy()
            self.root_window.destroy()

    # 主界面 - 打开output操作
    def open_output_dir_fun(self):
        os.system(r'start .\output')
        print('run over!')
        string = '访问RTMP流媒体捕获文件夹。'
        self.global_set.print_gui(string)

    # 主界面 - 打开VLC操作
    def open_vlc_pro_fun(self):
        os.system(r'start .\lib\vlc-3.0.8-win64\vlc.exe')
        print('run over!')
        string = '开启VLC。'
        self.global_set.print_gui(string)

    # 主界面 - 测试设置菜单操作
    def config_menu_fun(self):
        # self.reload_config_fun()
        self.config_window.update()
        self.config_window.deiconify()

    # 主界面 - button控制操作
    def button_contrl(self, step_idx, start=0):
        print("已完成操作step%d start%d" % (step_idx, start))
        if step_idx == -2:
            self.rtmp_url_combox_list['state'] = 'normal'
        elif step_idx == -1:
            if start:
                self.rtmp_url_combox_list['state'] = 'disabled'
            else:
                self.video_button_1['state'] = 'normal'
                self.video_button_2['state'] = 'normal'
                self.video_button_3['state'] = 'normal'
                self.sample_time_combox_list['state'] = 'normal'
        elif step_idx == 0:
            if start:
                self.sample_time_combox_list['state'] = 'disabled'
            else:
                self.button_1['state'] = 'normal'
        elif step_idx == 1:
            if start:
                self.button_1['state'] = 'disabled'
            else:
                self.button_2['state'] = 'normal'
        elif step_idx == 2:
            if start:
                self.button_2['state'] = 'disabled'
            else:
                self.button_3['state'] = 'normal'
        elif step_idx == 3:
            if start:
                self.button_3['state'] = 'disabled'
            else:
                self.button_4['state'] = 'normal'
                self.button_5['state'] = 'normal'
                self.min_entry['state'] = 'normal'
                self.max_entry['state'] = 'normal'
                self.avg_entry['state'] = 'normal'
                self.result_entry['state'] = 'normal'
        elif step_idx == 4:
            if start == 1:
                self.button_4['state'] = 'disabled'
            elif start == 2:
                self.button_5['state'] = 'disabled'
            else:
                self.rtmp_url_combox_list['state'] = 'disabled'
                self.sample_time_combox_list['state'] = 'disabled'
                self.button_1['state'] = 'disabled'
                self.button_2['state'] = 'disabled'
                self.button_3['state'] = 'disabled'
                self.button_4['state'] = 'disabled'
                self.button_5['state'] = 'disabled'
                self.min_entry['state'] = 'disabled'
                self.max_entry['state'] = 'disabled'
                self.avg_entry['state'] = 'disabled'
                self.result_entry['state'] = 'disabled'
                self.video_button_1['state'] = 'disabled'
                self.video_button_2['state'] = 'disabled'
                self.video_button_3['state'] = 'disabled'
                # 停止视频播放
                # self.video_click(2)
        else:
            self.rtmp_url_combox_list['state'] = 'disabled'
            self.sample_time_combox_list['state'] = 'disabled'
            self.button_1['state'] = 'disabled'
            self.button_2['state'] = 'disabled'
            self.button_3['state'] = 'disabled'
            self.button_4['state'] = 'disabled'
            self.button_5['state'] = 'disabled'
            self.min_entry['state'] = 'disabled'
            self.max_entry['state'] = 'disabled'
            self.avg_entry['state'] = 'disabled'
            self.result_entry['state'] = 'disabled'
            self.video_button_1['state'] = 'disabled'
            self.video_button_2['state'] = 'disabled'
            self.video_button_3['state'] = 'disabled'

        # print("当前窗口的高度为", self.root_window.winfo_height())

    # 子界面 - 关闭窗口操作
    def subwin_on_closing(self):
        self.config_window.withdraw()

    # 配置界面 - 返回配置操作
    def reload_config_fun(self):
        # 设定输入框
        self.config_entry_1.delete(0, tkinter.END)
        self.config_entry_1.insert(0, self.config_dict["ip"])
        self.config_entry_2.delete(0, tkinter.END)
        self.config_entry_2.insert(0, self.config_dict["user"])
        self.config_entry_3.delete(0, tkinter.END)
        self.config_entry_3.insert(0, self.config_dict["pswd"])
        self.config_entry_4.delete(0, tkinter.END)
        self.config_entry_4.insert(0, self.config_dict["path"])

    # 配置界面 - 设置配置操作
    def set_config_btn_fun(self):
        self.config_dict["ip"] = self.config_entry_1.get()
        self.config_dict["user"] = self.config_entry_2.get()
        self.config_dict["pswd"] = self.config_entry_3.get()
        self.config_dict["path"] = self.config_entry_4.get()
        self.config_dict["factory"] = self.factory_combox_list.get()
        self.config_dict["model"] = self.config_entry_5.get()
        self.config_dict["parameter"] = self.parameter_combox_list.get()
        self.config_dict["count"] = self.count_combox_list.get()
        self.config_dict["is_test"] = self.config_entry_6.get()
        self.config_window.withdraw()
        string = '参数设置成功！网关厂商：%s，设备型号：%s，' \
                 '码流配置：%s，测试次数：%s。' % (
                     self.config_dict["factory"].split()[-1], self.config_dict["model"].split()[-1],
                     self.config_dict["parameter"].split()[-1], self.config_dict["count"].split()[-1])
        self.global_set.print_gui(string)
        # 创建存档文件夹
        if not self.mk_dir(self.save_dir_root):
            string = "创建文件夹%s失败，重试操作！" % self.save_dir_root
            self.global_set.print_gui(string)
            tkinter.messagebox.showerror('错误', string)
        if not self.mk_dir(self.get_record_dir()):
            string = "创建文件夹%s失败，重试操作！" % self.get_record_dir()
            self.global_set.print_gui(string)
            tkinter.messagebox.showerror('错误', string)

    # 配置界面 - 返回配置操作
    def back_config_btn_fun(self):
        self.config_window.withdraw()


def main():
    # 初始化对象
    app = AppGUI()
    # 进行布局
    # app.config_gui_arrange()
    app.root_gui_arrange()
    # 程序自检
    app.global_set.sys_log_check()
    # 加载外部设置
    app.global_set.load_outer_configs()
    # 进行布局
    app.config_gui_arrange()
    # 更新配置
    # app.update_gui_arrange()
    # 主程序执行
    tkinter.mainloop()


if __name__ == "__main__":
    main()
