# src/main.py

import sys
import tkinter as tk
from tkinter import ttk
from gflzirc import GFLCaptureProxy, set_windows_proxy
from monitor.monitor_gui import MonitorApp
from target_train.train_gui import TargetTrainApp
from utils import global_i18n

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title(global_i18n.get("app_title"))
        self.root.geometry("600x650")
        
        self.proxy_capture = None
        
        self.setup_top_bar()
        self.monitor_app = MonitorApp(self.root, self.log)
        self.train_app = TargetTrainApp(self.root, self.get_config, self.log)
        self.setup_log_area()

    def log(self, msg):
        self.root.after(0, self._append_log, msg)

    def _append_log(self, msg):
        self.txt_log.config(state=tk.NORMAL)
        self.txt_log.insert(tk.END, msg + "\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state=tk.DISABLED)

    def get_config(self):
        return {
            "uid": self.var_uid.get(),
            "sign": self.var_sign.get(),
            "server": self.var_server.get()
        }

    def setup_top_bar(self):
        self.frame_top = ttk.LabelFrame(self.root, text=global_i18n.get("cfg_group"), padding=10)
        self.frame_top.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self.frame_top, text=global_i18n.get("uid")).grid(row=0, column=0, sticky=tk.W)
        self.var_uid = tk.StringVar()
        ttk.Entry(self.frame_top, textvariable=self.var_uid, width=30).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(self.frame_top, text=global_i18n.get("sign")).grid(row=1, column=0, sticky=tk.W)
        self.var_sign = tk.StringVar()
        ttk.Entry(self.frame_top, textvariable=self.var_sign, width=30).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(self.frame_top, text=global_i18n.get("server")).grid(row=2, column=0, sticky=tk.W)
        self.var_server = tk.StringVar()
        servers = [
            "M4A1 | http://gfcn-game.gw.merge.sunborngame.com/index.php/1000/Targettrain/addCollect",
            "AR15 | http://gfcn-game.bili.merge.sunborngame.com/index.php/5000/Targettrain/addCollect",
            "SOP | http://gfcn-game.ios.merge.sunborngame.com/index.php/3000/Targettrain/addCollect",
            "RO635 | http://gfcn-game.ly.merge.sunborngame.com/index.php/4000/Targettrain/addCollect",
            "M16 | http://gfcn-game.tx.sunborngame.com/index.php/2000/Targettrain/addCollect"
        ]
        cb = ttk.Combobox(self.frame_top, textvariable=self.var_server, values=servers, width=45)
        cb.grid(row=2, column=1, padx=5, pady=2)
        cb.current(0)

        self.btn_cap = ttk.Button(self.frame_top, text=global_i18n.get("btn_capture"), command=self.start_capture)
        self.btn_cap.grid(row=0, column=2, padx=5)
        
        self.btn_stop_cap = ttk.Button(self.frame_top, text=global_i18n.get("btn_stop_capture"), command=self.stop_capture, state=tk.DISABLED)
        self.btn_stop_cap.grid(row=1, column=2, padx=5)

    def setup_log_area(self):
        f = ttk.LabelFrame(self.root, text=global_i18n.get("log_console"), padding=5)
        f.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.txt_log = tk.Text(f, height=10, state=tk.DISABLED)
        self.txt_log.pack(fill=tk.BOTH, expand=True)

    def on_keys_captured(self, uid, sign):
        self.root.after(0, self.var_uid.set, uid)
        self.root.after(0, self.var_sign.set, sign)
        self.log(f"[SYS] Captured UID: {uid}")

    def start_capture(self):
        if not self.proxy_capture:
            self.proxy_capture = GFLCaptureProxy(8080, "yundoudou", self.on_keys_captured)
            self.proxy_capture.start()
            set_windows_proxy(True, "127.0.0.1:8080")
            self.log("[SYS] Capture proxy started on 8080.")
            self.btn_cap.config(state=tk.DISABLED)
            self.btn_stop_cap.config(state=tk.NORMAL)

    def stop_capture(self):
        if self.proxy_capture:
            self.proxy_capture.stop()
            set_windows_proxy(False)
            self.proxy_capture = None
            self.log("[SYS] Capture proxy stopped.")
            self.btn_cap.config(state=tk.NORMAL)
            self.btn_stop_cap.config(state=tk.DISABLED)

    def on_close(self):
        self.stop_capture()
        self.monitor_app.stop_monitor()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()