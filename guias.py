import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import sqlite3
from sqlite3 import IntegrityError


# Read the CSV file into a DataFrame
def read_xls_file():
    # Read the Excel file into a DataFrame
    file_path = filedialog.askopenfilename(filetypes=[("Archivo excel", "*.xlsx")])
    df_excel = pd.read_excel(file_path)
    df = df_excel.copy()

    # Rest of the code remains the same
    df.drop(df.index[0], axis=0, inplace=True)
    df.iloc[:, 1] = df.iloc[:, 1].str[3:]
    df.head()

    # Create a connection to the database
    connection = sqlite3.connect("D:/intermodal/control/control_intermodal.db")
    # Insert the DataFrame records into the 'test' table in the database
    df.columns = [
        "estado",
        "numero_guia",
        "fecha_de_asignacion",
        "remitente",
        "destino",
        "destinatario",
        "direccion_de_entrega",
        "fecha_maxima_de_entrega",
        "unidades",
        "peso_Kg",
        "volumen_m3",
        "valor_declarado_(COP)",
        "fecha_entrega_reexpedidor",
        "hora_entrega_reexpedidor",
        "ultima_causal",
        "fecha_ultima_causal",
        "balance_RCE",
        "balance_FCE",
        "fd",
        "rd",
        "ruta",
        "telefono",
    ]
    for i in range(len(df)):
        try:
            df.iloc[i:i+1].to_sql("guias", connection, if_exists='append', index=False, method='multi')
        except IntegrityError:
            pass #or any other action   
        
    messagebox.showinfo("", "Guias importadas con éxito")
    connection.close()

# define ui guias module
def show_guias(frame):
    for widget in frame.winfo_children():
        widget.grid_forget()

    frame_guias = tk.Frame(frame, bd=2, relief="groove", width=1000, height=600)
    frame_guias.grid(row=0, column=0, padx=0, pady=10, )
    frame_guias.grid_propagate(False)
    
    frame_guias.grid_columnconfigure(0, weight=1)
    frame_guias.grid_columnconfigure(1, weight=1)

    frame_buscar_guias = tk.Frame(frame_guias, bd=2, relief="groove")
    frame_buscar_guias.grid( row=0, column=0, sticky='we', padx=10, pady=10)
    
    tk.Label(frame_buscar_guias, text="Buscar Guías", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=10 )
    tk.Label(frame_buscar_guias, text="Ingrese Guía:").grid(row=1, column=0, sticky="w")    
    entry_search_guia = tk.Entry(frame_buscar_guias)
    entry_search_guia.grid(row=1, column=1, sticky="w", padx=10, pady=10)
    entry_search_guia.bind("<Return>", lambda event: search_button.invoke())
    search_button = tk.Button(frame_buscar_guias,text="Buscar",command=lambda: search_guias(frame_guias, entry_search_guia.get()) )
    search_button.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)


    frame_agregar_guias = tk.Frame(frame_guias, bd=2, relief="groove")
    frame_agregar_guias.grid(row=0, column=1, sticky='we',  padx=10, pady=10)
    
    tk.Label(frame_agregar_guias, text="Agregar Guías", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=10 )
    tk.Label(frame_agregar_guias, text="Ingrese Guía:").grid(row=1, column=0, sticky="w")
    entry_add_guia = tk.Entry(frame_agregar_guias)
    entry_add_guia.grid(row=1, column=1, sticky="w", padx=10, pady=10)    
    add_button = tk.Button(frame_agregar_guias, text="Agregar")
    add_button.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    frame_import_all = tk.Frame(frame_guias, bd=2, relief="groove", background="red")
    frame_import_all.grid(row=0, column=2, columnspan=2, sticky='s', padx=10, pady=10)
    import_button = tk.Button(frame_guias, text="Importar", command=read_xls_file)
    import_button.grid(row=1, column=1, sticky="e", padx=10, pady=5)

    return frame_guias

def search_guias(frame, number):
    
    connection = sqlite3.connect("D:/intermodal/control/control_intermodal.db")
    # Execute a SQL query to search for the guia number
    query = f"SELECT estado, numero_guia, fecha_de_asignacion, remitente, destino, destinatario, direccion_de_entrega, unidades, peso_Kg, volumen_m3, ultima_causal, fecha_ultima_causal, telefono FROM guias WHERE numero_guia = '{number}'"
    result = connection.execute(query)

    # Process the query result
    for row in result:
        # Create a new frame for each row
        frame_row = tk.Frame(frame, bd=2, relief="groove")
        frame_row.grid(row=4, column=0, sticky="we", columnspan=2, padx=10, pady=10)

        # Display the data in labels
        tk.Label(frame_row, text="Estado:").grid(row=0, column=0, sticky="w")
        tk.Label(frame_row, text=row[0]).grid(row=0, column=1, sticky="w")

        tk.Label(frame_row, text="Número de Guía:").grid(row=1, column=0, sticky="w")
        tk.Label(frame_row, text=row[1]).grid(row=1, column=1, sticky="w")

        tk.Label(frame_row, text="Fecha de Asignación:").grid(row=2, column=0, sticky="w")
        tk.Label(frame_row, text=row[2]).grid(row=2, column=1, sticky="w")

        tk.Label(frame_row, text="Remitente:").grid(row=3, column=0, sticky="w")
        tk.Label(frame_row, text=row[3]).grid(row=3, column=1, sticky="w")

        tk.Label(frame_row, text="Destino:").grid(row=4, column=0, sticky="w")
        tk.Label(frame_row, text=row[4]).grid(row=4, column=1, sticky="w")

        tk.Label(frame_row, text="Destinatario:").grid(row=5, column=0, sticky="w")
        tk.Label(frame_row, text=row[5]).grid(row=5, column=1, sticky="w")

        tk.Label(frame_row, text="Dirección de Entrega:").grid(row=6, column=0, sticky="w")
        tk.Label(frame_row, text=row[6]).grid(row=6, column=1, sticky="w")

        tk.Label(frame_row, text="Unidades:").grid(row=7, column=0, sticky="w")
        tk.Label(frame_row, text=row[7]).grid(row=7, column=1, sticky="w")

        tk.Label(frame_row, text="Peso (Kg):").grid(row=8, column=0, sticky="w")
        tk.Label(frame_row, text=row[8]).grid(row=8, column=1, sticky="w")

        tk.Label(frame_row, text="Volumen (m3):").grid(row=9, column=0, sticky="w")
        tk.Label(frame_row, text=row[9]).grid(row=9, column=1, sticky="w")

        tk.Label(frame_row, text="Última Causal:").grid(row=11, column=0, sticky="w")
        tk.Label(frame_row, text=row[10]).grid(row=11, column=1, sticky="w")

        tk.Label(frame_row, text="Fecha Última Causal:").grid(row=12, column=0, sticky="w")
        tk.Label(frame_row, text=row[11]).grid(row=12, column=1, sticky="w")

        tk.Label(frame_row, text="Teléfono:").grid(row=13, column=0, sticky="w")
        tk.Label(frame_row, text=row[12]).grid(row=13, column=1, sticky="w")

        # Continue displaying the rest of the data...

    # Close the database connection
    connection.close()