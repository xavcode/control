import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import config


def show_destinos(frame):
    for widget in frame.winfo_children():
        widget.grid_forget()

    def print_destinos():
        # Connect to the SQLite database
        conn = sqlite3.connect(config.db_path)
        # Execute the query to fetch the destinations
        query = "SELECT * FROM destinos"
        df = pd.read_sql_query(query, conn)
        # Insert the data into the table
        for index, row in df.iterrows():
            table.insert("", "end", text="", values=tuple(row))  # type: ignore
        conn.close()
    
    frame_destinos = ttk.LabelFrame(frame, text="Destinos") 
    frame_destinos.grid(row=0, column=0, pady=10, padx=30, sticky="")

    frame_table_destinos = ttk.Frame(frame_destinos)
    frame_table_destinos.grid(row=0, column=0, pady=10, padx=20,  sticky="")
    
    # Create a treeview widget to display the destinations
    table = ttk.Treeview(frame_table_destinos, columns=("id_destino", "destino", "valor_1", "valor_2", "valor_3",), show="headings", height=25, selectmode="browse")
    table.grid(row=1, column=0, sticky='nswe', padx=10, pady=10)
    table.column("#0", width=0, stretch=False, anchor="center")
    table.column("id_destino", width=50, stretch=False, anchor="center")
    table.column("destino", width=180, stretch=False, anchor="center")
    table.column("valor_1", width=80, stretch=False, anchor="center")
    table.column("valor_2", width=80, stretch=False, anchor="center")
    table.column("valor_3", width=80, stretch=False, anchor="center")

    table.heading("id_destino", text="ID")
    table.heading("destino", text="Destino")
    table.heading("valor_1", text="Valor 1")
    table.heading("valor_2", text="Valor 2")
    table.heading("valor_3", text="Valor 3")
    
    scrollbar = ttk.Scrollbar(frame_table_destinos, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=1, column=2, sticky="ns")

    print_destinos()
    
    frame_form_add_destinos = ttk.LabelFrame(frame_destinos, text="Agregar Destinos")
    frame_form_add_destinos.grid(row=0, column=1, pady=10, padx=20, sticky="nwe")
    
    # Create labels and entry widgets for adding destinations and their values
    label_destino = ttk.Label(frame_form_add_destinos, text="Destino:")
    label_destino.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_destino = ttk.Entry(frame_form_add_destinos)
    entry_destino.grid(row=0, column=1, padx=10, pady=5)

    label_valor_1 = ttk.Label(frame_form_add_destinos, text="Valor 1:")
    label_valor_1.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_valor_1 = ttk.Entry(frame_form_add_destinos)
    entry_valor_1.grid(row=1, column=1, padx=10, pady=5)

    label_valor_2 = ttk.Label(frame_form_add_destinos, text="Valor 2:")
    label_valor_2.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_valor_2 = ttk.Entry(frame_form_add_destinos)
    entry_valor_2.grid(row=2, column=1, padx=10, pady=5)

    label_valor_3 = ttk.Label(frame_form_add_destinos, text="Valor 3:")
    label_valor_3.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_valor_3 = ttk.Entry(frame_form_add_destinos)
    entry_valor_3.grid(row=3, column=1, padx=10, pady=5)

    # Create a button to add the destination
    def add_destino():
        # Get the values from the entry widgets
        destino = entry_destino.get()
        valor_1 = entry_valor_1.get()
        valor_2 = entry_valor_2.get()
        valor_3 = entry_valor_3.get()
        
        # Connect to the SQLite database
        conn = sqlite3.connect(config.db_path)
        # Execute the query to insert the new destination
        query = f"INSERT INTO destinos (destino, valor_1, valor_2, valor_3) VALUES ('{destino}', '{valor_1}', '{valor_2}', '{valor_3}')"
        conn.execute(query)
        conn.commit()
        conn.close()
        
        # Clear the entry widgets
        entry_destino.delete(0, tk.END)
        entry_valor_1.delete(0, tk.END)
        entry_valor_2.delete(0, tk.END)
        entry_valor_3.delete(0, tk.END)
        
        # Refresh the table to display the new destination
        print_destinos()

    button_add_destino = ttk.Button(frame_form_add_destinos, text="Add Destino", command=add_destino)
    button_add_destino.grid(row=4, columnspan=2, padx=10, pady=10, sticky="we")

    btn_aceptar = ttk.Button(frame_destinos, text="Aceptar" )
    btn_aceptar.grid(row=4, column=0, padx=10, pady=10, sticky="")