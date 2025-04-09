import tkinter as tk
from tkinter import messagebox, filedialog
import random
import json
import os

SAVE_FILE = "song_sorter_save.json"

songs = [
    "嫉妒", "after 17", "女明星 (Live)", "九份的咖啡店", "微凉的你", "吉他手", "天天想你",
    "雨水一盒 (A Box of Rain)", "被动 (Live)", "1234567", "孩子", "华生", "灵感 (Live)",
    "台北某个地方", "家 (Home)", "沙漏 (View with a Grain of Sand)", "倒数 (Count Down)",
    "流浪者之歌 (Gypsy in Memory)", "慢歌一", "最初的起点", "下午三点", "黑眼圈", "表面的和平",
    "一起去巴黎", "会不会 (Live)", "旅行的意义 (Live)", "让我想一想 (Live)", "1234567 (Live)",
    "等待 (Live)", "失败者的飞翔 (Live)", "倔强爱情的胜利 (Live)", "下个星期去英国 (Live)",
    "Self (Live)", "腐朽 (Live)", "La Vie En Rose (玫瑰人生)", "太聪明", "旅行的意义 (Guitar Ver.)",
    "我亲爱的偏执狂", "还是会寂寞", "告诉我", "慢歌1", "(失明前)我想记得的四十七件事", "鱼",
    "旅行的意义", "烟火", "80%完美的日子", "小尘埃", "夜游", "等待", "慢歌3", "越洋电话",
    "小步舞曲", "躺在你的衣柜 (Guitar)", "温室花朵", "让我想一想", "Self",
    "我的骄傲无可救药 (Live)", "小船"
]

songs = list(dict.fromkeys(songs))

class SongSorterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("歌曲偏好选择器")

        self.pairs = self.generate_song_pairs(songs)
        self.index = 0
        self.preferences = []
        self.scores = {song: 0 for song in songs}

        self.label = tk.Label(root, text="请选择你更喜欢的一首：", font=("Arial", 16))
        self.label.pack(pady=10)

        self.button1 = tk.Button(root, text="", width=40, height=2, command=self.choose_first)
        self.button2 = tk.Button(root, text="", width=40, height=2, command=self.choose_second)
        self.button1.pack(pady=5)
        self.button2.pack(pady=5)

        self.status = tk.Label(root, text="", font=("Arial", 10))
        self.status.pack(pady=10)

        self.save_button = tk.Button(root, text="保存进度", command=self.save_progress)
        self.save_button.pack(pady=5)

        self.load_previous_progress()

        if self.pairs:
            self.update_buttons()
        else:
            self.label.config(text="没有可比较的歌曲对。")
            self.button1.config(state="disabled")
            self.button2.config(state="disabled")

    def generate_song_pairs(self, songs):
        pairs = [(songs[i], songs[j]) for i in range(len(songs)) for j in range(i + 1, len(songs))]
        random.shuffle(pairs)
        return pairs

    def choose_first(self):
        if self.index < len(self.pairs):
            self.choose(self.pairs[self.index][0])

    def choose_second(self):
        if self.index < len(self.pairs):
            self.choose(self.pairs[self.index][1])

    def choose(self, song):
        if self.index >= len(self.pairs):
            return
        pair = self.pairs[self.index]
        self.preferences.append({'pair': pair, 'choice': song})
        self.scores[song] += 1
        self.index += 1
        if self.index >= len(self.pairs):
            self.show_result()
        else:
            self.update_buttons()

    def update_buttons(self):
        if self.index < len(self.pairs):
            a, b = self.pairs[self.index]
            self.button1.config(text=a)
            self.button2.config(text=b)
            self.status.config(text=f"第 {self.index + 1} / {len(self.pairs)} 对")

    def show_result(self):
        sorted_scores = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        result_window = tk.Toplevel(self.root)
        result_window.title("排序结果")
        tk.Label(result_window, text="你的歌曲偏好排序（含得分）：", font=("Arial", 14)).pack(pady=10)
        for i, (song, score) in enumerate(sorted_scores, 1):
            tk.Label(result_window, text=f"{i}. {song} - {score} 分", anchor="w").pack(fill="x")

        tk.Button(result_window, text="导出选择记录", command=self.export_history).pack(pady=10)

    def export_history(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                for pref in self.preferences:
                    a, b = pref['pair']
                    f.write(f"{a} vs {b} => {pref['choice']}\n")
            messagebox.showinfo("导出成功", f"已保存到: {file_path}")

    def save_progress(self):
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'pairs': self.pairs,
                'index': self.index,
                'preferences': self.preferences,
                'scores': self.scores
            }, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("保存成功", "进度已保存！")

    def load_previous_progress(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.pairs = data['pairs']
                self.index = data['index']
                self.preferences = data['preferences']
                self.scores = data['scores']
            messagebox.showinfo("进度已加载", f"继续上次进度，从第 {self.index + 1} 对开始。")

if __name__ == "__main__":
    root = tk.Tk()
    app = SongSorterGUI(root)
    root.mainloop()
