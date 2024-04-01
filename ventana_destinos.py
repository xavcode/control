import sqlite3
import tkinter as tk
from tkinter import ttk
import config

# global destino
# destino = ''

# def select_destino():
    
    
    
get_destinos_db()

# def on_text_changed(event):
#     current_text = entry_var.get().lower()
#     listbox.delete(0, tk.END)
#     for item in options:
#         if current_text in item.lower():
#             listbox.insert(tk.END, item)

# def on_item_selected(event):
#     index = listbox.curselection()
#     if index:
#         selected_item = listbox.get(index)
#         entry_var.set(selected_item)
#         global destino
#         destino = selected_item
#         # print(destino)``
  
    
#     options = get_destinos_db()
    
root = tk.Tk( )
root.title("Autocompletado con Tkinter")
root.geometry("250x400")
root.grid_columnconfigure(0, weight=1)




listbox_frame = ttk.Frame(root)
listbox_frame.grid(row=1, column=0, pady=10, sticky="we")
listbox_frame.grid_columnconfigure(0, weight=1)



destinos = (get_destinos_db())
    
entry_var = tk.StringVar()
entry = ttk.Combobox(listbox_frame, textvariable=entry_var, width=25, values=destinos)
entry.grid(row=0, column=0, columnspan=2, pady=10, sticky="")
entry.bind("<KeyRelease>",)






#     listbox = tk.Listbox(listbox_frame, width=25, height=15, selectmode=tk.SINGLE)
#     listbox.grid(row=1, column=0, columnspan=2, sticky="")
#     listbox.bind("<<ListboxSelect>>", on_item_selected)
#     # listbox.bind("<Double-Button-1>", lambda event: on_item_selected(event))    


#     scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=listbox.yview)
#     scrollbar.grid(row=1, column=1, sticky="ns")
#     listbox.config(yscrollcommand=scrollbar.set)
    
#     btn_aceptar = ttk.Button(root, text='Aceptar', command=lambda: root.destroy())
#     btn_aceptar.grid(row=2, column=0, pady=10)
    


root.mainloop()


    

# destin = select_destino()
# print(destin)


