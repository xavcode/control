from datetime import datetime
import os
import sqlite3
from tkinter import messagebox, filedialog
from configparser import ConfigParser
import ttkbootstrap as ttk

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
        remesas_path = parser.get('paths', 'remesas_path')
        facturas_path = parser.get('paths', 'facturas_path')
        consecutives_remesas = parser.get('consecutives', 'remesas')
        consecutives_manifiestos = parser.get('consecutives', 'manifiestos')
        theme = parser.get('theme', 'actual_theme')
        return {'db_path': db_path, 'pueblos_path': pueblos_path, 'tumaco_path': tumaco_path, 'remesas_path': remesas_path, 'facturas_path': facturas_path, 'theme': theme, 'consecutives': {'remesas': consecutives_remesas, 'manifiestos': consecutives_manifiestos}}
    
    except Exception as e:
        messagebox.showerror(
            "", f"Error al cargar la configuración: {e}"
        )
        return {}

config = load_config()
def show_config(frame, width, height):
    def save_config():
        parser = ConfigParser()
        parser.read('config.ini')
        parser.set('paths', 'db_path', entry_db.get())
        parser.set('paths', 'pueblos_path', entry_pueblos.get())
        parser.set('paths', 'tumaco_path', entry_tumaco.get())
        parser.set('paths', 'remesas_path', entry_remesas.get())
        parser.set('paths', 'facturas_path', entry_facturas.get())
        parser.set('consecutives', 'remesas', entry_remesas_consecutives.get())
        parser.set('consecutives', 'manifiestos', entry_manifiestos_consecutives.get())
        parser.set('theme', 'actual_theme')
        with open('config.ini', 'w') as config_file:
            parser.write(config_file)
        
        messagebox.showinfo("", "Configuración guardada exitosamente")
        load_config()
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
    def save_backup():
        global config
        current_date = datetime.now().strftime("%Y-%m-%d")
        file_path = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("SQLite Database", "*.db")],
            title="Guardar respaldo de la base de datos",
            initialfile=f"backup_Intermodal_{current_date}.db"
            )
        if not file_path:
            return
        try:
            source_conn = sqlite3.connect(config['db_path']) # type: ignore
            backup_conn = sqlite3.connect(file_path)
            with backup_conn:
                source_conn.backup(backup_conn, pages=1, progress=None)
            source_conn.close()
            backup_conn.close()
            messagebox.showinfo("Éxito", "Backup realizado exitosamente en: {}".format(file_path))
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al realizar el backup: {e}")
    def save_remesas_path():
        global config
        folder_path = filedialog.askdirectory()
        if folder_path:
            entry_remesas.delete(0, 'end')
            entry_remesas.insert('end', folder_path)
            config['remesas_path'] = folder_path # type: ignore
    def save_facturas_path():
        global config
        folder_path = filedialog.askdirectory()
        if folder_path:
            entry_facturas.delete(0, 'end')
            entry_facturas.insert('end', folder_path)
            config['facturas_path'] = folder_path # type: ignore
    def save_consecutives():
        global config
        remesas = entry_remesas.get()
        manifiestos = entry_manifiestos_consecutives.get()
        if not remesas or not manifiestos:
            messagebox.showerror("Error", "Debe ingresar los nombres de los remesas y manifiestos")
            return
        config['consecutives'] = {'remesas': remesas, 'manifiestos': manifiestos} # type: ignore
        messagebox.showinfo("", "Consecutivos guardados exitosamente")
    for widget in frame.winfo_children():
        widget.grid_forget()
    
    frame_config = ttk.LabelFrame(frame, text='Configuraciones',width=width, height=height )
    frame_config.grid(row=0, column=0, padx=10, )
    frame_config.grid_propagate(False)
    frame_config.grid_columnconfigure(0, weight=2)
    frame_config.grid_columnconfigure(1, weight=2)
    
    frame_config.grid_rowconfigure(0, weight=1)
    
    ##****-------------------PATHS------------------------****##
    
    frame_paths = ttk.LabelFrame(frame_config, text='Rutas'  )
    frame_paths.grid(row=0, column=0,  sticky='nswe', padx=10)
    
    # create a label for the btn config
    label = ttk.Label(frame_paths, text="Seleccionar Base de Datos", font=("Arial", 18))
    label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    entry_db = ttk.Entry(frame_paths) 
    entry_db.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=5 )
    entry_db.insert('end', config['db_path']) # type: ignore
    
    #clean the entry before insert the new path
    btn_db = ttk.Button(frame_paths, text="Seleccionar", command=lambda: select_db()) # type: ignore
    btn_db.grid(row=2, column=1,  sticky="e", padx=10, pady=5)
    
    # #****-------------------------------------------------****#
    
    separator = ttk.Separator(frame_paths, orient='horizontal')
    separator.grid(row=3, column=0, columnspan=3, padx=5, sticky="ew", pady=10)    
    
    ttk.Label(frame_paths, text="Tumaco", font=("Arial", 18)).grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")
    entry_tumaco = ttk.Entry(frame_paths)
    entry_tumaco.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
    entry_tumaco.insert('end', config['tumaco_path']) # type: ignore
    
    btn_tumaco = ttk.Button(frame_paths, text="Seleccionar", command=lambda: save_tumaco_file()) # type: ignore
    btn_tumaco.grid(row=6, column=1,  sticky="e", padx=10, pady=5)
    
    #****-------------------------------------------------****#
    
    
    ttk.Label(frame_paths, text="Pueblos", font=("Arial", 18)).grid(row=8, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")
    entry_pueblos = ttk.Entry(frame_paths)
    entry_pueblos.grid(row=9, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
    entry_pueblos.insert('end', config['pueblos_path']) # type: ignore

    btn_pueblos = ttk.Button(frame_paths, text="Seleccionar", command=lambda: save_pueblos_file()) # type: ignore
    btn_pueblos.grid(row=10, column=1,  sticky="e", padx=10, pady=5)

    #****-------------------------------------------------****#

    ttk.Label(frame_paths, text="Remesas", font=("Arial", 18)).grid(row=11, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")
    entry_remesas = ttk.Entry(frame_paths)
    entry_remesas.grid(row=12, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
    entry_remesas.insert('end', config['remesas_path']) # type: ignore

    btn_remesas = ttk.Button(frame_paths, text="Seleccionar", command=lambda: save_remesas_path()) # type: ignore
    btn_remesas.grid(row=13, column=1,  sticky="e", padx=10, pady=5)

    #****-------------------------------------------------****#

    ttk.Label(frame_paths, text="Facturas", font=("Arial", 18)).grid(row=14, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")
    entry_facturas = ttk.Entry(frame_paths)
    entry_facturas.grid(row=15, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
    entry_facturas.insert('end', config['facturas_path']) # type: ignore   

    btn_facturas = ttk.Button(frame_paths, text="Seleccionar", command=lambda: save_facturas_path()) # type: ignore
    btn_facturas.grid(row=16, column=1,  sticky="e", padx=10, pady=5)
   
    ##****-------------------PATHS------------------------****##
    
    ##****-------------------BACKUP------------------------****##
    
    frame_others = ttk.Frame(frame_config)
    frame_others.grid(row=0, column=1, sticky='nswe', )
    frame_others.grid_columnconfigure(0, weight=1)
    frame_others.grid_rowconfigure(0, weight=1)
    frame_others.grid_rowconfigure(1, weight=1)
    
    frame_backup = ttk.LabelFrame(frame_others, text='Backup')
    frame_backup.grid(row=0, column=0, sticky='nswe')    

    ttk.Label(frame_backup, text="Crear copia de seguridad", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, padx=10, pady=10)    
    btn_db_backup = ttk.Button(frame_backup, text="Crear copia", command=lambda: save_backup() ) 
    btn_db_backup.grid(row=1, column=0,  sticky="w", padx=10, pady=5)
    
     ##****-------------------BACKUP------------------------****##

     ##****-------------------CONSECUTIVES------------------------****##

    frame_consecutives = ttk.LabelFrame(frame_others, text='Consecutivos'  )
    frame_consecutives.grid(row=1, column=0, sticky='nwse')
   
    ttk.Label(frame_consecutives, text="Consecutivos", font=("Arial", 18)).grid(row=0, column=0, pady=10, padx=10, sticky="w")

    ttk.Label(frame_consecutives, text="REMESAS", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_remesas_consecutives = ttk.Entry(frame_consecutives)
    entry_remesas_consecutives.grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_remesas_consecutives.insert('end', f"{config['consecutives']['remesas']}") # type: ignore

    ttk.Label(frame_consecutives, text="MANIFIESTOS", font=("Arial", 10)).grid(row=1, column=1, sticky="w", padx=10, pady=5)
    entry_manifiestos_consecutives = ttk.Entry(frame_consecutives)
    entry_manifiestos_consecutives.grid(row=2, column=1, sticky="w", padx=10, pady=5)
    entry_manifiestos_consecutives.insert('end', f"{config['consecutives']['manifiestos']}") # type: ignore

    ##****-------------------CONSECUTIVES------------------------****##
    
    frame_btn_save = ttk.Frame(frame_config,)
    frame_btn_save.grid(row=1, column=0, columnspan=2, pady=10, sticky='')
    frame_btn_save.grid_columnconfigure(0, weight=1)
    
    btn_save_changes = ttk.Button(frame_btn_save, text="Guardar Cambios", command=lambda: save_config())
    btn_save_changes.grid(row=0, column=0, sticky="wes")

