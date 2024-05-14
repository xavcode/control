import os
import sys
import tkinter as tk
from tkinter import messagebox, filedialog,ttk
from configparser import ConfigParser

# Función para cargar la configuración desde el archivo INI
def load_config():
    try:    
        filepath = r'D:\javier\proyectos\PYTHON\control_intermodal\control\config.ini'   
        if  not os.path.exists(filepath):
            messagebox.showerror(
                "", f"No se encontró el archivo de configuración{filepath} "
            )
            return
        
        parser = ConfigParser()
        parser.read(filepath)
        db_path = parser.get('paths', 'db_path')
        pueblos_path = parser.get('paths', 'pueblos_path')
        tumaco_path = parser.get('paths', 'tumaco_path')
        return {'db_path': db_path, 'pueblos_path': pueblos_path, 'tumaco_path': tumaco_path}
    except Exception as e:
        messagebox.showerror(
            "", f"Error al cargar la configuración: {e}"
        )
        return {}
    # print(db_path, pueblos_path, tumaco_path, 'config')
    # return {'db_path': db_path, 'pueblos_path': pueblos_path, 'tumaco_path': tumaco_path}

config = load_config()
def show_config(frame):
    def save_config():
        parser = ConfigParser()
        parser.read('config.ini')
        parser.set('paths', 'db_path', entry_db.get())
        parser.set('paths', 'pueblos_path', entry_pueblos.get())
        parser.set('paths', 'tumaco_path', entry_tumaco.get())
        #save the config file
        with open('config.ini', 'w') as config_file:
            parser.write(config_file)
        # os.execl(sys.executable, sys.executable, *sys.argv)

    # Función para seleccionar la base de datos
    def select_db():
        global config
        file_path = filedialog.askopenfilename(filetypes=[("Archivo de base de datos", "*.db")])  
        if file_path:
            entry_db.delete(0, 'end')
            entry_db.insert('end', file_path)
    
    def save_tumaco_file():
        global config
        file_path = filedialog.askopenfilename(filetypes=[("", "*.xlsx;*.xls;*.xlsm")])
        if file_path:
            entry_tumaco.delete(0, 'end')
            entry_tumaco.insert('end', file_path)
    
    def save_pueblos_file():
        global config
        file_path = filedialog.askopenfilename(filetypes=[("", "*.xlsx;*.xls;*.xlsm")])
        if file_path:
            entry_pueblos.delete(0, 'end')
            entry_pueblos.insert('end', file_path)
            
    # create main frame for anexos
    for widget in frame.winfo_children():
        widget.grid_forget()
   
    frame_config = ttk.Frame(frame, width=1200, height=600,  )
    frame_config.grid(row=0, column=0, pady=10, padx=10)
    frame_config.grid_propagate(False)

    # create a label for the btn config
    label = ttk.Label(frame_config, text="Seleccionar Base de Datos", font=("Arial", 18))
    label.grid(row=0, column=0, columnspan=2, pady=10)

    entry_db = ttk.Entry(frame_config) 
    entry_db.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5 )
    entry_db.insert('end', config['db_path']) # type: ignore
    
    #clean the entry before insert the new path
    btn_db = ttk.Button(frame_config, text="Seleccionar", command=lambda: select_db()) # type: ignore
    btn_db.grid(row=1, column=2,  sticky="w", padx=5, pady=5)
    
    #****-------------------------------------------------****#
    
    separator = ttk.Separator(frame_config, orient='horizontal')
    separator.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)    
    
    label_tumaco = ttk.Label(frame_config, text="Tumaco", font=("Arial", 18))
    label_tumaco.grid(row=4, column=0, columnspan=2, pady=10)
    
    entry_tumaco = ttk.Entry(frame_config)
    entry_tumaco.grid(row=5, column=0, columnspan=2, sticky="we", padx=5, pady=5)
    entry_tumaco.insert('end', config['tumaco_path']) # type: ignore
    
    btn_tumaco = ttk.Button(frame_config, text="Seleccionar", command=lambda: save_tumaco_file()) # type: ignore
    btn_tumaco.grid(row=5, column=2,  sticky="w", padx=5, pady=5)
    
    
    #****-------------------------------------------------****#
    
    separator2 = ttk.Separator(frame_config, orient='horizontal')
    separator2.grid(row=7, column=0, columnspan=2, sticky="ew", pady=15)
    
    label_pueblos = ttk.Label(frame_config, text="Pueblos", font=("Arial", 18))
    label_pueblos.grid(row=8, column=0, columnspan=2, pady=10)
    
    entry_pueblos = ttk.Entry(frame_config)
    entry_pueblos.grid(row=9, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
    entry_pueblos.insert('end', config['pueblos_path']) # type: ignore
    
    btn_pueblos = ttk.Button(frame_config, text="Seleccionar", command=lambda: save_pueblos_file()) # type: ignore
    btn_pueblos.grid(row=9, column=2,  sticky="w", padx=5, pady=5)
    
    btn_save_changes = ttk.Button(frame, text="Guardar Cambios", command=lambda: save_config())
    btn_save_changes.grid(row=10, column=0, columnspan=2, pady=20)
    
    return frame_config


#Consecutives
    # label_consecutives = ttk.Label(frame_config, text="Consecutivos", font=("Arial", 18))
    # label_consecutives.grid(row=4, column=0, pady=10)
    
    # label_letter = tk.Label(frame_config, text="Letras", font=("Arial", 10))
    # label_letter.grid(row=5, column=0, sticky="w", padx=5, pady=5)
    # letters_consecutives = ttk.Entry(frame_config)
    # letters_consecutives.grid(row=6, column=0, sticky="w", padx=5, pady=5)
    # letters_consecutives.insert('end', 'RTP-24')
    
    # label_numbers = ttk.Label(frame_config, text="Numeros", font=("Arial", 10))
    # label_numbers.grid(row=5, column=1, sticky="w", padx=5, pady=5)
    # numbers_consecutives = ttk.Entry(frame_config)
    # numbers_consecutives.grid(row=6, column=1, sticky="w", padx=5, pady=5)
    # numbers_consecutives.insert('end', '0001')