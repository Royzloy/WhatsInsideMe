import tkinter as tk
from tkinter import ttk, scrolledtext, Menu, filedialog, messagebox
import platform
import psutil
import socket
import getpass
import os
import GPUtil
import threading
import time
import subprocess
import tempfile
import datetime
import screeninfo
import sounddevice as sd
from fpdf import FPDF
import json
import sys

LOGO = """
╔╗╔╗╔╗╔╗╔╗╔══╗╔════╗╔══╗╔══╗╔╗─╔╗╔══╗╔══╗╔══╗─╔═══╗╔╗──╔╗╔═══╗
║║║║║║║║║║║╔╗║╚═╗╔═╝║╔═╝╚╗╔╝║╚═╝║║╔═╝╚╗╔╝║╔╗╚╗║╔══╝║║──║║║╔══╝
║║║║║║║╚╝║║╚╝║──║║──║╚═╗─║║─║╔╗─║║╚═╗─║║─║║╚╗║║╚══╗║╚╗╔╝║║╚══╗
║║║║║║║╔╗║║╔╗║──║║──╚═╗║─║║─║║╚╗║╚═╗║─║║─║║─║║║╔══╝║╔╗╔╗║║╔══╝
║╚╝╚╝║║║║║║║║║──║║──╔═╝║╔╝╚╗║║─║║╔═╝║╔╝╚╗║╚═╝║║╚══╗║║╚╝║║║╚══╗
╚═╝╚═╝╚╝╚╝╚╝╚╝──╚╝──╚══╝╚══╝╚╝─╚╝╚══╝╚══╝╚═══╝╚═══╝╚╝──╚╝╚═══╝
"""

TRANSLATIONS = {
    'en': {
        'tab_main': 'Main',
        'tab_settings': 'Settings',
        'refresh_btn': 'Refresh',
        'menu_file': 'File',
        'menu_save_as': 'Save as...',
        'menu_print': 'Print',
        'menu_exit': 'Exit',
        'menu_help': 'Help',
        'menu_about': 'About',
        'about_title': 'About',
        'about_text': 'WhatsInsideMe v26.1.3\nProgram for collecting system information.\n\nDeveloped with Python, tkinter, psutil, gputil, screeninfo, sounddevice.\n\n© 2026',
        'no_data': 'No data',
        'no_data_msg': 'First collect information (click Refresh).',
        'save_error': 'Error',
        'save_error_msg': 'Could not save file:\n{}',
        'print_error': 'Print error',
        'print_error_msg': 'Could not print:\n{}',
        'success': 'Success',
        'success_msg': 'Report saved to {}',
        'language': 'Language',
        'english': 'English',
        'russian': 'Russian',
        'collecting': 'Collecting information...',
        'end_of_report': '--- End of report ---',
        'report_generated': 'Report generated: {}',
        'section_system': 'System Information',
        'section_cpu': 'CPU Information',
        'section_memory': 'Memory Information',
        'section_battery': 'Battery Information',
        'section_disks': 'Disk Information',
        'section_network': 'Network Information',
        'section_gpu': 'GPU Information',
        'section_monitors': 'Monitor Information',
        'section_audio': 'Audio Devices',
        'label_hostname': 'Hostname',
        'label_username': 'Username',
        'label_os': 'OS',
        'label_os_version': 'OS Version',
        'label_architecture': 'Architecture',
        'label_python_version': 'Python Version',
        'label_model': 'Model',
        'label_physical_cores': 'Physical cores',
        'label_logical_cores': 'Logical cores',
        'label_max_freq': 'Max Frequency (MHz)',
        'label_current_freq': 'Current Frequency (MHz)',
        'label_usage': 'Usage',
        'label_total': 'Total',
        'label_available': 'Available',
        'label_used': 'Used',
        'label_percent': 'Usage',
        'label_charge': 'Charge',
        'label_plugged_in': 'Plugged in',
        'label_time_left': 'Time left',
        'label_device': 'Device',
        'label_mountpoint': 'Mountpoint',
        'label_filesystem': 'File system',
        'label_free': 'Free',
        'label_interface': 'Interface',
        'label_ip': 'IP',
        'label_netmask': 'Netmask',
        'label_broadcast': 'Broadcast',
        'label_mac': 'MAC',
        'label_name': 'Name',
        'label_load': 'Load',
        'label_memory_total': 'Memory Total',
        'label_memory_used': 'Memory Used',
        'label_memory_free': 'Memory Free',
        'label_temperature': 'Temperature',
        'label_resolution': 'Resolution',
        'label_primary': 'Primary',
        'label_inputs': 'Inputs',
        'label_outputs': 'Outputs',
        'label_sample_rate': 'Sample rate',
        'no_disk_info': 'No disk information available.',
        'no_network_info': 'No network information available.',
        'no_gpu': 'No GPU detected or GPUtil not installed.',
        'no_monitor_info': 'No monitor information available.',
        'no_audio_info': 'No audio devices found or sounddevice not installed.',
        'true': 'True',
        'false': 'False',
        'unknown': 'Unknown',
    },
    'ru': {
        'tab_main': 'Главная',
        'tab_settings': 'Настройки',
        'refresh_btn': 'Обновить',
        'menu_file': 'Файл',
        'menu_save_as': 'Сохранить как...',
        'menu_print': 'Печать',
        'menu_exit': 'Выход',
        'menu_help': 'Справка',
        'menu_about': 'О программе',
        'about_title': 'О программе',
        'about_text': 'WhatsInsideMe v26.1.3\nПрограмма для сбора информации о системе.\n\nРазработано с использованием Python, tkinter, psutil, gputil, screeninfo, sounddevice.\n\n© 2026',
        'no_data': 'Нет данных',
        'no_data_msg': 'Сначала соберите информацию (нажмите Обновить).',
        'save_error': 'Ошибка',
        'save_error_msg': 'Не удалось сохранить файл:\n{}',
        'print_error': 'Ошибка печати',
        'print_error_msg': 'Не удалось напечатать:\n{}',
        'success': 'Успех',
        'success_msg': 'Отчёт сохранён в {}',
        'language': 'Язык',
        'english': 'Английский',
        'russian': 'Русский',
        'collecting': 'Сбор информации...',
        'end_of_report': '--- Конец отчёта ---',
        'report_generated': 'Отчёт сформирован: {}',
        'section_system': 'Информация о системе',
        'section_cpu': 'Информация о процессоре',
        'section_memory': 'Информация о памяти',
        'section_battery': 'Информация о батарее',
        'section_disks': 'Информация о дисках',
        'section_network': 'Информация о сети',
        'section_gpu': 'Информация о видеокарте',
        'section_monitors': 'Информация о мониторах',
        'section_audio': 'Аудиоустройства',
        'label_hostname': 'Имя компьютера',
        'label_username': 'Имя пользователя',
        'label_os': 'ОС',
        'label_os_version': 'Версия ОС',
        'label_architecture': 'Архитектура',
        'label_python_version': 'Версия Python',
        'label_model': 'Модель',
        'label_physical_cores': 'Физических ядер',
        'label_logical_cores': 'Логических ядер',
        'label_max_freq': 'Макс. частота (МГц)',
        'label_current_freq': 'Тек. частота (МГц)',
        'label_usage': 'Загрузка',
        'label_total': 'Всего',
        'label_available': 'Доступно',
        'label_used': 'Использовано',
        'label_percent': 'Использование',
        'label_charge': 'Заряд',
        'label_plugged_in': 'Подключен к сети',
        'label_time_left': 'Осталось времени',
        'label_device': 'Устройство',
        'label_mountpoint': 'Точка монтирования',
        'label_filesystem': 'Файловая система',
        'label_free': 'Свободно',
        'label_interface': 'Интерфейс',
        'label_ip': 'IP',
        'label_netmask': 'Маска',
        'label_broadcast': 'Broadcast',
        'label_mac': 'MAC',
        'label_name': 'Название',
        'label_load': 'Загрузка',
        'label_memory_total': 'Память всего',
        'label_memory_used': 'Использовано памяти',
        'label_memory_free': 'Свободно памяти',
        'label_temperature': 'Температура',
        'label_resolution': 'Разрешение',
        'label_primary': 'Основной',
        'label_inputs': 'Входы',
        'label_outputs': 'Выходы',
        'label_sample_rate': 'Частота дискретизации',
        'no_disk_info': 'Нет информации о дисках.',
        'no_network_info': 'Нет информации о сети.',
        'no_gpu': 'Видеокарта не обнаружена или GPUtil не установлен.',
        'no_monitor_info': 'Нет информации о мониторах.',
        'no_audio_info': 'Аудиоустройства не найдены или sounddevice не установлен.',
        'true': 'Да',
        'false': 'Нет',
        'unknown': 'Неизвестно',
    }
}

def get_config_path():
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, 'config.json')

class SystemInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsInsideMe - System Information")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.configure(bg='black')

        self.config_file = get_config_path()
        self.load_config()

        self.translations = TRANSLATIONS
        self.font = ("Courier New", 10)
        self.info = None

        self.top_frame = tk.Frame(root, bg='black')
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        self.notebook = ttk.Notebook(self.top_frame)
        self.notebook.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.main_tab = tk.Frame(self.notebook, bg='black')
        self.notebook.add(self.main_tab, text=self.t('tab_main'))

        self.settings_tab = tk.Frame(self.notebook, bg='black')
        self.notebook.add(self.settings_tab, text=self.t('tab_settings'))

        self.refresh_btn = tk.Button(self.top_frame, text=self.t('refresh_btn'),
                                     command=self.refresh_data, bg='gray', fg='white')
        self.refresh_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        self.text_area = scrolledtext.ScrolledText(
            self.main_tab, wrap=tk.NONE, font=self.font,
            bg='black', fg='lime', insertbackground='lime'
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.setup_tags()
        self.create_menu()
        self.setup_settings_tab()
        self.show_logo()
        self.refresh_data()

    def load_config(self):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.lang = config.get('language', 'en')
        except (FileNotFoundError, json.JSONDecodeError):
            self.lang = 'en'
            self.save_config()

    def save_config(self):
        config = {'language': self.lang}
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
        except Exception:
            pass

    def t(self, key):
        return TRANSLATIONS[self.lang].get(key, key)

    def tr_bool(self, value):
        return self.t('true') if value else self.t('false')

    def setup_tags(self):
        self.text_area.tag_config("logo", foreground="cyan", font=("Courier New", 12, "bold"))
        self.text_area.tag_config("header", foreground="yellow", font=("Courier New", 11, "bold"))
        self.text_area.tag_config("section_title", foreground="magenta", font=("Courier New", 11, "bold"))
        self.text_area.tag_config("key", foreground="lightblue")
        self.text_area.tag_config("value", foreground="white")
        self.text_area.tag_config("border", foreground="green")

    def setup_settings_tab(self):
        settings_frame = tk.Frame(self.settings_tab, bg='black')
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        lang_label = tk.Label(settings_frame, text=self.t('language'),
                              font=('Arial', 12, 'bold'), fg='lime', bg='black')
        lang_label.pack(anchor=tk.W, pady=5)

        self.lang_var = tk.StringVar(value=self.lang)

        rb_en = tk.Radiobutton(settings_frame, text=self.t('english'),
                               variable=self.lang_var, value='en',
                               command=self.on_language_change,
                               fg='lime', bg='black', selectcolor='black', activebackground='black')
        rb_en.pack(anchor=tk.W, padx=20)

        rb_ru = tk.Radiobutton(settings_frame, text=self.t('russian'),
                               variable=self.lang_var, value='ru',
                               command=self.on_language_change,
                               fg='lime', bg='black', selectcolor='black', activebackground='black')
        rb_ru.pack(anchor=tk.W, padx=20)

        self.settings_widgets = {
            'lang_label': lang_label,
            'rb_en': rb_en,
            'rb_ru': rb_ru
        }

    def on_language_change(self):
        new_lang = self.lang_var.get()
        if new_lang != self.lang:
            self.change_language(new_lang)

    def change_language(self, new_lang):
        self.lang = new_lang
        self.save_config()
        self.notebook.tab(0, text=self.t('tab_main'))
        self.notebook.tab(1, text=self.t('tab_settings'))
        self.refresh_btn.config(text=self.t('refresh_btn'))
        self.settings_widgets['lang_label'].config(text=self.t('language'))
        self.settings_widgets['rb_en'].config(text=self.t('english'))
        self.settings_widgets['rb_ru'].config(text=self.t('russian'))
        self.create_menu()
        if self.info:
            self.display_info()

    def create_menu(self):
        if hasattr(self, 'menubar'):
            self.root.config(menu='')
        self.menubar = Menu(self.root)
        file_menu = Menu(self.menubar, tearoff=0)
        file_menu.add_command(label=self.t('menu_save_as'), command=self.save_as_dialog)
        file_menu.add_command(label=self.t('menu_print'), command=self.print_document)
        file_menu.add_separator()
        file_menu.add_command(label=self.t('menu_exit'), command=self.root.quit)
        self.menubar.add_cascade(label=self.t('menu_file'), menu=file_menu)
        help_menu = Menu(self.menubar, tearoff=0)
        help_menu.add_command(label=self.t('menu_about'), command=self.show_about)
        self.menubar.add_cascade(label=self.t('menu_help'), menu=help_menu)
        self.root.config(menu=self.menubar)

    def show_logo(self):
        self.text_area.insert(tk.END, LOGO + "\n\n", "logo")
        self.text_area.see(tk.END)
        self.root.update()

    def refresh_data(self):
        self.text_area.delete(1.0, tk.END)
        self.show_logo()
        self.text_area.insert(tk.END, self.t('collecting') + "\n", "header")
        self.root.update()
        thread = threading.Thread(target=self.collect_and_display, daemon=True)
        thread.start()

    def collect_and_display(self):
        time.sleep(1)
        self.info = self.get_system_info()
        self.root.after(0, self.display_info)

    def get_system_info(self):
        info = {}
        info['hostname'] = socket.gethostname()
        info['username'] = getpass.getuser()
        info['os'] = platform.system()
        info['os_version'] = platform.version()
        info['architecture'] = platform.machine()
        info['python_version'] = platform.python_version()
        info['cpu'] = {
            'model': platform.processor(),
            'cores_physical': psutil.cpu_count(logical=False),
            'cores_logical': psutil.cpu_count(logical=True),
            'max_freq': psutil.cpu_freq().max if psutil.cpu_freq() else "N/A",
            'current_freq': psutil.cpu_freq().current if psutil.cpu_freq() else "N/A",
            'usage_percent': psutil.cpu_percent(interval=1)
        }
        mem = psutil.virtual_memory()
        info['memory'] = {
            'total': self.get_size(mem.total),
            'available': self.get_size(mem.available),
            'used': self.get_size(mem.used),
            'percent': mem.percent
        }
        partitions = psutil.disk_partitions()
        disk_info = []
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': self.get_size(usage.total),
                    'used': self.get_size(usage.used),
                    'free': self.get_size(usage.free),
                    'percent': usage.percent
                })
            except PermissionError:
                continue
        info['disks'] = disk_info
        addrs = psutil.net_if_addrs()
        net_info = []
        for interface, addr_list in addrs.items():
            for addr in addr_list:
                if addr.family == socket.AF_INET:
                    net_info.append({
                        'interface': interface,
                        'ip': addr.address,
                        'netmask': addr.netmask,
                        'broadcast': addr.broadcast
                    })
                elif addr.family == psutil.AF_LINK:
                    net_info.append({
                        'interface': interface,
                        'mac': addr.address
                    })
        info['network'] = net_info
        try:
            gpus = GPUtil.getGPUs()
            gpu_info = []
            for gpu in gpus:
                gpu_info.append({
                    'name': gpu.name,
                    'load': f"{gpu.load*100:.1f}%",
                    'memory_total': self.get_size(gpu.memoryTotal * 1024 * 1024),
                    'memory_used': self.get_size(gpu.memoryUsed * 1024 * 1024),
                    'memory_free': self.get_size(gpu.memoryFree * 1024 * 1024),
                    'temperature': f"{gpu.temperature}°C" if gpu.temperature else "N/A"
                })
            info['gpu'] = gpu_info
        except:
            info['gpu'] = None
        try:
            monitors = screeninfo.get_monitors()
            monitor_info = []
            for m in monitors:
                monitor_info.append({
                    'name': m.name,
                    'width': m.width,
                    'height': m.height,
                    'primary': m.is_primary
                })
            info['monitors'] = monitor_info
        except:
            info['monitors'] = None
        try:
            devices = sd.query_devices()
            audio_info = []
            for i, dev in enumerate(devices):
                audio_info.append({
                    'index': i,
                    'name': dev['name'],
                    'max_inputs': dev['max_input_channels'],
                    'max_outputs': dev['max_output_channels'],
                    'default_samplerate': dev['default_samplerate']
                })
            info['audio'] = audio_info
        except:
            info['audio'] = None
        battery = psutil.sensors_battery()
        if battery:
            info['battery'] = {
                'percent': battery.percent,
                'plugged': battery.power_plugged,
                'time_left': battery.secsleft if battery.secsleft != -1 else self.t('unknown')
            }
        else:
            info['battery'] = None
        info['report_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return info

    @staticmethod
    def get_size(bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor
        return f"{bytes:.2f}Y{suffix}"

    def insert_line(self, line, tag="data", indent=0):
        self.text_area.insert(tk.END, " " * indent + line + "\n", tag)
        self.text_area.see(tk.END)
        self.root.update()

    def display_info(self):
        if not self.info:
            return
        self.text_area.delete(1.0, tk.END)
        self.show_logo()
        info = self.info

        def insert_bordered_line(left_key, right_value, tag="data"):
            left = self.t(left_key)
            if isinstance(right_value, bool):
                right_value = self.tr_bool(right_value)
            else:
                right_value = str(right_value)
            line = f"║ {left:<20} : {right_value:<47} ║"
            self.text_area.insert(tk.END, line + "\n", tag)

        self.insert_line("╔" + "═"*70 + "╗", "border")
        self.insert_line("║{:^70}║".format(self.t('section_system')), "header")
        self.insert_line("╠" + "═"*70 + "╣", "border")
        insert_bordered_line('label_hostname', info['hostname'], "key")
        insert_bordered_line('label_username', info['username'], "key")
        insert_bordered_line('label_os', info['os'], "key")
        insert_bordered_line('label_os_version', info['os_version'], "key")
        insert_bordered_line('label_architecture', info['architecture'], "key")
        insert_bordered_line('label_python_version', info['python_version'], "key")
        self.insert_line("╚" + "═"*70 + "╝", "border")
        self.insert_line("")

        self.insert_line("╔" + "═"*70 + "╗", "border")
        self.insert_line("║{:^70}║".format(self.t('section_cpu')), "header")
        self.insert_line("╠" + "═"*70 + "╣", "border")
        insert_bordered_line('label_model', info['cpu']['model'], "key")
        insert_bordered_line('label_physical_cores', info['cpu']['cores_physical'], "key")
        insert_bordered_line('label_logical_cores', info['cpu']['cores_logical'], "key")
        insert_bordered_line('label_max_freq', info['cpu']['max_freq'], "key")
        insert_bordered_line('label_current_freq', info['cpu']['current_freq'], "key")
        insert_bordered_line('label_usage', f"{info['cpu']['usage_percent']}%", "key")
        self.insert_line("╚" + "═"*70 + "╝", "border")
        self.insert_line("")

        self.insert_line("╔" + "═"*70 + "╗", "border")
        self.insert_line("║{:^70}║".format(self.t('section_memory')), "header")
        self.insert_line("╠" + "═"*70 + "╣", "border")
        insert_bordered_line('label_total', info['memory']['total'], "key")
        insert_bordered_line('label_available', info['memory']['available'], "key")
        insert_bordered_line('label_used', info['memory']['used'], "key")
        insert_bordered_line('label_percent', f"{info['memory']['percent']}%", "key")
        self.insert_line("╚" + "═"*70 + "╝", "border")
        self.insert_line("")

        if info['battery']:
            self.insert_line("╔" + "═"*70 + "╗", "border")
            self.insert_line("║{:^70}║".format(self.t('section_battery')), "header")
            self.insert_line("╠" + "═"*70 + "╣", "border")
            insert_bordered_line('label_charge', f"{info['battery']['percent']}%", "key")
            insert_bordered_line('label_plugged_in', info['battery']['plugged'], "key")
            insert_bordered_line('label_time_left', info['battery']['time_left'], "key")
            self.insert_line("╚" + "═"*70 + "╝", "border")
            self.insert_line("")

        if info['disks']:
            self.insert_line("╔" + "═"*70 + "╗", "border")
            self.insert_line("║{:^70}║".format(self.t('section_disks')), "header")
            self.insert_line("╠" + "═"*70 + "╣", "border")
            for disk in info['disks']:
                insert_bordered_line('label_device', disk['device'], "key")
                insert_bordered_line('label_mountpoint', disk['mountpoint'], "key")
                insert_bordered_line('label_filesystem', disk['fstype'], "key")
                insert_bordered_line('label_total', disk['total'], "key")
                insert_bordered_line('label_used', f"{disk['used']} ({disk['percent']}%)", "key")
                insert_bordered_line('label_free', disk['free'], "key")
                self.insert_line("╠" + "═"*70 + "╣", "border")
            self.text_area.delete("end-2l", "end-1l")
            self.insert_line("╚" + "═"*70 + "╝", "border")
            self.insert_line("")
        else:
            self.insert_line(self.t('no_disk_info'), "value")
            self.insert_line("")

        if info['network']:
            self.insert_line("╔" + "═"*70 + "╗", "border")
            self.insert_line("║{:^70}║".format(self.t('section_network')), "header")
            self.insert_line("╠" + "═"*70 + "╣", "border")
            for net in info['network']:
                if 'ip' in net:
                    line = f"{self.t('label_interface')}: {net['interface']} | {self.t('label_ip')}: {net['ip']} | {self.t('label_netmask')}: {net['netmask']}"
                    if net.get('broadcast'):
                        line += f" | {self.t('label_broadcast')}: {net['broadcast']}"
                elif 'mac' in net:
                    line = f"{self.t('label_interface')}: {net['interface']} | {self.t('label_mac')}: {net['mac']}"
                else:
                    continue
                if len(line) > 66:
                    line = line[:63] + "..."
                self.insert_line("║ {:<68} ║".format(line), "value")
            self.insert_line("╚" + "═"*70 + "╝", "border")
            self.insert_line("")
        else:
            self.insert_line(self.t('no_network_info'), "value")
            self.insert_line("")

        if info['gpu']:
            self.insert_line("╔" + "═"*70 + "╗", "border")
            self.insert_line("║{:^70}║".format(self.t('section_gpu')), "header")
            self.insert_line("╠" + "═"*70 + "╣", "border")
            for gpu in info['gpu']:
                insert_bordered_line('label_name', gpu['name'], "key")
                insert_bordered_line('label_load', gpu['load'], "key")
                insert_bordered_line('label_memory_total', gpu['memory_total'], "key")
                insert_bordered_line('label_memory_used', gpu['memory_used'], "key")
                insert_bordered_line('label_memory_free', gpu['memory_free'], "key")
                insert_bordered_line('label_temperature', gpu['temperature'], "key")
                self.insert_line("╠" + "═"*70 + "╣", "border")
            self.text_area.delete("end-2l", "end-1l")
            self.insert_line("╚" + "═"*70 + "╝", "border")
            self.insert_line("")
        else:
            self.insert_line(self.t('no_gpu'), "value")
            self.insert_line("")

        if info['monitors']:
            self.insert_line("╔" + "═"*70 + "╗", "border")
            self.insert_line("║{:^70}║".format(self.t('section_monitors')), "header")
            self.insert_line("╠" + "═"*70 + "╣", "border")
            for i, mon in enumerate(info['monitors']):
                insert_bordered_line(f"Monitor {i+1}", "", "key")
                insert_bordered_line('  ' + self.t('label_name'), mon['name'], "key")
                insert_bordered_line('  ' + self.t('label_resolution'), f"{mon['width']}x{mon['height']}", "key")
                insert_bordered_line('  ' + self.t('label_primary'), mon['primary'], "key")
                self.insert_line("╠" + "═"*70 + "╣", "border")
            self.text_area.delete("end-2l", "end-1l")
            self.insert_line("╚" + "═"*70 + "╝", "border")
            self.insert_line("")
        else:
            self.insert_line(self.t('no_monitor_info'), "value")
            self.insert_line("")

        if info['audio']:
            self.insert_line("╔" + "═"*70 + "╗", "border")
            self.insert_line("║{:^70}║".format(self.t('section_audio')), "header")
            self.insert_line("╠" + "═"*70 + "╣", "border")
            for dev in info['audio'][:10]:
                insert_bordered_line(f"{self.t('label_name')} {dev['index']}", dev['name'], "key")
                insert_bordered_line('  ' + self.t('label_inputs'), dev['max_inputs'], "key")
                insert_bordered_line('  ' + self.t('label_outputs'), dev['max_outputs'], "key")
                insert_bordered_line('  ' + self.t('label_sample_rate'), dev['default_samplerate'], "key")
                self.insert_line("╠" + "═"*70 + "╣", "border")
            self.text_area.delete("end-2l", "end-1l")
            self.insert_line("╚" + "═"*70 + "╝", "border")
        else:
            self.insert_line(self.t('no_audio_info'), "value")

        self.insert_line("")
        self.insert_line("╔" + "═"*70 + "╗", "border")
        self.insert_line("║{:^70}║".format(self.t('report_generated').format(info['report_time'])), "header")
        self.insert_line("╚" + "═"*70 + "╝", "border")
        self.insert_line("")
        self.insert_line(self.t('end_of_report'), "header")

    def save_as_dialog(self):
        if not self.info:
            messagebox.showwarning(self.t('no_data'), self.t('no_data_msg'))
            return
        file_types = [
            ("Text files", "*.txt"),
            ("HTML files", "*.html"),
            ("PDF files", "*.pdf")
        ]
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=file_types,
            title=self.t('menu_save_as')
        )
        if not filename:
            return
        ext = os.path.splitext(filename)[1].lower()
        try:
            if ext == ".txt":
                self.export_txt(filename)
            elif ext == ".html":
                self.export_html(filename)
            elif ext == ".pdf":
                self.export_pdf(filename)
            else:
                messagebox.showerror(self.t('save_error'), "Unsupported file format.")
                return
            messagebox.showinfo(self.t('success'), self.t('success_msg').format(filename))
        except Exception as e:
            messagebox.showerror(self.t('save_error'), self.t('save_error_msg').format(str(e)))

    def export_txt(self, filename):
        content = self.text_area.get(1.0, tk.END)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

    def export_html(self, filename):
        content = self.text_area.get(1.0, tk.END)
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>WhatsInsideMe Report</title>
    <style>
        body {{ background-color: black; color: lime; font-family: 'Courier New', monospace; white-space: pre; }}
        .header {{ color: yellow; font-weight: bold; }}
        .border {{ color: green; }}
        .key {{ color: lightblue; }}
        .value {{ color: white; }}
    </style>
</head>
<body>
<pre>
{content}
</pre>
</body>
</html>"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

    def export_pdf(self, filename):
        class PDF(FPDF):
            def header(self):
                pass
            def footer(self):
                self.set_y(-15)
                self.set_font('Courier', 'I', 8)
                self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        pdf = PDF()
        pdf.add_page()
        pdf.set_font('Courier', '', 10)
        pdf.set_text_color(0, 255, 0)
        content = self.text_area.get(1.0, tk.END).splitlines()
        for line in content:
            if len(line.encode('latin-1', 'ignore')) > 180:
                line = line[:80] + "..."
            safe_line = line.encode('latin-1', 'ignore').decode('latin-1')
            pdf.cell(0, 5, safe_line, ln=True)
        pdf.output(filename)

    def print_document(self):
        if not self.info:
            messagebox.showwarning(self.t('no_data'), self.t('no_data_msg'))
            return
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            content = self.text_area.get(1.0, tk.END)
            f.write(content)
            tempname = f.name
        try:
            if os.name == 'nt':
                os.startfile(tempname, 'print')
            else:
                subprocess.run(['lp', tempname], check=True)
            self.root.after(5000, lambda: os.remove(tempname))
        except Exception as e:
            messagebox.showerror(self.t('print_error'), self.t('print_error_msg').format(str(e)))
            os.remove(tempname)

    def show_about(self):
        messagebox.showinfo(self.t('about_title'), self.t('about_text'))

def main():
    root = tk.Tk()
    app = SystemInfoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()