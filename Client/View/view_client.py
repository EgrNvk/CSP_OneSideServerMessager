import tkinter as tk

class ClientView:
    def __init__(self, title="Client"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("700x700")

        self.history = tk.Text(self.root, wrap="word", state="disabled")
        self.history.pack(fill="both", expand=True, padx=10, pady=10)


    def add_line(self, text):
        self.history.configure(state="normal")
        self.history.insert("end", text + "\n")
        self.history.configure(state="disabled")
        self.history.see("end")

    def start(self):
        self.root.mainloop()