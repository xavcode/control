import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
from config import load_config

def show_destinos(frame, width, height, ):
    config = load_config()
    db_path = config['db_path']  # type: ignore
    
    # def focus_tab(tab):
    #     tab.select(tab_to_show) 
    
    for widget in frame.winfo_children():
        widget.grid_forget()
    def print_destinos():
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        # Execute the query to fetch the destinations
        query = "SELECT * FROM destinos ORDER BY destino ASC"
        df = pd.read_sql_query(query, conn)
        # Insert the data into the table
        for index, row in df.iterrows():
            treeview_destinos.insert("", "end", text="", values=tuple(row))  # type: ignore
        conn.close()
    def clean_table():
        for i in treeview_destinos.get_children():
            treeview_destinos.delete(i)
    def add_destino():
        # Get the values from the entry widgets
        destino = entry_destino.get().upper()
        valor_1 = entry_valor_destino.get()
        # valor_2 = entry_valor_2.get()
        # valor_3 = entry_valor_3.get()
        
        # Connect to the SQLite database
        connection = sqlite3.connect(db_path)
        # Execute the query to insert the new destination
        query = f"INSERT INTO destinos (destino, valor_destino_1) VALUES ('{destino}', '{valor_1}' )"
        connection.execute(query)
        connection.commit()
        connection.close()
        
        # Clear the entry widgets
        entry_destino.delete(0, tk.END)
        entry_valor_destino.delete(0, tk.END)
        # entry_valor_2.delete(0, tk.END)
        # entry_valor_3.delete(0, tk.END)
        clean_table()
        print_destinos()
    def delete_destino():
        # Get the selected destination
        selected = treeview_destinos.selection()
        destino = treeview_destinos.item(treeview_destinos.focus())["values"][0]
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
        connection = sqlite3.connect(db_path)
        # Execute the query to delete the destination
        query = f"DELETE FROM destinos WHERE destino = ?"
        result = connection.execute(query, (destino,))
        if result.rowcount != 0:
            messagebox.showerror("Error", "Se ha borrado el destino: " + destino)
        connection.commit()
        connection.close()
        clean_table()
        print_destinos()
    def search_destino(destino):
        if not destino:
            messagebox.showerror("Error", "Ingrese un destino para buscar")
            return
        # Connect to the SQLite database
        connection = sqlite3.connect(db_path)
        try:            
            connection = connection.cursor()
            # Execute the query to search the destination
            query = f'''
                        SELECT * 
                        FROM destinos 
                        WHERE destino = ?
                        '''
            result = connection.execute(query, (destino,))
            
            entry_destino.delete(0, tk.END)
            entry_valor_destino.delete(0, tk.END)
            
            for row in result:
                entry_destino.insert(0, row[0])
                entry_valor_destino.insert(0, row[1])
        except:
            messagebox.showerror("Error", "No se ha encontrado el destino")        
        connection.close()
    def update_destino(destino):
        if not destino :
            messagebox.showerror("Error", "Ingrese un destino para actualizar")
            return
        # Get the values from the entry widgets
        destino = entry_destino.get().upper()
        valor_destino = int(entry_valor_destino.get())
        connection = sqlite3.connect(db_path)
        try:
            cursor = connection.cursor()
            query = '''UPDATE destinos
                        SET valor_destino_1 = ?
                        WHERE destino = ?'''
            cursor.execute(query, (valor_destino, destino))
            connection.commit()  
            messagebox.showinfo("Información", "Se ha actualizado el destino")
            clean_table()
            print_destinos()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se ha podido actualizar el destino {str(e)}" )
        connection.close()
 
    parent = ttk.Frame(frame,width=1366, height=768)
    parent.grid(row=0, column=0, sticky="nswe")
    parent.grid_propagate(False)
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)
    
    frame_destinos = ttk.Frame(parent) 
    frame_destinos.grid(row=0, column=0, sticky="")

    frame_table_destinos = ttk.Frame(frame_destinos)
    frame_table_destinos.grid(row=0, column=0,  sticky="")
    
    # Create a treeview widget to display the destinations
    treeview_destinos = ttk.Treeview(frame_table_destinos, columns=("destino", "valor",), show="headings", height=25, selectmode="browse")
    treeview_destinos.grid(row=1, column=0, sticky='nswe', padx=10, )
    
    treeview_destinos.column("destino", width=220, stretch=False, anchor="center")
    treeview_destinos.column("valor", width=120, stretch=False, anchor="center")

    treeview_destinos.heading("destino", text="Destino")
    treeview_destinos.heading("valor", text="Valor ")
    
    treeview_destinos.bind("<ButtonRelease-1>", lambda e: search_destino(treeview_destinos.item(treeview_destinos.focus())["values"][0]))    
    
    scrollbar = ttk.Scrollbar(frame_table_destinos, orient="vertical", command=treeview_destinos.yview)
    treeview_destinos.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=1, column=2, sticky="ns")
    
    frame_form_add_destinos = ttk.Frame(frame_destinos, relief="groove", borderwidth=1)
    frame_form_add_destinos.grid(row=0, column=1, padx=20, sticky="nswe")
    
    # Create labels and entry widgets for adding destinations and their values
    label_destino = ttk.Label(frame_form_add_destinos, text="Destino:") 
    label_destino.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_destino = ttk.Entry(frame_form_add_destinos)
    entry_destino.grid(row=0, column=1, padx=10, pady=5)

    label_valor_destino = ttk.Label(frame_form_add_destinos, text="Valor:")
    label_valor_destino.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_valor_destino = ttk.Entry(frame_form_add_destinos)
    entry_valor_destino.grid(row=1, column=1, padx=10, pady=5)
    
    btn_add_destino = ttk.Button(frame_form_add_destinos, text="Agregar Destino", command=add_destino)
    btn_add_destino.grid(row=4, columnspan=2, padx=10, pady=10, sticky="we")

    btn_delete_destino = ttk.Button(frame_form_add_destinos, text="Borrar Destino", command= lambda: delete_destino())
    btn_delete_destino.grid(row=5, columnspan=2, padx=10, pady=10, sticky="we")
    
    btn_update_destino = ttk.Button(frame_form_add_destinos, text="Actualizar Destino", command= lambda: update_destino(entry_destino.get()))
    btn_update_destino.grid(row=6, columnspan=2, padx=10, pady=10, sticky="we")
    
    btn_aceptar = ttk.Button(frame_destinos, text="Aceptar" )
    btn_aceptar.grid(row=4, column=0, padx=10, pady=10, sticky="")  
    
    print_destinos()
    # focus_tab()