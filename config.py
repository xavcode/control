from datetime import datetime
import os
import sqlite3
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
        remesas_path = parser.get('paths', 'remesas_path')
        facturas_path = parser.get('paths', 'facturas_path')
        return {'db_path': db_path, 'pueblos_path': pueblos_path, 'tumaco_path': tumaco_path, 'remesas_path': remesas_path, 'facturas_path': facturas_path}
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
        #save the config file
        with open('config.ini', 'w') as config_file:
            parser.write(config_file)
        
        messagebox.showinfo("", "Configuración guardada exitosamente")
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
    
    for widget in frame.winfo_children():
        widget.grid_forget()

    frame_config = ttk.LabelFrame(frame, text='Configuraciones',width=1366, height=768 )
    frame_config.grid(row=0, column=0, )
    frame_config.grid_propagate(False)
    frame_config.grid_columnconfigure(0, weight=1)
    frame_config.grid_rowconfigure(0, weight=1)
    frame_config.grid_columnconfigure(1, weight=1)
    
    ##****-------------------PATHS------------------------****##
    
    frame_paths = ttk.LabelFrame(frame_config, text='Rutas'  )
    frame_paths.grid(row=0, column=0, padx=20, sticky='nswe')
    
    # create a label for the btn config
    label = ttk.Label(frame_paths, text="Seleccionar Base de Datos", font=("Arial", 18))
    label.grid(row=0, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

    entry_db = ttk.Entry(frame_paths) 
    entry_db.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=5 )
    entry_db.insert('end', config['db_path']) # type: ignore
    
    #clean the entry before insert the new path
    btn_db = ttk.Button(frame_paths, text="Seleccionar", command=lambda: select_db()) # type: ignore
    btn_db.grid(row=1, column=2,  sticky="w", padx=5, pady=5)
    
    #****-------------------------------------------------****#
    
    separator = ttk.Separator(frame_paths, orient='horizontal')
    separator.grid(row=3, column=0, columnspan=2, padx=5, sticky="ew", pady=10)    
    
    label_tumaco = ttk.Label(frame_paths, text="Tumaco", font=("Arial", 18))
    label_tumaco.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")
    
    entry_tumaco = ttk.Entry(frame_paths)
    entry_tumaco.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=20, pady=5)
    entry_tumaco.insert('end', config['tumaco_path']) # type: ignore
    
    btn_tumaco = ttk.Button(frame_paths, text="Seleccionar", command=lambda: save_tumaco_file()) # type: ignore
    btn_tumaco.grid(row=5, column=2,  sticky="w", padx=5, pady=5)
    
    #****-------------------------------------------------****#
    
    separator2 = ttk.Separator(frame_paths, orient='horizontal')
    separator2.grid(row=7, column=0, columnspan=2, sticky="ew", pady=15)
    
    label_pueblos = ttk.Label(frame_paths, text="Pueblos", font=("Arial", 18))
    label_pueblos.grid(row=8, column=0, columnspan=2, pady=10, sticky="nsew")
    
    entry_pueblos = ttk.Entry(frame_paths)
    entry_pueblos.grid(row=9, column=0, columnspan=2, sticky="nsew", padx=20, pady=5)
    entry_pueblos.insert('end', config['pueblos_path']) # type: ignore
    
    btn_pueblos = ttk.Button(frame_paths, text="Seleccionar", command=lambda: save_pueblos_file()) # type: ignore
    btn_pueblos.grid(row=9, column=2,  sticky="w", padx=5, pady=5)
    
    label_remesas = ttk.Label(frame_paths, text="Remesas", font=("Arial", 18))
    label_remesas.grid(row=10, column=0, columnspan=2, pady=10, sticky="nsew")
    
    entry_remesas = ttk.Entry(frame_paths)
    entry_remesas.grid(row=11, column=0, columnspan=2, sticky="nsew", padx=20, pady=5)
    entry_remesas.insert('end', config['remesas_path']) # type: ignore
    
    btn_remesas = ttk.Button(frame_paths, text="Seleccionar", command=lambda: save_remesas_path()) # type: ignore
    btn_remesas.grid(row=11, column=2,  sticky="w", padx=5, pady=5)
    
    label_facturas = ttk.Label(frame_paths, text="Facturas", font=("Arial", 18))
    label_facturas.grid(row=12, column=0, columnspan=2, pady=10, sticky="nsew")
    
    entry_facturas = ttk.Entry(frame_paths)
    entry_facturas.grid(row=13, column=0, columnspan=2, sticky="nsew", padx=20, pady=5)
    entry_facturas.insert('end', config['facturas_path']) # type: ignore   
    
    btn_facturas = ttk.Button(frame_paths, text="Seleccionar", command=lambda: save_facturas_path()) # type: ignore
    btn_facturas.grid(row=13, column=2,  sticky="w", padx=5, pady=5)
    
   
    ##****-------------------PATHS------------------------****##
  
    
    ##****-------------------BACKUP------------------------****##
    
    frame_backup = ttk.LabelFrame(frame_config, text='Backup'  )
    frame_backup.grid(row=0, column=1, padx=20, sticky='nswe')
    
    ttk.Label(frame_backup, text="Crear copia de seguridad", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, padx=5, pady=10)
    # entry_db_backup = ttk.Entry(frame_backup)
    # entry_db_backup.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=5 )
    # entry_db_backup.insert('end', config['db_path']) # type: ignore
    
    btn_db_backup = ttk.Button(frame_backup, text="Crear copia", command=lambda: save_backup() ) # type: ignore
    btn_db_backup.grid(row=1, column=0,  sticky="w", padx=5, pady=5)
    
     ##****-------------------BACKUP------------------------****##
    
    frame_btn_save = ttk.Frame(frame_config,)
    frame_btn_save.grid(row=1, column=0, columnspan=2, pady=20, sticky='nsew')
    frame_btn_save.grid_columnconfigure(0, weight=1)
    
    btn_save_changes = ttk.Button(frame_btn_save, text="Guardar Cambios", command=lambda: save_config())
    btn_save_changes.grid(row=0, column=0, sticky="s")


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