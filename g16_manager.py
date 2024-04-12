import os
import tkinter as tk
from tkinter import filedialog, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
import subprocess
import threading
import atexit
import platform

class GaussianCalcQueue:
    def __init__(self, master):
        self.master = master
        self.setup_gui()
        self.pending_files = []  # 未計算リスト
        self.running = False  # 計算が実行中かどうかを追跡
        atexit.register(self.cleanup)  # アプリケーション終了時に実行する関数を登録

    def setup_gui(self):
        self.master.title('G16 Manager')
        self.master.geometry('600x450')  # GUIのサイズを設定

        # ボタンフレームの設定
        self.btn_frame = ttk.Frame(self.master)
        self.btn_frame.pack(fill=tk.X, padx=10, pady=5)

        self.add_file_btn = ttk.Button(self.btn_frame, text="Add Files", command=self.select_file)
        self.add_file_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.move_up_btn = ttk.Button(self.btn_frame, text="Up", command=self.move_up)
        self.move_up_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.move_down_btn = ttk.Button(self.btn_frame, text="Down", command=self.move_down)
        self.move_down_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.clear_btn = ttk.Button(self.btn_frame, text="Clear Selected", command=self.clear_selected)
        self.clear_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 未計算ファイルリストの設定
        self.pending_frame = ttk.LabelFrame(self.master, text="Pending Files")
        self.pending_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=0)

        self.pending_list = tk.Listbox(self.pending_frame, selectmode=tk.EXTENDED)
        self.pending_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.pending_scrollbar = ttk.Scrollbar(self.pending_frame, orient=tk.VERTICAL, command=self.pending_list.yview)
        self.pending_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.pending_list.config(yscrollcommand=self.pending_scrollbar.set)

        # 計算中ファイルリストの設定
        self.running_frame = ttk.LabelFrame(self.master, text="Running Calculations")
        self.running_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.running_list = tk.Listbox(self.running_frame, selectmode=tk.EXTENDED)
        self.running_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.running_scrollbar = ttk.Scrollbar(self.running_frame, orient=tk.VERTICAL, command=self.running_list.yview)
        self.running_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.running_list.config(yscrollcommand=self.running_scrollbar.set)

        self.start_btn = ttk.Button(self.master, text="Start Calculations", command=self.start_calculation)
        self.start_btn.pack(pady=5)

        self.master.drop_target_register(DND_FILES)
        self.master.dnd_bind('<<Drop>>', self.drop)

    def select_file(self):
        file_paths = filedialog.askopenfilenames(initialdir="/", title="Select files",
                                                 filetypes=(("gjf files", "*.gjf"), ("all files", "*.*")))
        for file_path in file_paths:
            if file_path.endswith('.gjf'):
                self.pending_list.insert(tk.END, file_path)

    def clear_selected(self):
        for item in self.pending_list.curselection()[::-1]:
            self.pending_list.delete(item)

    def move_up(self):
        pos_list = self.pending_list.curselection()
        for pos in pos_list:
            if pos > 0:
                text = self.pending_list.get(pos)
                self.pending_list.delete(pos)
                self.pending_list.insert(pos-1, text)
                self.pending_list.select_set(pos-1)

    def move_down(self):
        pos_list = reversed(self.pending_list.curselection())
        for pos in pos_list:
            if pos < self.pending_list.size() - 1:
                text = self.pending_list.get(pos)
                self.pending_list.delete(pos)
                self.pending_list.insert(pos+1, text)
                self.pending_list.select_set(pos+1)

    def drop(self, event):
        file_paths = self.master.tk.splitlist(event.data)
        for file_path in file_paths:
            if file_path.endswith('.gjf'):
                self.pending_list.insert(tk.END, file_path)

    def start_calculation(self):
        if not self.running and self.pending_list.size() > 0:
            self.running = True
            threading.Thread(target=self.run_calculation).start()

    def run_calculation(self):
        while self.pending_list.size() > 0 and self.running:
            file_path = self.pending_list.get(0)
            self.pending_files.append(file_path)  # Store for cleanup
            self.master.after(0, self.pending_list.delete, 0)
            self.master.after(0, self.running_list.insert, tk.END, file_path)

            output_file = file_path.rsplit('.', 1)[0] + '.out'
            cmd = f'g16 "{file_path}" "{output_file}"'
            subprocess.run(cmd, cwd=r'C:\G16W', shell=True)
            self.master.after(0, self.post_calculation, file_path)
        self.running = False

    def post_calculation(self, file_path):
        index = self.running_list.get(0, tk.END).index(file_path)
        self.master.after(0, self.running_list.delete, index)

    def cleanup(self):
        try:
            if platform.system() == 'Windows':
                subprocess.run(['taskkill', '/F', '/IM', 'g16.exe'], check=True)
            else:
                subprocess.run(['killall', 'g16'], check=True)
        except subprocess.CalledProcessError as e:
            print("Error terminating g16 process:", e)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = GaussianCalcQueue(root)
    root.mainloop()
