import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sqlite3
import customtkinter as ctk

# Frame para el formulario de remesas
def show_remesas(frame):
  for widget in frame.winfo_children():
      widget.grid_forget()
  # add remesas
  def add_guia_to_remesa(number):
    connection = sqlite3.connect("D:/intermodal/control/control_intermodal.db")    
    query = f"SELECT guias.numero_guia, guias.unidades, guias.peso_Kg, guias.destino, guias.fecha_de_asignacion, guias.destinatario, destinos.valor_destino,  (guias.balance_RCE + guias.balance_FCE) AS balance_cobro  FROM guias JOIN destinos ON destinos.destino = guias.destino WHERE guias.numero_guia = {number};"
    result = connection.execute(query)
    data = result.fetchall()    
    for row in data:      
      table.insert("", "end", values=row)   
    entry_guia.delete(0, tk.END)
    calcular_total()
    connection.close()
    return data  
    
  # delete remesas
  def delete_row():
    selected_item = table.selection()
    if selected_item:
      table.delete(*selected_item)  # Convert the tuple to a string using the * operator
    calcular_total()
      
  def calcular_total():
    total_unidades = 0.0
    total_kilos = 0.0
    total_valor = 0.0
    for item in table.get_children():
      unidades = float(table.item(item, "values")[1])
      kilos = float(table.item(item, "values")[2])
      valor = float(table.item(item, "values")[6])
      total_unidades += unidades
      total_kilos += kilos
      total_valor += valor

    entry_total_uds.delete(0, tk.END)
    entry_total_uds.insert(0, str(total_unidades))

    entry_total_kg.delete(0, tk.END)
    entry_total_kg.insert(0, str(total_kilos))

    entry_flete_coord_rtp.delete(0, tk.END)
    entry_flete_coord_rtp.insert(0, str(total_valor))
    
    # Actualiza los valores en los Entry respectivos
    entry_total_uds.delete(0, tk.END)
    entry_total_uds.insert(0, str(total_unidades))

    entry_total_kg.delete(0, tk.END)
    entry_total_kg.insert(0, str(total_kilos))

  
  # Marco para el formulario de la remesa
  frame_remesas = tk.Frame(frame, width=1000, height=600)
  frame_remesas.grid(row=0, column=0, sticky='news', pady=10) 
  frame_remesas.grid_rowconfigure(0, weight=1)
  frame_remesas.grid_rowconfigure(1, weight=1)
  frame_remesas.grid_columnconfigure(0, weight=1)
  frame_remesas.grid_columnconfigure(2, weight=1)
  frame_remesas.grid_propagate(False)
  
  frame_form_remesa = tk.Frame(frame_remesas, bd=2, relief="groove")
  frame_form_remesa.grid(row=0, column=1,  pady=10, sticky="ns" ) 
  
  frame_search_remesa = tk.Frame(frame_form_remesa, bd=2, relief="groove")
  frame_search_remesa.grid(row=0, column=0, columnspan=2,  pady=10, sticky="e" )
  
  btn_search_remesa = tk.Button(frame_search_remesa, text="Buscar Remesa")
  btn_search_remesa.grid(row=0, column=0, sticky="w")
  entry_search_remesa = tk.Entry(frame_search_remesa)
  entry_search_remesa.grid(row=0, column=1, padx=5, pady=5)
  
  # Crear y ubicar los widgets para el formulario de la remesa
  tk.Label(frame_form_remesa, text="Remesa: (RTP)").grid(row=1, column=0, sticky="w")
  entry_id_remesa = tk.Entry(frame_form_remesa)
  entry_id_remesa.grid(row=1, column=1, padx=5, pady=5)

  tk.Label(frame_form_remesa, text="Manifiesto:").grid(row=2, column=0, sticky="w")
  entry_manifiesto = tk.Entry(frame_form_remesa)
  entry_manifiesto.grid(row=2, column=1, padx=5, pady=5)

  tk.Label(frame_form_remesa, text="Conductor:").grid(row=3, column=0, sticky="w")
  entry_conductor = tk.Entry(frame_form_remesa)
  entry_conductor.grid(row=3, column=1, padx=5, pady=5)

  tk.Label(frame_form_remesa, text="Fecha:").grid(row=4, column=0, sticky="w")
  entry_fecha = tk.Entry(frame_form_remesa)
  entry_fecha.grid(row=4, column=1, padx=5, pady=5)

  tk.Label(frame_form_remesa, text="Total Kg:").grid(row=5, column=0, sticky="w")
  entry_total_kg = tk.Entry(frame_form_remesa)
  entry_total_kg.grid(row=5, column=1, padx=5, pady=5)

  tk.Label(frame_form_remesa, text="Total Unidades:").grid(row=6, column=0, sticky="w")
  entry_total_uds = tk.Entry(frame_form_remesa)
  entry_total_uds.grid(row=6, column=1, padx=5, pady=5)

  tk.Label(frame_form_remesa, text="Flete Coord RTP:").grid(row=7, column=0, sticky="w")
  entry_flete_coord_rtp = tk.Entry(frame_form_remesa)
  entry_flete_coord_rtp.grid(row=7, column=1, padx=5, pady=5)

  tk.Label(frame_form_remesa, text="Ingreso Op. Total:").grid(row=8, column=0, sticky="w")
  entry_ingreso_operativo_total = tk.Entry(frame_form_remesa)
  entry_ingreso_operativo_total.grid(row=8, column=1, padx=5, pady=5)

  tk.Label(frame_form_remesa, text="Gasto Operativo:").grid(row=9, column=0, sticky="w")
  entry_gasto_operativo = tk.Entry(frame_form_remesa)
  entry_gasto_operativo.grid(row=9, column=1, padx=5, pady=5)

  tk.Label(frame_form_remesa, text="Utilidad:").grid(row=10, column=0, sticky="w")
  entry_utilidad = tk.Entry(frame_form_remesa)
  entry_utilidad.grid(row=10, column=1, padx=5, pady=5)

  tk.Label(frame_form_remesa, text="Rentabilidad:").grid(row=11, column=0, sticky="w")
  entry_rentabilidad = tk.Entry(frame_form_remesa)
  entry_rentabilidad.grid(row=11, column=1, padx=5, pady=5)

  # Crear y ubicar la tabla
  frame_table = tk.Frame(frame_remesas, bd=2, relief="groove")
  frame_table.grid(row=0, column=3, columnspan=4, sticky='ns', padx=10, pady=10)
  
  frame_add_guia = tk.Frame(frame_table)
  frame_add_guia.grid(row=0, column=0, sticky="nwe", padx=10)

  # Crear y ubicar los widgets para agregar guías a la remesa
  tk.Label(frame_add_guia, text="Ingrese Guía:").grid(row=0, column=0, pady=10, sticky="nw")
  entry_guia = tk.Entry(frame_add_guia)
  entry_guia.grid(row=0, column=0, sticky='n', padx=85, pady=14)
  entry_guia.bind("<Return>", lambda event: btn_agregar_guia.invoke())
  btn_agregar_guia = tk.Button(frame_add_guia, text="Agregar Guía", command=lambda: add_guia_to_remesa(entry_guia.get()))
  btn_agregar_guia.grid(row=0, column=0, sticky="e", pady=10)
  btn_borrar = tk.Button(frame_add_guia, text="Borrar Registro", command=delete_row)
  btn_borrar.grid(row=0, column=1, sticky='n', pady=10)
  # Vincula la tecla "Delete" a la función de borrado de fila

  table = ttk.Treeview(frame_table,columns=("numero_guia", "unidades", "peso_Kg", "destino", "fecha_de_asignacion", "cliente", "valor", "balance_cobro"), show="headings")
  table.column("#0", width=0, stretch=False, anchor="center")
  table.column("numero_guia", width=80, stretch=False, anchor="center")
  table.column("unidades", width=60, stretch=False, anchor="center")
  table.column("peso_Kg", width=50, stretch=False, anchor="center")
  table.column("destino", width=150, stretch=False, anchor="center")
  table.column("fecha_de_asignacion", width=100, stretch=False, anchor="center")
  table.column("cliente", width=300, stretch=False, anchor="center")
  table.column("valor", width=50, stretch=False, anchor="center")
  table.column("balance_cobro", width=50, stretch=False, anchor="center")


 # Configurar encabezados de columna
  table.heading("numero_guia", text="Guia")
  table.heading("unidades", text="Uds")
  table.heading("peso_Kg", text="Kg")
  table.heading("destino", text="Destino")
  table.heading("fecha_de_asignacion", text="F.Recepcion")
  table.heading("cliente", text="Cliente")
  table.heading("valor", text="Valor")
  table.heading("balance_cobro", text="Cobro")

  # Agregar barra de desplazamiento vertical a la tabla
  scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=table.yview)
  table.configure(yscrollcommand=scrollbar.set)
  scrollbar.grid(row=1, column=12, sticky="ns")

  # Ubicar la tabla en el frame
  table.grid(row=1, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")
  frame_table.grid_columnconfigure(0, minsize=400)
  frame_table.grid_rowconfigure(1, weight=1)
  

 
        
  #delete row in the table
  table.bind("<Delete>", lambda event: delete_row())
  
  # button to save remesa
  btn_guardar = tk.Button(frame_remesas, text="Guardar Remesa")
  btn_guardar.grid(row=1, column=1, sticky='wes', padx=10, pady=10)
  return frame_remesas