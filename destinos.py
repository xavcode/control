
import tkinter as tk
from tkinter import  messagebox
import sqlite3
import ttkbootstrap as ttk

from config import load_config

def show_destinos(frame, width, height, ):
    config = load_config()
    db_path = config['db_path']  # type: ignore
    destino_selected = None # used for update the sasme name of destination
    
    for widget in frame.winfo_children():
        widget.grid_forget()
    def get_destinos():
        try:
            conn = sqlite3.connect(db_path)
            query = "SELECT * FROM destinos ORDER BY destino ASC"
            result = conn.execute(query)
            data = result.fetchall()
            if not data :
                messagebox.showerror("", "no se encontraron destinos")
                return
            conn.close()
            clean_table()
            for row in data:                   
                row_list = list(row)
                row_list[1] = "{:,}".format(int(row_list[1]))
                row_list[2] = "{:,}".format(int(row_list[2]))
                row_list[3] = "{:,}".format(int(row_list[3]))
                row_list[4] = "{:,}".format(int(row_list[4]))                                
                treeview_destinos.insert("", "end", text="", values=row_list) 
            conn.close()            
        except Exception as e:
            messagebox.showerror("", f"Error al obtener los destinos: {str(e)}")
        finally:
            conn.close()
    def clean_table():
        for i in treeview_destinos.get_children():
            treeview_destinos.delete(i)
    def clear_entries():
        entry_destino.delete(0, tk.END)
        entry_valor_destino_1.delete(0, tk.END)
        entry_valor_destino_2.delete(0, tk.END)
        entry_valor_destino_3.delete(0, tk.END)
        entry_extra.delete(0, tk.END)
    def add_destino():
        # Get the values from the entry widgets
        destino = entry_destino.get().upper()
        valor_1 = entry_valor_destino_1.get()
        valor_2 = entry_valor_destino_2.get()
        valor_3 = entry_valor_destino_3.get()
        valor_extra = entry_extra.get()
        
        if not destino:
            messagebox.showerror("", "El destino no puede estar vacío")
            return
        if not valor_1:
            messagebox.showerror("", "Ingrese minimo una tarifa ")
            return
        if not valor_1.isdigit() or int(valor_1) < 0:
            messagebox.showerror("", "Ingrese un valor valido")
            return
        if (not valor_2.isdigit() or int(valor_2) < 0 )and not valor_2 == "":
            messagebox.showerror("", "Ingrese un valor 2 valido")
            return
        if (not valor_3.isdigit() or int(valor_3) < 0) and not valor_2 == "":
            messagebox.showerror("", "Ingrese un valor 3 valido")
            return
        if valor_2 == '':
            valor_2 = 0
        if valor_3 == '':
            valor_3 = 0
        if valor_extra == '':
            valor_extra = 0
        
        try:
            connection = sqlite3.connect(db_path)            
            query = f"INSERT INTO destinos (destino, valor_destino_1, valor_destino_2, valor_destino_3, extra) VALUES ('{destino}', {int(valor_1)}, {int(valor_2)}, {int(valor_3)},{int(valor_extra)})"
            connection.execute(query)
            connection.commit()
            connection.close()
            clear_entries()
            clean_table()
            get_destinos()
        except Exception as e:
            messagebox.showerror("", f"Error al agregar el destino: {str(e)}")
    def delete_destino():
        # Get the selected destination
        selected = treeview_destinos.selection()
        destino = treeview_destinos.item(treeview_destinos.focus())["values"][0]
        if not selected:
            messagebox.showerror("Error", "Seleccione un destino para borrar")
            return
        confirmed = messagebox.askyesno("Confirmar", f"¿Estás seguro de borrar el destino: {destino} ?")
        if not confirmed:
            return
        
        connection = sqlite3.connect(db_path)
        query = "DELETE FROM destinos WHERE destino = ?"
        result = connection.execute(query, (destino,))
        if result.rowcount != 0:
            messagebox.showerror("Error", "Se ha borrado el destino: " + destino)
        connection.commit()
        connection.close()
        clean_table()
        clear_entries()
        get_destinos()
    def search_destino(destino):
        if not destino:
            messagebox.showerror("Error", "Ingrese un destino para buscar")
            return
        global destino_selected
        destino_selected = destino
        try:            
            connection = sqlite3.connect(db_path)
            connection = connection.cursor()
            query = '''
                        SELECT * 
                        FROM destinos 
                        WHERE destino = ?
                        '''
            result = connection.execute(query,(destino,))
            
            list_entries = [entry_destino, entry_valor_destino_1, entry_valor_destino_2, entry_valor_destino_3, entry_extra]
            for i in range(len(list_entries)):
                list_entries[i].delete(0, tk.END)
                        
            for row in result:
                entry_destino.insert(0, row[0])
                entry_valor_destino_1.insert(0, (row[1]))
                entry_valor_destino_2.insert(0, (row[2]))
                entry_valor_destino_3.insert(0, (row[3]))
                entry_extra.insert(0, (row[4]))
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se ha podido buscar el destino {str(e)}" )
            connection.close()
        finally:
            connection.close()
    def update_destino(destino):
        global destino_selected
        if not destino :
            messagebox.showerror("Error", "Ingrese un destino para actualizar")
            return
        # Get the values from the entry widgets
        destino = entry_destino.get().upper()
        valor_destino_2 = entry_valor_destino_2.get()
        valor_destino_3 = entry_valor_destino_3.get()
        valor_extra = entry_extra.get()        

        #Validations

        new_destino = entry_destino.get().upper()
        if not new_destino:
            messagebox.showerror("Error", "Ingrese un destino valido")
            return

        valor_destino_1 = entry_valor_destino_1.get()
        if valor_destino_1 is None:
            messagebox.showerror("Error", "Ingrese al menos una tarifa")
            return
        if not valor_destino_1.isdigit() or int(valor_destino_1) < 0:
            messagebox.showerror("Error", "Ingrese un valor 1 valido")
            return
        
        if valor_destino_2 == '':
            valor_destino_2 = 0
        elif not valor_destino_2.isdigit() or int(valor_destino_2) < 0:
            messagebox.showerror("Error", "Ingrese un valor 2 valido")
            return
        
        if valor_destino_3 == '':
            valor_destino_3 = 0
        elif not valor_destino_3.isdigit() or int(valor_destino_3) < 0: 
            messagebox.showerror("Error", "Ingrese un valor 3 valido")
            return

        if valor_extra == '':
            valor_extra = 0
        elif not valor_extra.isdigit() or int(valor_extra) < 0: 
            messagebox.showerror("Error", "Ingrese un valor extra valido")
            return
        
        #Update query
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            query = ''' 
                        UPDATE destinos
                        SET
                        destino = ?, 
                        valor_destino_1 = ?,
                        valor_destino_2 = ?,
                        valor_destino_3 = ?,
                        extra = ?
                        WHERE destino = ?
                    '''
            cursor.execute(query, (new_destino, valor_destino_1, valor_destino_2, valor_destino_3, valor_extra, destino_selected))
            connection.commit()  
            messagebox.showinfo("Información", f"Se ha actualizado el destino: {destino_selected}")
            clean_table()
            clear_entries()
            get_destinos()
        except sqlite3.Error as e:
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror("Error", "Ya existe el destino")
            else:
                messagebox.showerror("Error", f"No se ha podido actualizar el destino {str(e)}" )
                
        connection.close()
    parent = ttk.Frame(frame,width=width, height=height)
    parent.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")
    parent.grid_propagate(False)
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)
    
    frame_destinos = ttk.Frame(parent) 
    frame_destinos.grid(row=0, column=0, sticky="nswe")
    frame_destinos.grid_columnconfigure(0, weight=1)
    frame_destinos.grid_columnconfigure(1, weight=1)
    frame_destinos.grid_rowconfigure(0, weight=1)
    frame_destinos.grid_rowconfigure(1, weight=0)
    frame_destinos.grid_rowconfigure(2, weight=0)
  
    frame_table_destinos = ttk.Frame(frame_destinos)
    frame_table_destinos.grid(row=0, column=0,  sticky="wesn")
    frame_table_destinos.grid_columnconfigure(0, weight=1)
    frame_table_destinos.grid_rowconfigure(0, weight=1)
    
    # Create a treeview widget to display the destinations
    list_camps = ("Destino", "Valor 1", "Valor 2", "Valor 3", "Extra")
    treeview_destinos = ttk.Treeview(frame_table_destinos, columns=list_camps, show="headings", height=25, selectmode="browse")
    treeview_destinos.grid(row=0, column=0, sticky='nse', padx=10, )
    
    for col in list_camps:
        treeview_destinos.heading(col, text=col)
        treeview_destinos.column(col, width=120, stretch=True, anchor="center")
    treeview_destinos.column("#1", width=300, stretch=True, anchor="center")
    
    treeview_destinos.bind("<ButtonRelease-1>", lambda e: search_destino(treeview_destinos.item(treeview_destinos.focus())["values"][0]))
    
    scrollbar = ttk.Scrollbar(frame_table_destinos, bootstyle= 'primary-round', orient="vertical", command=treeview_destinos.yview) # type: ignore
    treeview_destinos.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=2, sticky="ns")
    
    frame_form_add_destinos = ttk.Frame(frame_destinos, relief="groove", borderwidth=1)
    frame_form_add_destinos.grid(row=0, column=1, padx=10, sticky="nw")
    
    # Create labels and entry widgets for adding destinations and their values
    ttk.Label(frame_form_add_destinos, text="Destino:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_destino = ttk.Entry(frame_form_add_destinos, justify='center')
    entry_destino.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(frame_form_add_destinos, text="Valor 1:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_valor_destino_1 = ttk.Entry(frame_form_add_destinos, justify='center')
    entry_valor_destino_1.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(frame_form_add_destinos, text="Valor 2:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_valor_destino_2 = ttk.Entry(frame_form_add_destinos, justify='center')
    entry_valor_destino_2.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(frame_form_add_destinos, text="Valor 3:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_valor_destino_3 = ttk.Entry(frame_form_add_destinos, justify='center')
    entry_valor_destino_3.grid(row=3, column=1, padx=10, pady=5)

    ttk.Label(frame_form_add_destinos, text="Extra:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    entry_extra = ttk.Entry(frame_form_add_destinos, justify='center')
    entry_extra.grid(row=4, column=1, padx=10, pady=5)
    
    btn_add_destino = ttk.Button(frame_form_add_destinos, text="Agregar Destino", command=add_destino)
    btn_add_destino.grid(row=5, columnspan=2, padx=10, pady=10, sticky="we")

    btn_clear_entries = ttk.Button(frame_form_add_destinos, text="Limpiar", command=lambda:clear_entries())
    btn_clear_entries.grid(row=6, columnspan=2, padx=10, pady=10, sticky="we")
    
    btn_delete_destino = ttk.Button(frame_form_add_destinos, text="Borrar Destino", command=lambda:delete_destino())
    btn_delete_destino.grid(row=7, columnspan=2, padx=10, pady=10, sticky="we")

    btn_update_destino = ttk.Button(frame_form_add_destinos, text="Actualizar Destino", command=lambda: update_destino(entry_destino.get()))
    btn_update_destino.grid(row=8, columnspan=2, padx=10, pady=10, sticky="we") 
    get_destinos()
