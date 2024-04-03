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
  
    def clean_table():
        for i in table.get_children():
            table.delete(i)
    
    def add_destino():
        # Get the values from the entry widgets
        destino = entry_destino.get().upper()
        valor_1 = entry_valor_1.get()
        # valor_2 = entry_valor_2.get()
        # valor_3 = entry_valor_3.get()
        
        # Connect to the SQLite database
        connection = sqlite3.connect(config.db_path)
        # Execute the query to insert the new destination
        query = f"INSERT INTO destinos (destino, valor_destino_1) VALUES ('{destino}', '{valor_1}' )"
        connection.execute(query)
        connection.commit()
        connection.close()
        
        # Clear the entry widgets
        entry_destino.delete(0, tk.END)
        entry_valor_1.delete(0, tk.END)
        # entry_valor_2.delete(0, tk.END)
        # entry_valor_3.delete(0, tk.END)
        clean_table()
        print_destinos()
    
    def delete_destino():
        # Get the selected destination
        selected = table.selection()
        destino = table.item(table.focus())["values"][0]
        if not selected:
            messagebox.showerror("Error", "Seleccione un destino para borrar")
            return
        # Get the destination name
        # Ask for confirmation before deleting the destination
        confirmed = messagebox.askyesno("Confirmar", "¿Estás seguro de borrar el destino seleccionado?")
        if not confirmed:
            return
        
        # print(destino)
        # Connect to the SQLite database
        connection = sqlite3.connect(config.db_path)
        # Execute the query to delete the destination
        query = f"DELETE FROM destinos WHERE destino = ?"
        result = connection.execute(query, (destino,))
        if result.rowcount != 0:
            messagebox.showerror("Error", "Se ha borrado el destino : " + destino)
        connection.commit()
        connection.close()
        clean_table()
        print_destinos()

    frame_destinos = ttk.LabelFrame(frame, text="Destinos") 
    frame_destinos.grid(row=0, column=0, pady=10, padx=30, sticky="wne")

    frame_table_destinos = ttk.Frame(frame_destinos)
    frame_table_destinos.grid(row=0, column=0, pady=10, padx=20,  sticky="")
    
    # Create a treeview widget to display the destinations
    table = ttk.Treeview(frame_table_destinos, columns=("destino", "valor",), show="headings", height=25, selectmode="browse")
    table.grid(row=1, column=0, sticky='nswe', padx=10, pady=10)
    
    table.column("destino", width=220, stretch=False, anchor="center")
    table.column("valor", width=120, stretch=False, anchor="center")
    # table.column("valor_2", width=80, stretch=False, anchor="center")
    # table.column("valor_3", width=80, stretch=False, anchor="center")

    table.heading("destino", text="Destino")
    table.heading("valor", text="Valor ")
    # table.heading("valor_2", text="Valor 2")
    # table.heading("valor_3", text="Valor 3")
    
    scrollbar = ttk.Scrollbar(frame_table_destinos, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=1, column=2, sticky="ns")
    
    frame_form_add_destinos = ttk.LabelFrame(frame_destinos, text="Agregar Destinos")
    frame_form_add_destinos.grid(row=0, column=1, pady=10, padx=20, sticky="nwe")
    
    # Create labels and entry widgets for adding destinations and their values
    label_destino = ttk.Label(frame_form_add_destinos, text="Destino:")
    label_destino.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_destino = ttk.Entry(frame_form_add_destinos)
    entry_destino.grid(row=0, column=1, padx=10, pady=5)

    label_valor_1 = ttk.Label(frame_form_add_destinos, text="Valor:")
    label_valor_1.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_valor_1 = ttk.Entry(frame_form_add_destinos)
    entry_valor_1.grid(row=1, column=1, padx=10, pady=5)

    # label_valor_2 = ttk.Label(frame_form_add_destinos, text="Valor 2:")
    # label_valor_2.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    # entry_valor_2 = ttk.Entry(frame_form_add_destinos)
    # entry_valor_2.grid(row=2, column=1, padx=10, pady=5)

    # label_valor_3 = ttk.Label(frame_form_add_destinos, text="Valor 3:")
    # label_valor_3.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    # entry_valor_3 = ttk.Entry(frame_form_add_destinos)
    # entry_valor_3.grid(row=3, column=1, padx=10, pady=5)

    # Create a button to add the destination
    
        
        # Refresh the table to display the new destination

    
    
    button_add_destino = ttk.Button(frame_form_add_destinos, text="Add Destino", command=add_destino)
    button_add_destino.grid(row=4, columnspan=2, padx=10, pady=10, sticky="we")
    
    button_delete_destino = ttk.Button(frame_form_add_destinos, text="Delete Destino", command= lambda: delete_destino())
    button_delete_destino.grid(row=5, columnspan=2, padx=10, pady=10, sticky="we")
    

    btn_aceptar = ttk.Button(frame_destinos, text="Aceptar" )
    btn_aceptar.grid(row=4, column=0, padx=10, pady=10, sticky="")  
    
    print_destinos()