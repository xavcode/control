import os
import tkinter as tk
from tkinter import messagebox, filedialog


global db_path 
db_path = 'D:/intermodal/control/control_intermodal.db'

def select_db():
    file_path = filedialog.askopenfilename(filetypes=[("Archivo de base de datos", "*.db")])
    # file_path = os.path.abspath(file_path)
    db_path = file_path
    return db_path

def save_db_path(path):
    db_path = path
    messagebox.showinfo("Éxito", "Ruta de la base de datos guardada correctamente")


def show_config(frame):
    # create main frame for anexos
    for widget in frame.winfo_children():
        widget.grid_forget()
   
    frame_config = tk.Frame(frame, bd=2, relief="groove", width=1000, height=400)
    frame_config.grid(row=0, column=0, pady=10, padx=10)
    frame_config.grid_propagate(False)

    # create a label for the btn config
    label = tk.Label(frame_config, text="Seleccionar Base de Datos", font=("Arial", 18))
    label.grid(row=0, column=0, columnspan=2, pady=10)

    entry_db = tk.Entry(frame_config) 
    entry_db.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5 )
    entry_db.insert(0, db_path)
    
    #clean the entry before insert the new path
    btn_config = tk.Button(frame_config, text="Seleccionar", command=lambda: [entry_db.delete(0, tk.END), entry_db.insert(0, select_db())])
    btn_config.grid(row=2, column=0, columnspan=1, sticky="nsew", padx=5, pady=5)
    
    btn_save = tk.Button(frame_config, text="Guardar", command=lambda: save_db_path(entry_db.get()))
    btn_save.grid(row=2, column=1, columnspan=1, sticky="nsew", padx=5, pady=5)
    

    return frame_config
