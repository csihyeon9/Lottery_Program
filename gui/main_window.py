import tkinter as tk
from tkinter import ttk, messagebox

from services.participant_service import add_participant
from services.prize_service import get_prizes, init_prize_file
from services.draw_service import draw_with_prize
from gui.draw_screen import DrawScreen
from services.draw_service import get_candidate_names


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎁 경품 추첨 프로그램")
        self.root.geometry("650x450")
        self.root.resizable(False, False)

        self.create_tabs()

    def create_tabs(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both")

        # 탭 프레임
        self.tab_participant = ttk.Frame(notebook)
        self.tab_prize = ttk.Frame(notebook)
        self.tab_draw = ttk.Frame(notebook)

        notebook.add(self.tab_participant, text="참가자 관리")
        notebook.add(self.tab_prize, text="경품 관리")
        notebook.add(self.tab_draw, text="추첨")

        self.create_participant_tab()
        self.create_prize_tab()
        self.create_draw_tab()

    # ================= 참가자 탭 =================
    def create_participant_tab(self):
        frame = ttk.LabelFrame(self.tab_participant, text="참가자 입력")
        frame.pack(padx=20, pady=20, fill="x")

        ttk.Label(frame, text="이름").grid(row=0, column=0, padx=10, pady=10)
        ttk.Label(frame, text="소속").grid(row=1, column=0, padx=10, pady=10)

        self.name_entry = ttk.Entry(frame, width=30)
        self.org_entry = ttk.Entry(frame, width=30)

        self.name_entry.grid(row=0, column=1)
        self.org_entry.grid(row=1, column=1)

        ttk.Button(
            frame,
            text="참가자 저장",
            command=self.save_participant
        ).grid(row=2, column=0, columnspan=2, pady=10)

    def save_participant(self):
        name = self.name_entry.get()
        org = self.org_entry.get()

        if not name or not org:
            messagebox.showwarning("경고", "이름과 소속을 입력하세요.")
            return

        add_participant(name, org)
        messagebox.showinfo("완료", "참가자가 저장되었습니다.")

        self.name_entry.delete(0, tk.END)
        self.org_entry.delete(0, tk.END)

    # ================= 경품 탭 =================
    def create_prize_tab(self):
        init_prize_file()

        frame = ttk.LabelFrame(self.tab_prize, text="등록된 경품")
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.prize_list = tk.Listbox(frame, height=10)
        self.prize_list.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_prize_list()

    def refresh_prize_list(self):
        self.prize_list.delete(0, tk.END)
        for name, qty in get_prizes():
            self.prize_list.insert(tk.END, f"{name} (남은 수량: {qty})")

    # ================= 추첨 탭 =================
    def create_draw_tab(self):
        frame = ttk.LabelFrame(self.tab_draw, text="경품 추첨")
        frame.pack(padx=20, pady=30, fill="x")

        ttk.Label(frame, text="경품 선택").pack(pady=5)

        self.prize_var = tk.StringVar()
        self.prize_combo = ttk.Combobox(
            frame,
            textvariable=self.prize_var,
            state="readonly",
            width=30
        )
        self.prize_combo.pack(pady=5)

        ttk.Button(
            frame,
            text="🎲 추첨 시작",
            width=30,
            command=self.draw
        ).pack(pady=20)

        self.refresh_draw_prizes()

    def refresh_draw_prizes(self):
        prizes = get_prizes()
        available = [p[0] for p in prizes if p[1] > 0]
        self.prize_combo["values"] = available
        if available:
            self.prize_combo.current(0)

    def draw(self):
        prize = self.prize_var.get()
        if not prize:
            messagebox.showwarning("경고", "경품을 선택하세요.")
            return

        candidates = get_candidate_names()
        if not candidates:
            messagebox.showinfo("알림", "추첨 가능한 인원이 없습니다.")
            return

        result = draw_with_prize(prize)

        if result == "NO_PRIZE":
            messagebox.showinfo("알림", "경품 수량이 없습니다.")
            return

        # 🎬 전체화면 연출
        screen = DrawScreen(
            self.root,
            candidates=candidates,
            final_winner=result["name"]
        )
        screen.start_animation()

        self.refresh_prize_list()
        self.refresh_draw_prizes()

    def run(self):
        self.root.mainloop()
