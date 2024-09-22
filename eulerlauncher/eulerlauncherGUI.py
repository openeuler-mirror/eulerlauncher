"""
Author: XiangChenyu
Description: EulerLauncher前端界面
Tips:
- take-snapshot与export-development-image功能由于主程序尚未实现，该前端界面在这两部分留空，实现后请补齐
    具体需要修改的位置为button_vmsnapshot_clicked和button_vmout_clicked两个函数
    Line 620  未实现的提示，主程序实现该功能后请删除此行代码
    Line 637  实现后请在实际情况下修改该判断条件，就是按照正确执行后命令行的返回值特点来进行判断
    Line 672  未实现的提示，主程序实现该功能后请删除此行代码
    Line 690  实现后请在实际情况下修改该判断条件，就是按照正确执行后命令行的返回值特点来进行判断
- 由于主程序暂未对Linux提供支持，因此Linux系统下的终端SSH连接功能还未进行验证，修改请在Line 739处进行
- 增删改功能请在主界面init_ui或四个界面生成函数(以widget_of开头)中增删改按钮等控件，然后增删改对应的槽函数即可。
- 本代码中有许多通用方法，如do_cmd、table_process、create_massage_box、create_line等，可以复用
    它们在Line 374、415、955、964
- 请注意，本代码仅为前端界面，后端功能由EulerLauncherd提供，因此请确保整个EulerLauncher已经正确安装并配置好conf文件
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QFrame, \
                            QPushButton, QLabel, QListWidget, QFileDialog, QInputDialog, QMessageBox, QTextEdit, \
                            QLineEdit, QCheckBox, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from paramiko import SSHClient, AutoAddPolicy
import subprocess
import time
import re


class EulerLauncherGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建一个堆叠布局
        self.stack = QStackedWidget()

        # 创建边栏
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar_layout = QVBoxLayout(self.sidebar)

        # 创建内容区域
        self.content = QFrame()
        self.content.setObjectName("content")
        self.content_layout = QVBoxLayout(self.content)

        # 设置刷新提示与刷新时间记录文本
        self.refresh_time = QLabel('请点击刷新按钮获取镜像列表')
        self.refresh_vm_time = QLabel('请点击刷新按钮获取虚拟机列表')

        # 边栏选中的按钮
        self.current_button = None

        # 虚拟机连接界面的信息
        self.vm_tip = QLabel('请点击虚拟机管理界面选择虚拟机进行连接', self)
        self.vm_tip.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.vm_name = QLabel('', self)
        self.vm_name.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.vm_image = QLabel('', self)
        self.vm_image.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.vm_state = QLabel('', self)
        self.vm_state.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.vm_ip = QLabel('', self)
        self.vm_ip.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # ssh连接
        self.ssh = None
        self.shell = None

        # 创建主窗口
        self.init_ui()

    def init_ui(self):
        # 创建主窗口
        main_widget = QWidget()

        # 创建布局
        main_layout = QHBoxLayout(self)

        # 将堆叠布局添加到内容区域
        self.content_layout.addWidget(self.stack)

        # 将各个页面添加到堆叠布局
        self.stack.addWidget(self.widget_of_iso())
        self.stack.addWidget(self.widget_of_management())
        self.stack.addWidget(self.widget_of_connecting())
        self.stack.addWidget(self.widget_of_setting())

        # 切换显示用的按钮, 它们的name属性为menu
        self.button1 = QPushButton('镜像管理', self)
        self.button1.setProperty('name', 'menu')
        self.button1.clicked.connect(self.switch_page)
        self.sidebar_layout.addWidget(self.button1)

        self.button2 = QPushButton('虚拟机管理', self)
        self.button2.setProperty('name', 'menu')
        self.button2.clicked.connect(self.switch_page)
        self.sidebar_layout.addWidget(self.button2)

        self.button3 = QPushButton('虚拟机连接', self)
        self.button3.setProperty('name', 'menu')
        self.button3.clicked.connect(self.switch_page)
        self.sidebar_layout.addWidget(self.button3)

        self.button4 = QPushButton('设置', self)
        self.button4.setProperty('name', 'menu')
        self.button4.clicked.connect(self.switch_page)

        # 设置按钮的位置
        self.sidebar_layout.addStretch(1)
        self.sidebar_layout.addWidget(self.create_line(True))
        self.sidebar_layout.addWidget(self.button4)

        # 设置按钮的可选择状态
        self.button1.setCheckable(True)
        self.button2.setCheckable(True)
        self.button3.setCheckable(True)
        self.button4.setCheckable(True)

        # 设置按钮的默认状态
        self.current_button = self.button1
        self.button1.setChecked(True)

        # 将按钮布局和堆叠布局添加到主布局中
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)

        # 设置主窗口的布局
        main_widget.setLayout(main_layout)

        # 设置主窗口的中央部件
        self.setCentralWidget(main_widget)

        # 设置窗口的标题
        self.setWindowTitle('EulerLauncherGUI')

        # 设置窗口的图标
        self.setWindowIcon(QIcon('etc/favicon.ico'))

        # 加载样式表
        self.load_qss_style()

        # 设置窗口的大小
        self.resize(800, 450)

    def widget_of_iso(self):  # 创建镜像管理页面
        wid = QWidget()

        # 定义布局
        main_layout = QVBoxLayout(wid)
        button_layout = QHBoxLayout(wid)

        # 镜像列表的标题
        label1 = QLabel(f'镜像名称 | 位置 | 状态', wid)
        label1.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(label1)

        # 镜像列表 使用QListWidget
        self.list_of_iso = QListWidget(wid)

        # 四个按钮
        button_fresh = QPushButton('刷新', wid)
        button_load = QPushButton('加载本地镜像', wid)
        button_del = QPushButton('删除镜像', wid)
        button_download = QPushButton('下载镜像', wid)

        # 各个button的位置布局 放入HBox button_layout 中
        button_layout.addStretch(1)
        button_layout.addWidget(button_fresh)
        button_layout.addStretch(1)
        button_layout.addWidget(button_load)
        button_layout.addStretch(1)
        button_layout.addWidget(button_del)
        button_layout.addStretch(1)
        button_layout.addWidget(button_download)
        button_layout.addStretch(1)

        # 设置按钮的信号与槽
        button_fresh.clicked.connect(self.button_fresh_clicked)
        button_load.clicked.connect(self.button_load_clicked)
        button_del.clicked.connect(self.button_del_clicked)
        button_download.clicked.connect(self.button_download_clicked)

        # 将文本、镜像列表和按钮布局放入VBox main_layout 中
        main_layout.addWidget(self.list_of_iso)
        main_layout.addWidget(self.refresh_time)
        main_layout.addLayout(button_layout)

        # 设置窗口的布局
        wid.setLayout(main_layout)

        return wid

    def widget_of_management(self):  # 创建虚拟机管理页面
        wid = QWidget()

        # 定义布局
        main_layout = QVBoxLayout(wid)
        button_layout = QHBoxLayout(wid)
        head_layout = QHBoxLayout(wid)

        # 虚拟机列表的标题
        label1 = QLabel(f'虚拟机名称 | 使用的镜像 | 状态 | IP', wid)
        label1.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        head_layout.addWidget(label1)

        # 镜像列表 使用QListWidget
        self.list_of_vm = QListWidget(wid)

        # 六个按钮
        button_vmfresh = QPushButton('刷新', wid)
        button_vmcreate = QPushButton('创建虚拟机', wid)
        button_vmsnapshot = QPushButton('生成快照', wid)
        button_vmdel = QPushButton('删除虚拟机', wid)
        button_vmout = QPushButton('导出为开发镜像', wid)
        button_vmlink = QPushButton('连接', wid)

        # 刷新按钮与Label一行
        head_layout.addWidget(button_vmfresh)
        main_layout.addLayout(head_layout)

        # 其他各个button的位置布局 放入HBox button_layout 中
        button_layout.addStretch(1)
        button_layout.addWidget(button_vmcreate)
        button_layout.addStretch(1)
        button_layout.addWidget(button_vmdel)
        button_layout.addStretch(1)
        button_layout.addWidget(button_vmsnapshot)
        button_layout.addStretch(1)
        button_layout.addWidget(button_vmout)
        button_layout.addStretch(1)
        button_layout.addWidget(button_vmlink)
        button_layout.addStretch(1)

        # 设置按钮的信号与槽
        button_vmfresh.clicked.connect(self.button_vmfresh_clicked)
        button_vmcreate.clicked.connect(self.button_vmcreate_clicked)
        button_vmsnapshot.clicked.connect(self.button_vmsnapshot_clicked)
        button_vmdel.clicked.connect(self.button_vmdel_clicked)
        button_vmout.clicked.connect(self.button_vmout_clicked)
        button_vmlink.clicked.connect(self.button_vmlink_clicked)

        # 将文本、镜像列表和按钮布局放入VBox main_layout 中
        main_layout.addWidget(self.list_of_vm)
        main_layout.addWidget(self.refresh_vm_time)
        main_layout.addLayout(button_layout)

        # 设置窗口的布局
        wid.setLayout(main_layout)

        return wid

    def widget_of_connecting(self):  # 创建虚拟机连接页面
        wid = QWidget()

        # 定义按钮
        btn = QPushButton('调用终端进行SSH连接', wid)
        btn.clicked.connect(self.button_connection_clicked)
        btn2 = QPushButton('在GUI中进行SSH连接', wid)
        btn2.clicked.connect(self.connect_ssh)
        btn3 = QPushButton('断开连接', wid)
        btn3.clicked.connect(self.close_ssh)
        self.ck = QCheckBox('保留上一句命令', wid)

        # 定义内容输出框
        self.output_text = QTextEdit(wid)
        self.output_text.setReadOnly(True)

        # 定义输入框与发送按钮
        self.command_input = QLineEdit(wid)
        self.command_input.returnPressed.connect(self.execute_command)
        self.command_input.setPlaceholderText("Command  Press Enter to send")
        send_button = QPushButton('Send', wid)
        send_button.clicked.connect(self.execute_command)

        # 定义布局
        main_layout = QVBoxLayout(wid)
        upper_layout = QHBoxLayout(wid)
        bottom_layout = QHBoxLayout(wid)

        button_layout = QVBoxLayout(wid)
        button_layout.addWidget(btn)
        button_layout.addWidget(btn2)
        button_layout.addWidget(btn3)

        layout = QVBoxLayout(wid)
        layout.addWidget(self.vm_tip)
        layout.addWidget(self.vm_name)
        layout.addWidget(self.vm_image)
        layout.addWidget(self.vm_state)
        layout.addWidget(self.vm_ip)

        upper = QWidget()
        upper_layout.addLayout(layout)
        upper_layout.addLayout(button_layout)
        upper.setLayout(upper_layout)
        upper.setMaximumHeight(200)

        bottom_layout.addWidget(self.command_input)
        bottom_layout.addWidget(send_button)

        main_layout.addWidget(upper)
        main_layout.addWidget(self.output_text)
        main_layout.addLayout(bottom_layout)
        main_layout.addWidget(self.ck)

        wid.setLayout(main_layout)

        return wid

    def widget_of_setting(self):  # 创建设置页面
        wid = QWidget()
        main_layout = QVBoxLayout(wid)

        # conf文件选择区域
        conf_layout = QHBoxLayout(wid)

        conf_button = QPushButton('选择conf文件', wid)
        conf_button.clicked.connect(self.fetch_conf_path)

        self.conf_label = QLabel('conf文件未选中', wid)

        conf_layout.addWidget(self.conf_label)
        conf_layout.addWidget(conf_button)

        # conf文件显示内容修改区域
        bottom_layout = QHBoxLayout(wid)
        btn_layout = QVBoxLayout(wid)

        self.conf_text = QTextEdit(wid)
        self.conf_text.setReadOnly(True)

        edit_button = QPushButton('修改', wid)
        edit_button.clicked.connect(self.write_conf)
        re_button = QPushButton('恢复默认', wid)
        re_button.clicked.connect(self.initialize_conf)

        btn_layout.addStretch(1)
        btn_layout.addWidget(edit_button)
        btn_layout.addWidget(re_button)
        btn_layout.addStretch(1)

        bottom_layout.addWidget(self.conf_text)
        bottom_layout.addLayout(btn_layout)

        # 设置布局
        main_layout.addLayout(conf_layout)
        main_layout.addWidget(self.create_line())
        main_layout.addLayout(bottom_layout)

        wid.setLayout(main_layout)

        return wid

    def switch_page(self):  # 切换页面
        button = self.sender()
        if self.current_button:  # 取消之前选中的按钮
            self.current_button.setChecked(False)
        button.setChecked(True)  # 设置当前选中的按钮
        self.current_button = button
        index = 0
        if button.text() == '镜像管理':
            index = 0
        elif button.text() == '虚拟机管理':
            index = 1
        elif button.text() == '虚拟机连接':
            index = 2
        elif button.text() == '设置':
            index = 3
        self.stack.setCurrentIndex(index)  # 切换页面
        if self.ssh:
            self.close_ssh()  # 关闭ssh连接, 防止在连接界面切换到其他界面时出现问题

    def do_cmd(self, cmd):
        # 执行命令行语句, 并将输出以列表形式返回, check为True表示正常执行, False表示出现错误
        outputs = []
        check = True
        try:  # 捕获异常
            if sys.platform == 'win32':
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                     creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            while True:
                output = p.stdout.readline()
                if output == '' and p.poll() is not None:
                    break
                elif output:
                    outputs.append(output.strip())

            # 等待进程结束
            p.wait()

            # 错误输出
            stderr = p.stderr.read()
            if stderr:
                self.create_message_box('错误', stderr)
                check = False

        # 异常处理
        except FileNotFoundError:
            self.create_message_box('错误', '命令行未知命令: eulerlauncher\n请检查是否安装了EulerLauncher\n'
                                    '\n需要以管理员身份运行'
                                    '\nWindows：是否将EulerLauncher添加到环境变量PATH中'
                                    '\nLinux & MacOS：EulerLauncher是否按说明将conf文件配置正确')
            check = False
        except Exception as e:
            self.create_message_box('错误', str(e))
            check = False
        finally:
            return outputs, check

    @staticmethod
    def table_process(column_num, table_list, target_q_list_widget):  # 该函数处理返回的表格
        for item in table_list:
            if item[0] == '+':  # 去除表格线
                continue
            else:
                pattern1 = r'.+Images.+Location.+Status.*'
                pattern2 = r'.+Name.+Image.+State.+IP.*'
                if re.match(pattern1, item) or re.match(pattern2, item):  # 去除表头
                    continue
                else:  # 处理表格内容
                    item = item.split()
                    flag = 0
                    item_process = ''
                    for i in item:
                        if not i == '|':
                            flag += 1
                            item_process += i
                            if flag < column_num:
                                item_process += ' | '
                    target_q_list_widget.addItem(item_process)

    def button_fresh_clicked(self):  # 镜像刷新按钮的槽函数
        self.list_of_iso.clear()

        # 构建命令行语句
        cmd = ['eulerlauncher',  'images']

        # 执行命令行语句, 并将输出添加到列表中
        iso_list, check = self.do_cmd(cmd)
        if check:
            if not iso_list[0][0] == '+':  # 返回的不是一个表格, 说明出现了错误
                if iso_list[0] == 'Calling to EulerLauncherd daemon failed, please check ' \
                            'EulerLauncherd daemon status ...':
                    self.create_message_box('错误', '{}\n请检查是否运行了EulerLauncherd后台程序'.format(iso_list[0]))
                else:
                    self.create_message_box('错误', iso_list[0])
            else:
                # 处理表格
                self.table_process(3, iso_list, self.list_of_iso)
            self.list_of_iso.update()

            # 刷新时间
            self.refresh_time.setText('刷新时间: ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    def button_load_clicked(self):  # 加载本地镜像按钮的槽函数
        # 打开文件选择对话框
        filepath, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "镜像文件 (*.qcow2 *.raw *.vmdk *.vhd *.vhdx "
                                                  "*.qcow *.vdi *.qcow2.xz *.raw.xz *.vmdk.xz *.vhd.xz *.vhdx.xz "
                                                  "*.qcow.xz *.vdi.xz)")
        if filepath:
            # 选中镜像后给镜像命名
            image_name, ok = QInputDialog.getText(self, '镜像命名', '请输入镜像名称:')
            if ok:
                # 构建命令行语句
                cmd = ['eulerlauncher', 'load-image', '--path', filepath, image_name]

                # 执行命令行语句, 并将输出添加到列表中
                outputs, check = self.do_cmd(cmd)
                if check:
                    self.refresh_time.setText(
                        'Loading: {}, 可能需要一段时间, 请通过刷新按键查看加载状态'.format(image_name))
                    self.create_message_box('信息', 'Loading: {}, 可能需要一段时间\n'
                                            '请通过刷新按键查看加载状态, Ready时加载完毕'.format(image_name))
                    self.button_fresh_clicked()

    def button_del_clicked(self):  # 删除镜像按钮的槽函数
        item = self.list_of_iso.currentItem()
        if item:
            # 获取选中的镜像名称已经其状态
            iso_info = item.text().split(' | ')
            iso_name = iso_info[0]

            # 构建命令行语句
            cmd = ['eulerlauncher', 'delete-image', iso_name]

            # 执行命令行语句, 并将输出添加到列表中
            outputs, check = self.do_cmd(cmd)
            pattern = r'.+has been successfully deleted'
            if check and re.match(pattern, outputs[0]):
                self.refresh_time.setText('镜像{}被成功删除'.format(iso_name))
                self.create_message_box('信息', '镜像{}被成功删除'.format(iso_name))
                self.button_fresh_clicked()
            elif check:
                self.create_message_box('错误', outputs[0])
            else:
                self.create_message_box('错误', '删除失败')

        else:
            self.create_message_box('错误', '未选中镜像')

    def button_download_clicked(self):  # 下载镜像按钮的槽函数
        item = self.list_of_iso.currentItem()
        if item:
            # 获取选中的镜像名称已经其状态
            iso_info = item.text().split(' | ')
            iso_name = iso_info[0]
            iso_status = iso_info[2]

            if iso_status == 'Downloadable':
                # 构建命令行语句
                cmd = ['eulerlauncher', 'download-image', iso_name]

                # 执行命令行语句, 并将输出添加到列表中
                outputs, check = self.do_cmd(cmd)
                if check:
                    self.refresh_time.setText(
                        'Downloading: {}, 可能需要一段时间, 请通过刷新按键查看下载状态'.format(iso_name))
                    self.create_message_box('信息', 'Downloading: {}, 可能需要一段时间\n'
                                            '请通过刷新按键查看下载状态, Ready时为下载完毕'.format(iso_name))
                    self.button_fresh_clicked()
        else:
            self.create_message_box('错误', '未选中镜像')

    def button_vmfresh_clicked(self):  # 虚拟机刷新按钮的槽函数
        self.list_of_vm.clear()

        # 构建命令行语句
        cmd = ['eulerlauncher', 'list']

        # 执行命令行语句, 并将输出添加到列表中
        vm_list, check = self.do_cmd(cmd)
        if check:
            if not vm_list[0][0] == '+':
                if vm_list[0] == 'Calling to EulerLauncherd daemon failed, please check ' \
                            'EulerLauncherd daemon status ...':
                    self.create_message_box('错误', '{}\n请检查是否运行了EulerLauncherd后台程序\n'.format(vm_list[0]))
                else:
                    self.create_message_box('错误', vm_list[0])
            else:
                # 处理表格
                self.table_process(4, vm_list, self.list_of_vm)
            self.list_of_vm.update()

            # 如果要连接的虚拟机不存在了, 则将连接界面的信息清空
            if self.vm_ip.text() != '':
                vm_ip = self.vm_ip.text()
                for i in range(self.list_of_vm.count()):
                    now = self.list_of_vm.item(i).text()
                    ip = now.split(' | ')[3]
                    if ip == vm_ip:
                        break
                else:
                    self.vm_tip.setText('请点击虚拟机管理界面选择虚拟机进行连接')
                    self.vm_name.setText('')
                    self.vm_image.setText('')
                    self.vm_state.setText('')
                    self.vm_ip.setText('')

            # 刷新时间
            self.refresh_vm_time.setText('刷新时间: ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    def button_vmcreate_clicked(self):  # 创建虚拟机按钮的槽函数
        self.button_fresh_clicked()

        # 获取可用镜像列表
        list_of_iso_copy = []
        for i in range(self.list_of_iso.count()):
            now = self.list_of_iso.item(i).text()
            name = now.split(' | ')[0]
            status = now.split(' | ')[2]
            if status == 'Ready':
                list_of_iso_copy.append(name)

        # 如果没有可用镜像, 则'无可用镜像'
        if len(list_of_iso_copy) == 0:
            list_of_iso_copy.append('无可用镜像')

        # 弹出对话框, 选择镜像
        text, ok = QInputDialog.getItem(self, '选择一个镜像', '镜像:', list_of_iso_copy, 0, False)
        if ok and text:
            if text == '无可用镜像':
                self.create_message_box('错误', '无可用镜像\n请先加载镜像或下载镜像')
            else:
                # 弹出对话框, 输入虚拟机名称
                vm_name, ok = QInputDialog.getText(self, '虚拟机命名', '请输入虚拟机名称:')

                if ok:
                    # 等待提示
                    dialog = QDialog(self)
                    dialog.setWindowTitle('请等待...')
                    dialog.setWindowModality(Qt.WindowModal)
                    dialog.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
                    dialog_layout = QVBoxLayout(dialog)
                    dialog.setLayout(dialog_layout)
                    dialog_label = QLabel('创建虚拟机{}中, 需要一段时间响应, 请稍后'.format(vm_name))
                    dialog_layout.addWidget(dialog_label)
                    dialog.show()

                    # 构建命令行语句
                    cmd = ['eulerlauncher', 'launch', '--image', text, vm_name]

                    # 执行命令行语句, 并将输出添加到列表中
                    outputs, check = self.do_cmd(cmd)
                    if check:
                        if outputs[0][0] == '+':  # 返回的是一个表格, 说明创建成功
                            self.create_message_box('信息', '创建虚拟机{}成功\n'
                                                    '需要一定时间进行网络配置，请等待\n'.format(vm_name))
                        else:
                            self.create_message_box('错误', outputs[0])
                    else:
                        self.create_message_box('错误', '创建失败')
                    dialog.close()
                    self.button_vmfresh_clicked()

    def button_vmsnapshot_clicked(self):  # 生成快照按钮的槽函数
        self.create_message_box('提示', '该功能在主程序尚未实现，请自行取消后续操作')  # 该功能在主程序尚未实现，实现后请删除此行代码

        item = self.list_of_vm.currentItem()
        if item:
            snapshot_name, ok = QInputDialog.getText(self, '快照命名', '请输入快照名称:')
            if ok:
                folder_path = QFileDialog.getExistingDirectory(None, '选择保存路径', './', QFileDialog.ShowDirsOnly)
                if folder_path:
                    # 获取选中的虚拟机名称
                    vm_name = item.text().split(' | ')[0]

                    # 构建命令行语句
                    cmd = ['eulerlauncher', 'take-snapshot', snapshot_name, 'snap', folder_path, 'path', vm_name]

                    # 执行命令行语句, 并将输出添加到列表中
                    outputs, check = self.do_cmd(cmd)
                    if check:
                        if re.match(r'Unknown', outputs[0]):  # 注：此处无对应的正确输出，因为指令不存在，请在实际情况下修改该判断条件
                            self.create_message_box('信息', '创建快照{}成功'.format(snapshot_name))
                        else:
                            self.create_message_box('错误', outputs[0])
                    else:
                        self.create_message_box('错误', '快照生成失败')
                    self.button_vmfresh_clicked()
        else:
            self.create_message_box('错误', '未选中虚拟机')

    def button_vmdel_clicked(self):  # 删除虚拟机按钮的槽函数
        item = self.list_of_vm.currentItem()
        if item:
            # 获取选中的虚拟机名称
            vm_name = item.text().split(' | ')[0]

            # 构建命令行语句
            cmd = ['eulerlauncher', 'delete-instance', vm_name]

            # 执行命令行语句, 并将输出添加到列表中
            outputs, check = self.do_cmd(cmd)
            if check:
                if re.match(r'Successfully deleted instance.+', outputs[0]):
                    self.create_message_box('信息', '删除虚拟机{}成功'.format(vm_name))
                    self.button_vmfresh_clicked()
                else:
                    self.create_message_box('错误', outputs[0])
            else:
                self.create_message_box('错误', '删除失败')
            self.button_vmfresh_clicked()

        else:
            self.create_message_box('错误', '未选中虚拟机')

    def button_vmout_clicked(self):  # 导出为开发镜像按钮的槽函数
        self.create_message_box('提示', '该功能在主程序尚未实现，请自行取消后续操作')  # 该功能在主程序尚未实现，实现后请删除此行代码

        item = self.list_of_vm.currentItem()
        if item:
            image_name, ok = QInputDialog.getText(self, '导出镜像命名', '请输入导出镜像名称:')
            if ok:
                folder_path = QFileDialog.getExistingDirectory(None, '选择保存路径', './', QFileDialog.ShowDirsOnly)
                if folder_path:
                    # 获取选中的虚拟机名称
                    vm_name = item.text().split(' | ')[0]

                    # 构建命令行语句
                    cmd = ['eulerlauncher', 'export-development-image', image_name, 'image', folder_path, 'path',
                           vm_name]

                    # 执行命令行语句, 并将输出添加到列表中
                    outputs, check = self.do_cmd(cmd)
                    if check:
                        if re.match(r'Unknown', outputs[0]):  # 注：此处无对应的正确输出，因为指令不存在，请在实际情况下修改修改该判断条件
                            self.create_message_box('信息', '导出为开发镜像{}成功'.format(image_name))
                        else:
                            self.create_message_box('错误', outputs[0])
                    else:
                        self.create_message_box('错误', '导出失败')
                    self.button_vmfresh_clicked()
        else:
            self.create_message_box('错误', '未选中虚拟机')

    def button_vmlink_clicked(self):  # 连接按钮的槽函数
        # 获取选中的虚拟机信息
        vm = self.list_of_vm.currentItem()
        if vm:
            vm_info = vm.text().split(' | ')
            # 如果虚拟机IP正在配置中, 则无法连接
            if vm_info[3] == 'N/A':
                self.create_message_box('错误', '虚拟机IP正在配置中，请稍后')
            else:
                # 更新虚拟机连接界面的信息
                self.vm_tip.setText('更换需要连接的虚拟机\n请在虚拟机管理中重新选择\n\n'
                                    '将要连接的虚拟机信息: ')
                self.vm_name.setText('虚拟机名称: ' + vm_info[0])
                self.vm_image.setText('使用的镜像: ' + vm_info[1])
                self.vm_state.setText('状态: ' + vm_info[2])
                self.vm_ip.setText(vm_info[3])

                # 自动切到虚拟机连接界面
                self.button3.click()
        else:
            self.create_message_box('错误', '未选中虚拟机')

    def button_connection_clicked(self):  # 虚拟机连接界面按钮的槽函数
        now_ip = self.vm_ip.text()
        if now_ip == '':  # 未选中虚拟机
            self.create_message_box('错误', '请点击虚拟机管理界面选择虚拟机进行连接')
        else:  # 打开终端, 并连接虚拟机
            self.open_terminal(self, 'ssh root@{}'.format(now_ip))

    @staticmethod
    def open_terminal(self, command):  # 打开终端并执行命令，用于执行终端ssh连接的第一种方式
        if sys.platform == "win32":
            # Windows系统
            subprocess.run(f'start cmd /k {command}', shell=True)
        elif sys.platform == "darwin":
            # macOS系统
            subprocess.run(['open', '-a', 'Terminal', '--args', 'bash', '-c', f'{command}; exec bash'])
        elif sys.platform == "linux" or sys.platform == "linux2":
            # Linux系统
            terminals = ['terminal', 'gnome-terminal', 'xterm', 'konsole', 'terminator', 'tilix']
            for terminal in terminals:
                try:
                    subprocess.run([terminal, '--', 'bash', '-c', f'{command}; exec bash'])
                    break
                except FileNotFoundError:
                    continue
            else:
                self.create_message_box('错误', '未找到合适的终端')

    def connect_ssh(self):  # GUI连接SSH
        host = self.vm_ip.text()
        user = 'root'
        password = 'openEuler12#$'

        if host == '':  # 未选中虚拟机
            self.create_message_box('错误', '请点击虚拟机管理界面选择虚拟机进行连接')
            return

        # 检查是否为官方镜像，如果是则使用默认密码
        self.button_fresh_clicked()
        for i in range(self.list_of_iso.count()):
            now = self.list_of_iso.item(i).text()
            name = now.split(' | ')[0]
            location = now.split(' | ')[1]
            tar = self.vm_image.text().split(': ')[1]
            if name == tar and location == 'Remote':
                break
        else:
            self.create_message_box('信息', '检测到该虚拟机为非官方镜像\n请手动输入密码连接')
            password, ok = QInputDialog.getText(self, '输入密码', '请输入密码:')
            if not ok:
                return

        # 清空输出框
        self.output_text.clear()

        try:
            # 创建SSH连接
            self.ssh = SSHClient()
            self.ssh.set_missing_host_key_policy(AutoAddPolicy())
            self.ssh.connect(host, username=user, password=password)

            # 创建伪shell
            self.shell = self.ssh.invoke_shell()

            # 读取输出
            if self.shell and self.shell.recv_ready():
                self.output_text.append(f"Connected to {host}\n")
            self.read_output()

        except Exception as e:
            self.output_text.append(f"Error: {str(e)}\n")

    def read_output(self):  # 输出读取函数
        if self.shell:
            try:
                while True:
                    if self.shell.recv_ready():
                        # 去除输出中ANSI转义字符
                        data = re.sub(r'\x1b\[\??([0-9a-z]+)(;[0-9]+)*([A-Za-z])?', '',
                                      self.shell.recv(1024).decode('utf-8'))
                        # 输出到文本框
                        self.output_text.append(data)
                        if '$' in data or '# ' in data:  # 检查命令提示符，结束读取
                            break
            except Exception as e:
                self.output_text.append(f"Error reading output: {str(e)}\n")

    def execute_command(self):  # 执行命令，即发送命令
        if self.shell:
            command = self.command_input.text()
            if command == 'exit':
                self.close_ssh()
                return
            self.shell.send(command + '\n')
            self.read_output()
            if not self.ck.isChecked():
                self.command_input.clear()
        else:
            self.output_text.clear()
            self.output_text.append("Not connected\n")

    def close_ssh(self):
        if self.ssh:
            self.ssh.close()
            self.ssh = None
        if self.shell:
            self.shell.close()
            self.shell = None
        self.output_text.clear()
        self.command_input.clear()
        self.output_text.append("Disconnected\n")

    def read_conf(self):
        try:
            with open(self.conf_label.text(), 'r') as f:
                self.conf_text.setText(f.read())
        except Exception as e:
            self.create_message_box('错误', '读取conf文件失败,{}'.format(e))
            self.conf_text.setText(str(e))

    def write_conf(self):
        if self.conf_label.text() == 'conf文件未选中':
            self.create_message_box('错误', '请先选择conf文件')
            return

        # 确认弹窗
        reply = QMessageBox.question(self, '确认', '确认修改conf文件？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        # 修改收集弹窗
        dialog = QDialog(self)
        dialog.setWindowTitle('修改conf文件')
        dialog.resize(400, 200)

        # 创建布局
        layout = QVBoxLayout(dialog)
        self.write_text = QTextEdit(dialog)
        self.write_text.setText(self.conf_text.toPlainText())
        layout.addWidget(self.write_text)
        button = QPushButton('确认', dialog)
        button.clicked.connect(self.write_conf_to_file)
        layout.addWidget(button)

        # 设置布局
        dialog.setLayout(layout)

        # 显示弹窗
        dialog.exec()

        # 完成后再次读取conf文件
        self.read_conf()

    def write_conf_to_file(self):
        try:
            with open(self.conf_label.text(), 'w') as f:
                f.write(self.write_text.toPlainText())
            self.create_message_box('信息', '修改成功')
        except Exception as e:
            self.create_message_box('错误', '写入conf文件失败,{}'.format(e))
        finally:
            dialog = self.sender().parent()
            dialog.close()

    def initialize_conf(self):
        if self.conf_label.text() == 'conf文件未选中':
            self.create_message_box('错误', '请先选择conf文件')
            return

        # 确认弹窗
        reply = QMessageBox.question(self, '确认', '确认将conf文件恢复为初始状态？', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.No:
            return

        # 按系统选择恢复内容
        if sys.platform == "win32":
            # Windows系统
            index = r'''[default]
log_dir = C:\workdir\logs
debug = True
work_dir = C:\workdir
image_dir = images
instance_dir = instances
qemu_dir = 
pattern = hyper-v

[vm]
cpu_num = 2
memory = 8G'''
        else:
            # Linux & MacOS系统
            index = '''[default]
log_dir = 
work_dir = 
wget_dir = 
qemu_dir = 
qemu_img_dir = 
debug = True

[vm]
cpu_num = 1
memory = 1024'''

        # 确认弹窗
        reply = QMessageBox.question(self, '确认', '确认将conf文件恢复为以下内容？\n{}\n注意：该内容不完整，'
                                     '请稍后自行根据情况填入和更改各参数'.format(index),
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        # 恢复默认
        try:
            with open(self.conf_label.text(), 'w') as f:
                f.write(index)
            self.create_message_box('信息', '恢复初始状态成功')
        except Exception as e:
            self.create_message_box('错误', '写入conf文件失败,{}'.format(e))

        # 完成后读取conf文件内容
        self.read_conf()

    def fetch_conf_path(self):
        # 打开文件选择对话框
        filepath, _ = QFileDialog.getOpenFileName(self, "选择对应conf文件", "",
                                                  "eulerlauncher.conf文件 (eulerlauncher.conf)")
        if filepath:
            # 选中conf文件后显示conf文件路径
            self.conf_label.setText(filepath)

            # 读取conf文件内容
            self.read_conf()

    # 创建该程序中标准的消息框
    def create_message_box(self, title, text):
        message_box = QMessageBox(self)
        message_box.setIcon(QMessageBox.Information)
        message_box.setText(text)
        message_box.setWindowTitle(title)
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec()

    @staticmethod  # 创建该程序中标准的分割线 True为水平 False为垂直
    def create_line(horizon=True):
        line = QFrame()
        if horizon:
            line.setFrameShape(QFrame.HLine)
        else:
            line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    def load_qss_style(self):  # 读取 QSS 文件
        # 本字符串为GUI的样式表，用于设置GUI的样式，其为qss格式
        # 进行修改请在style字符串中进行
        style = """
        QWidget
        {
            font-family: "Arial", "SimHei", sans-serif;
            font-size: 14px;
        }
        QPushButton[name = 'menu']
        {
            color : black;
            padding-top : 10px;
            padding-bottom : 10px;
            padding-left : 10px;
            padding-right : 50px;
            min-width : 100px;
            border-left : 0;
            font-size : 18px;
            background-color: white;
            border-radius: 10px;
            text-align: left;
        }
        QPushButton[name = 'menu']:checked
        {
            background-color: #f0f0f0;
            border-left: 5px solid #87CEEB;
            padding-left : 5px;
        }
        QPushButton
        {
            color : black;
            padding : 10px;
            min-width : 80px;
        }
        QListWidget
        {
            color: black;
            border-radius: 10px;
        }
        QListWidget::item
        {
            padding: 5px;
        }
        #sidebar
        {
            background-color: white;
            width: 300px;
            color: black;
            border-radius: 10px;
        }
        QLineEdit
        {
            border-radius: 10px;
            border: 1px solid #87CEEB;
            padding: 10px;
        }
        QTextEdit
        {
            border-radius: 10px;
            border: 1px solid #87CEEB;
            padding: 3px;
        }
        """
        self.setStyleSheet(style)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EulerLauncherGUI()
    ex.show()
    sys.exit(app.exec())
