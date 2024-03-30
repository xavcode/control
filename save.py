import tkinter as tk
from tkinter import ttk

def on_text_changed(event):
    current_text = entry_var.get().lower()
    listbox.delete(0, tk.END)
    for item in options:
        if current_text in item.lower():
            listbox.insert(tk.END, item)

def on_item_selected(event):
    index = listbox.curselection()
    if index:
        selected_item = listbox.get(index)
        entry_var.set(selected_item)

root = tk.Tk()
root.title("Autocompletado con Tkinter")

options = ["Manzana", "Banana", "Cereza", "Uva", "Pera", "Piña", "Mango", "Fresa", "Sandía", "Melón"]

entry_var = tk.StringVar()
entry = ttk.Entry(root, textvariable=entry_var)
entry.pack(pady=10)
entry.bind("<KeyRelease>", on_text_changed)

listbox_frame = ttk.Frame(root)
listbox_frame.pack(fill=tk.BOTH, expand=True)

listbox = tk.Listbox(listbox_frame)
listbox.pack(fill=tk.BOTH, expand=True)
listbox.bind("<<ListboxSelect>>", on_item_selected)

scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)

root.mainloop()
