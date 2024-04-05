import os
import tkinter as tk
from tkinter import messagebox, filedialog,ttk


global db_path 

db_path = 'D:/intermodal/control_intermodal - copia.db'
# db_path = 'D:/intermodal/control/prueba_borrar.db'


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
   
    frame_config = ttk.LabelFrame(frame, width=1200, height=600, text="Configuración")
    frame_config.grid(row=0, column=0, pady=10, padx=10)
    frame_config.grid_propagate(False)

    # create a label for the btn config
    label = ttk.Label(frame_config, text="Seleccionar Base de Datos", font=("Arial", 18))
    label.grid(row=0, column=0, columnspan=2, pady=10)

    entry_db = ttk.Entry(frame_config) 
    entry_db.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5 )
    entry_db.insert(0, db_path)
    
    #clean the entry before insert the new path
    btn_config = ttk.Button(frame_config, text="Seleccionar", command=lambda: [entry_db.delete(0, tk.END), entry_db.insert(0, select_db())])
    btn_config.grid(row=2, column=0, columnspan=1, sticky="nsew", padx=5, pady=5)
    
    btn_save = ttk.Button(frame_config, text="Guardar", command=lambda: save_db_path(entry_db.get()))
    btn_save.grid(row=2, column=1, columnspan=1, sticky="nsew", padx=5, pady=5)
    
    #****-------------------------------------------------****#
    separator = ttk.Separator(frame_config, orient='horizontal')
    separator.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)    
        
    #Consecutives
    label_consecutives = ttk.Label(frame_config, text="Consecutivos", font=("Arial", 18))
    label_consecutives.grid(row=4, column=0, pady=10)
    
    label_letter = tk.Label(frame_config, text="Letras", font=("Arial", 10))
    label_letter.grid(row=5, column=0, sticky="w", padx=5, pady=5)
    letters_consecutives = ttk.Entry(frame_config)
    letters_consecutives.grid(row=6, column=0, sticky="w", padx=5, pady=5)
    letters_consecutives.insert('end', 'RTP-24')
    
    label_numbers = ttk.Label(frame_config, text="Numeros", font=("Arial", 10))
    label_numbers.grid(row=5, column=1, sticky="w", padx=5, pady=5)
    numbers_consecutives = ttk.Entry(frame_config)
    numbers_consecutives.grid(row=6, column=1, sticky="w", padx=5, pady=5)
    numbers_consecutives.insert('end', '0001')
    
    separator2 = ttk.Separator(frame_config, orient='horizontal')
    separator2.grid(row=7, column=0, columnspan=2, sticky="ew", pady=15)
    
    btn_save_changes = ttk.Button(frame_config, text="Guardar Cambios")
    btn_save_changes.grid(row=8, column=0, columnspan=2, pady=10)
    
    
    

    return frame_config
