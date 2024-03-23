import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3

import config

def show_remesas(frame):
    for widget in frame.winfo_children():
        widget.grid_forget()
        
    def calc_total():
      total_unidades = 0
      total_kilos = 0
      total_valor = 0
      total_cobro = 0
      total_volumen = 0
      total_ingreso = 0
      total_utilidad = 0
      total_rentabilidad =0.0
            
      
      for item in table.get_children():
        unidades = int(table.item(item, "values")[1])
        kilos = int(table.item(item, "values")[2])
        valor = int(table.item(item, "values")[7])
        cobro =int(table.item(item, "values")[3])
        valor = int(table.item(item, "values")[7])
        gasto_operativo = int(entry_gasto_operativo.get())
        # total_ingreso = int(table.item(item, "values")[6])  # mismo valor que envio.
        if gasto_operativo==0:
            gasto_operativo = 1
        
        total_unidades += unidades
        total_kilos += kilos
        total_valor += valor        
        total_cobro += cobro
        total_volumen += int(table.item(item, "values")[3])
        total_utilidad += (total_valor - total_valor)
        total_rentabilidad =+ (total_valor / gasto_operativo)
        # total_ingreso += total_ingreso
        
        
      entry_total_uds.delete(0,tk.END)
      entry_total_uds.insert(0, str(total_unidades))

      entry_total_kg.delete(0,tk.END)
      entry_total_kg.insert(0, str(total_kilos))

      entry_flete_coord_rtp.delete(0,tk.END)
      entry_flete_coord_rtp.insert(0, str(total_valor))
      
      # Actualiza los valores en los Entry respectivos
      entry_total_uds.delete(0,tk.END)
      entry_total_uds.insert(0, str(total_unidades))

      entry_total_kg.delete(0,tk.END)
      entry_total_kg.insert(0, str(total_kilos))
      
      entry_total_volumen.delete(0,tk.END)
      entry_total_volumen.insert(0, str(total_volumen))
      
      entry_cobro_total.delete(0,tk.END)
      entry_cobro_total.insert(0, str(total_cobro))
      
      entry_ingreso_operativo_total.delete(0,tk.END)
      entry_ingreso_operativo_total.insert(0, str(total_valor))
      
      entry_gasto_operativo.delete(0,tk.END)
      entry_gasto_operativo.insert(0, str(0))
      
      entry_utilidad.delete(0,tk.END)
      entry_utilidad.insert(0, str(total_utilidad))
      
      entry_rentabilidad.delete(0,tk.END)
      entry_rentabilidad.insert(0, str(total_rentabilidad))
    def clean_fields_guia():
        entry_guia.delete(0, tk.END)
        entry_unidades.delete(0, tk.END)
        entry_peso.delete(0, tk.END)
        entry_volumen.delete(0, tk.END)
        entry_destino.delete(0, tk.END)
        entry_fecha_asignacion.delete(0, tk.END)
        entry_cliente.delete(0, tk.END)
        entry_valor.delete(0, tk.END)
        entry_balance_cobro.delete(0, tk.END)
        calc_total()                
    def add_guia_to_remesa(number):
        data = [
            entry_guia.get(),
            int(entry_unidades.get()),
            int(entry_peso.get()),
            int(entry_volumen.get()),
            entry_destino.get(),
            entry_fecha_asignacion.get(),
            entry_cliente.get(),
            int(entry_valor.get()),
            int(entry_balance_cobro.get())
        ]
        table.insert("", "end", values=data)
        calc_total()        
        clean_fields_guia()
        
        return data  
    def delete_row():
        selected_item = table.selection()
        if selected_item:
            table.delete(*selected_item)  # Convert the tuple to a string using the * operator
        calc_total()
    def get_info_guia(number):
        clean_fields_guia()
        connection = sqlite3.connect(config.db_path)
        query = f"SELECT guias.numero_guia, guias.unidades, guias.peso_Kg, guias.volumen_m3, guias.destino, guias.fecha_de_asignacion, guias.destinatario, destinos.valor_destino_1,  (guias.balance_RCE + guias.balance_FCE) AS balance_cobro  FROM guias JOIN destinos ON destinos.destino = guias.destino WHERE guias.numero_guia = {number};"
        result = connection.execute(query)
        data = result.fetchall()
        for row in data:   
            entry_guia.insert(0, row[0])   
            entry_unidades.insert(0, row[1])
            entry_peso.insert(0, row[2])
            entry_volumen.insert(0, row[3])
            entry_destino.insert(0, row[4])
            entry_fecha_asignacion.insert(0, row[5])
            entry_cliente.insert(0, row[6])
            entry_valor.insert(0, row[7])
            entry_balance_cobro.insert(0, row[8])       
        connection.close()
        print(entry_fecha.get())
    def calc_utilidad():
        
        total_ingreso = int(entry_ingreso_operativo_total.get())
        total_gasto = int(entry_gasto_operativo.get())
        total_utilidad = total_ingreso - total_gasto
        if total_utilidad < 1:
            total_utilidad = 0
        entry_utilidad.delete(0, tk.END)
        entry_utilidad.insert(0, str(total_utilidad))
    def calc_rentabilidad():
        rentabilidad = 0.0
        total_utilidad = entry_utilidad.get()                
        if total_utilidad == 0 or total_utilidad == None:
            total_utilidad = 1
        else: total_utilidad = int(total_utilidad)
        print(total_utilidad)
        
            
            
        total_ingreso = int(entry_ingreso_operativo_total.get())
        rentabilidad = float((total_utilidad / total_ingreso)*100).__round__(2)
        entry_rentabilidad.delete(0, tk.END)
        entry_rentabilidad.insert(0, str(rentabilidad))
    def calc_gans():               
        calc_utilidad()
        calc_rentabilidad()
    
        
    tabs_remesas = ttk.Notebook(frame,)
    tabs_remesas.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")
    
    tabs_remesas.grid_rowconfigure(0, weight=1)

    frame_remesas = ttk.Frame(frame )
    frame_remesas.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nswe")
    frame_remesas.grid_columnconfigure(0, weight=1)
    
    
    frame_add_remesa = LabelFrame(frame_remesas, text="Agregar Remesa" )
    frame_add_remesa.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
    frame_add_remesa.grid_columnconfigure(0, weight=1)
    

    frame_form_remesa = LabelFrame(frame_add_remesa, text="Datos de la Remesa" )
    frame_form_remesa.grid(row=1, column=0, padx=(10,10), pady=10, sticky="we")

    tk.Label(frame_form_remesa, text="Remesa: (RTP)").grid(  row=1, column=0, sticky="w", padx=10 )
    entry_id_remesa = ttk.Entry(frame_form_remesa)
    entry_id_remesa.grid(row=1, column=1, padx=5, pady=5)
    entry_id_remesa.insert(0, "RTP-24-")

    tk.Label(frame_form_remesa, text="Manifiesto:").grid( row=1, column=2, sticky="w", padx=10  )
    entry_manifiesto = ttk.Entry(frame_form_remesa)
    entry_manifiesto.grid(row=1, column=3, padx=5, pady=5)

    ttk.Label(frame_form_remesa, text="Conductor:").grid( row=1, column=4, sticky="w", padx=10)
    entry_conductor = ttk.Entry(frame_form_remesa)
    entry_conductor.grid(row=1, column=5, padx=5, pady=5)

    ttk.Label(frame_form_remesa, text="Fecha:").grid( row=1, column=6, sticky="w", padx=10 )
    entry_fecha = DateEntry(frame_form_remesa, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
    entry_fecha.grid(row=1, column=7, padx=5, pady=5, ipadx=15)

    ttk.Label(frame_form_remesa, text="Total Unidades:").grid(row=2, column=0, sticky="w", padx=10    )
    entry_total_uds = ttk.Entry(frame_form_remesa)
    entry_total_uds.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame_form_remesa, text="Total Kg:").grid(row=2, column=2, sticky="w", padx=10)
    entry_total_kg = ttk.Entry(frame_form_remesa)
    entry_total_kg.grid(row=2, column=3, padx=5, pady=5)
    
    ttk.Label(frame_form_remesa, text="Total Vol:").grid(row=2, column=4, sticky="w", padx=10)
    entry_total_volumen = ttk.Entry(frame_form_remesa)
    entry_total_volumen.grid(row=2, column=5, padx=5, pady=5)
    
    ttk.Label(frame_form_remesa, text="Cobro Total:").grid( row=2, column=6, sticky="w", padx=10 )    
    entry_cobro_total = ttk.Entry(frame_form_remesa)
    entry_cobro_total.grid(row=2, column=7, padx=5, pady=5)

    ttk.Label(frame_form_remesa, text="Flete Coord RTP:").grid(row=3, column=0, sticky="w", padx=10)
    entry_flete_coord_rtp = ttk.Entry(frame_form_remesa)
    entry_flete_coord_rtp.grid(row=3, column=1, padx=5, pady=5)
    
    ttk.Label(frame_form_remesa, text="Ingreso Op. Total:").grid(row=3, column=2, sticky="w", padx=10)       
    entry_ingreso_operativo_total = ttk.Entry(frame_form_remesa)
    entry_ingreso_operativo_total.grid(row=3, column=3, padx=5, pady=5)

    ttk.Label(frame_form_remesa, text="Gasto Operativo:").grid( row=3, column=4, sticky="w", padx=10  )
    entry_gasto_operativo = ttk.Entry(frame_form_remesa)
    entry_gasto_operativo.grid(row=3, column=5, padx=5, pady=5)
    entry_gasto_operativo.bind("<KeyRelease>", lambda event: calc_gans())

    ttk.Label(frame_form_remesa, text="Utilidad:").grid( row=3, column=6, sticky="w", padx=10)
    entry_utilidad = ttk.Entry(frame_form_remesa)
    entry_utilidad.grid(row=3, column=7, padx=5, pady=5)

    ttk.Label(frame_form_remesa, text="Rentabilidad:").grid(row=4, column=0, sticky="w", padx=10)
    entry_rentabilidad = ttk.Entry(frame_form_remesa)
    entry_rentabilidad.grid(row=4, column=1, padx=5, pady=5)
    entry_rentabilidad.bind("<KeyRelease>", lambda event: calc_gans())
    
    #* FRAME TREE VIEW
    #? TABLE FOR PREVIEW
    list_camps = ("numero_guia", "unidades", "peso_Kg", "volumen_m3", "destino", "fecha_de_asignacion", "cliente", "valor", "balance_cobro")
    table = ttk.Treeview(frame_add_remesa,columns=list_camps, show="headings", height=16)
    table.grid(row=3, column=0, columnspan=80, sticky="wes", padx=(10,20), pady=10,)

    # Create a vertical scrollbar
    scrollbar = ttk.Scrollbar(frame_add_remesa, orient="vertical", command=table.yview)
    scrollbar.grid(row=3, column=8, sticky="wns", pady=20,) 
    table.configure(yscrollcommand=scrollbar.set)

    table.column("#0", width=0, stretch=False, anchor="center")
    table.column("numero_guia", width=80, stretch=False, anchor="center")
    table.column("unidades", width=60, stretch=False, anchor="center")
    table.column("peso_Kg", width=50, stretch=False, anchor="center")
    table.column("volumen_m3", width=50, stretch=False, anchor="center")
    table.column("destino", width=150, stretch=False, anchor="center")
    table.column("fecha_de_asignacion", width=100, stretch=False, anchor="center")
    table.column("cliente", width=300, stretch=False, anchor="center")
    table.column("valor", width=100, stretch=False, anchor="center")
    table.column("balance_cobro", width=100, stretch=False, anchor="center")
    # Configurar encabezados de columna
    table.heading("numero_guia", text="Guia")
    table.heading("unidades", text="Uds")
    table.heading("peso_Kg", text="Kg")
    table.heading("volumen_m3", text="Vol(M3)")
    table.heading("destino", text="Destino")
    table.heading("fecha_de_asignacion", text="F.Asignacion")
    table.heading("cliente", text="Cliente")
    table.heading("valor", text="Valor")
    table.heading("balance_cobro", text="Bal. de Cobro")


    #   #*  FRAME GUIAS!!!!

    # # Crear y ubicar los widgets para cada elemento de la tabla
    frame_guia = Frame(frame_add_remesa )
    frame_guia.grid(row=2, column=0, columnspan=8, padx=(10, 0), sticky="we")


    ttk.Label(frame_guia, text="Guia:").grid(row=0, column=0, padx=10,)
    entry_guia = ttk.Entry(frame_guia, width=15, justify="center")
    entry_guia.grid(row=1, column=0,)
    ttk.Button(frame_guia, text="🔤", command= lambda: get_info_guia(entry_guia.get()), width=4).grid(row=1, column=1, ipady=1, sticky='w',)

    ttk.Label(frame_guia, text="Uds:").grid(row=0, column=2, padx=5,)
    entry_unidades = ttk.Entry(frame_guia, width=8, justify="center")
    entry_unidades.grid(row=1, column=2, padx=5,)

    ttk.Label(frame_guia, text="Peso (Kg):").grid(row=0, column=3, padx=5,)
    entry_peso = ttk.Entry(frame_guia, width=8, justify="center")
    entry_peso.grid(row=1, column=3, padx=5,)
    
    ttk.Label(frame_guia, text="Volumen (M3):").grid(row=0, column=4, padx=5,)
    entry_volumen = ttk.Entry(frame_guia, width=8, justify="center")
    entry_volumen.grid(row=1, column=4, padx=5,)

    ttk.Label(frame_guia, text="Destino:").grid(row=0, column=5, padx=5,)
    entry_destino = ttk.Entry(frame_guia, width= 20, justify="center")
    entry_destino.grid(row=1, column=5, padx=5,)

    ttk.Label(frame_guia, text="Fecha de Asignacion:").grid(row=0, column=6, padx=5,)
    entry_fecha_asignacion = ttk.Entry(frame_guia, width=12, justify="center")
    entry_fecha_asignacion.grid(row=1, column=6, padx=5,)

    ttk.Label(frame_guia, text="Cliente:").grid(row=0, column=7, padx=5,)
    entry_cliente = ttk.Entry(frame_guia, width=30, justify="center")
    entry_cliente.grid(row=1, column=7, padx=5,)

    ttk.Label(frame_guia, text="Valor:").grid(row=0, column=8, padx=5,)
    entry_valor = ttk.Entry(frame_guia, justify="center")
    entry_valor.grid(row=1, column=8, padx=5,)

    ttk.Label(frame_guia, text="Balance Cobro:").grid(row=0, column=9, padx=5,)
    entry_balance_cobro = ttk.Entry(frame_guia, width=10, justify="center")
    entry_balance_cobro.grid(row=1, column=9, padx=5,)

    ttk.Button(frame_guia, text="✅", width=4, command= lambda: add_guia_to_remesa(entry_guia.get())).grid(row=1, column=10, padx=5, pady=5, )    
    ttk.Button(frame_guia, text="❌", width=4, command= lambda: delete_row()).grid(row=1, column=11, padx=5, pady=5,)

    btn_guardar = ttk.Button(frame_remesas, text="Guardar Remesa")
    btn_guardar.grid(row=4, column=0, sticky='s', padx=10, pady=10)
    
    calc_total()
    tabs_remesas.add(frame_remesas, text="Agregar Remesa")    
        
    
    
    #* FRAME TAB SEARCH REMESA
    
    def list_remesas():
        connection = sqlite3.connect(config.db_path)
        query = f"SELECT id_remesa, manifiesto, conductor, fecha, ingreso_operativo_total, rentabilidad FROM remesas;"
        result = connection.execute(query)
        data = result.fetchall()
        
        for row in data:
            table_list_remesas.insert("", "end", values=row)
             # Set the column headings
            table_list_remesas.heading("id_remesa", text="ID Remesa")
            table_list_remesas.heading("manifiesto", text="Manifiesto")
            table_list_remesas.heading("conductor", text="Conductor")
            table_list_remesas.heading("fecha", text="Fecha")
            table_list_remesas.heading("ingreso_operativo_total", text="Ingreso Operativo Total")
            table_list_remesas.heading("rentabilidad", text="Rentabilidad")
        connection.close()
    def search_remesa(id_remesa):
        
        
        connection = sqlite3.connect(config.db_path)
        query = f"SELECT r.id_remesa, r.manifiesto, r.conductor, d.destino, r.fecha, r.total_kg, r.total_uds, total_vol, r.flete_coord_rtp, r.ingreso_operativo_total, r. gasto_operativo, r.utilidad, r.rentabilidad FROM remesas AS r JOIN destinos  AS d ON d.id_destino = r.destino_id WHERE id_remesa = '{id_remesa}'";       
        result = connection.execute(query)
        data = result.fetchall() 
        connection.close()
    
        entries = [entry_id_remesa, entry_manifiesto, entry_conductor, entry_destino, entry_fecha, entry_total_kg, entry_total_uds, entry_total_volumen, entry_flete_coord_rtp, entry_ingreso_operativo_total, entry_gasto_operativo, entry_utilidad, entry_rentabilidad]
        
        
        def create_entries(data):
            #creamos los entries con los datos de la remesa, para verlos y editarlos en la misma ventana.            
           
            frame_edit_remesa = ttk.Frame(frame_search_remesa)
            frame_edit_remesa.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="")            
            
            ttk.Label(frame_edit_remesa, text="ID Remesa:").grid(row=0, column=0, sticky="w", padx=10)
            entry_id_remesa = ttk.Entry(frame_edit_remesa)
            entry_id_remesa.configure(state="enabled")
            entry_id_remesa.grid(row=0, column=1, padx=5, pady=5)
            entry_id_remesa.insert(0, data[0][0])
            entry_id_remesa.configure(state="disabled")
            
            ttk.Label(frame_edit_remesa, text="Manifiesto:").grid(row=0, column=2, sticky="w", padx=10)
            entry_manifiesto = ttk.Entry(frame_edit_remesa)
            entry_manifiesto.configure(state="enabled")
            entry_manifiesto.grid(row=0, column=3, padx=5, pady=5)
            entry_manifiesto.insert(0, data[0][1])
            entry_manifiesto.configure(state="disabled")
            
            ttk.Label(frame_edit_remesa, text="Conductor:").grid(row=0, column=4, sticky="w", padx=10)
            entry_conductor = ttk.Entry(frame_edit_remesa)
            entry_conductor.configure(state="enabled")
            entry_conductor.grid(row=0, column=5, padx=5, pady=5)
            entry_conductor.insert(0, data[0][2])
            entry_conductor.configure(state="disabled")
            
            ttk.Label(frame_edit_remesa, text="Destino:").grid(row=0, column=6, sticky="w", padx=10)
            entry_destino = ttk.Entry(frame_edit_remesa)
            entry_destino.configure(state="enabled")
            entry_destino.grid(row=0, column=7, padx=5, pady=5)
            entry_destino.insert(0, data[0][3])
            entry_destino.configure(state="disabled")
            
            ttk.Label(frame_edit_remesa, text="Fecha:").grid(row=0, column=8, sticky="w", padx=10)
            entry_fecha = ttk.Entry(frame_edit_remesa)
            entry_fecha.configure(state="enabled")
            entry_fecha.grid(row=0, column=9, padx=5, pady=5)
            entry_fecha.insert(0, data[0][4])
            entry_fecha.configure(state="disabled")
            
            ttk.Label(frame_edit_remesa, text="Total Kg:").grid(row=1, column=0, sticky="w", padx=10)
            entry_total_kg = ttk.Entry(frame_edit_remesa)
            entry_total_kg.configure(state="enabled")
            entry_total_kg.grid(row=1, column=1, padx=5, pady=5)
            entry_total_kg.insert(0, data[0][5])
            entry_total_kg.configure(state="disabled")
            
            ttk.Label(frame_edit_remesa, text="Total Uds:").grid(row=1, column=2, sticky="w", padx=10)
            entry_total_uds = ttk.Entry(frame_edit_remesa)
            entry_total_uds.configure(state="enabled")
            entry_total_uds.grid(row=1, column=3, padx=5, pady=5)
            entry_total_uds.insert(0, data[0][6])
            entry_total_uds.configure(state="disabled")
            
            ttk.Label(frame_edit_remesa, text="Total Volumen:").grid(row=1, column=4, sticky="w", padx=10)
            entry_total_volumen = ttk.Entry(frame_edit_remesa)
            entry_total_volumen.configure(state="enabled")
            entry_total_volumen.grid(row=1, column=5, padx=5, pady=5)
            entry_total_volumen.insert(0, data[0][7])
            entry_total_volumen.configure(state="disabled")

            
            ttk.Label(frame_edit_remesa, text="Flete Coord RTP:").grid(row=1, column=6, sticky="w", padx=10)
            entry_flete_coord_rtp = ttk.Entry(frame_edit_remesa)
            entry_flete_coord_rtp.configure(state="enabled")
            entry_flete_coord_rtp.grid(row=1, column=7, padx=5, pady=5)
            entry_flete_coord_rtp.insert(0, data[0][8])
            entry_flete_coord_rtp.configure(state="disabled")
            
            
            ttk.Label(frame_edit_remesa, text="Ingreso Op. Total:").grid(row=1, column=8, sticky="w", padx=10)
            entry_ingreso_operativo_total = ttk.Entry(frame_edit_remesa)
            entry_ingreso_operativo_total.configure(state="enabled")
            entry_ingreso_operativo_total.grid(row=1, column=9, padx=5, pady=5)
            entry_ingreso_operativo_total.insert(0, data[0][9])
            entry_ingreso_operativo_total.configure(state="disabled")
            
            ttk.Label(frame_edit_remesa, text="Gasto Operativo:").grid(row=2, column=0, sticky="w", padx=10)
            entry_gasto_operativo = ttk.Entry(frame_edit_remesa)
            entry_gasto_operativo.configure(state="enabled")
            entry_gasto_operativo.grid(row=2, column=1, padx=5, pady=5)
            entry_gasto_operativo.insert(0, data[0][10])
            entry_gasto_operativo.configure(state="disabled")
            
            ttk.Label(frame_edit_remesa, text="Utilidad:").grid(row=2, column=2, sticky="w", padx=10)
            entry_utilidad = ttk.Entry(frame_edit_remesa)
            entry_utilidad.configure(state="enabled")
            entry_utilidad.grid(row=2, column=3, padx=5, pady=5)
            entry_utilidad.insert(0, data[0][11])
            entry_utilidad.configure(state="disabled")
            
            ttk.Label(frame_edit_remesa, text="Rentabilidad:").grid(row=2, column=4, sticky="w", padx=10)
            entry_rentabilidad = ttk.Entry(frame_edit_remesa)
            entry_rentabilidad.configure(state="enabled")
            entry_rentabilidad.grid(row=2, column=5, padx=5, pady=5)
            entry_rentabilidad.insert(0,str(data[0][12]))
            entry_rentabilidad.configure(state="disabled")        
            
            def enable_edit_remesa():
                entries = [entry_id_remesa, entry_manifiesto, entry_conductor, entry_destino, entry_fecha, entry_total_kg, entry_total_uds, entry_total_volumen,entry_flete_coord_rtp, entry_ingreso_operativo_total, entry_gasto_operativo, entry_utilidad, entry_rentabilidad]
                
                for entry in entries:
                    entry.configure(state="enabled")
            btn_edit_remesa = ttk.Button(frame_search_single_remesa, text="Editar Remesa", command=lambda: enable_edit_remesa())
            btn_edit_remesa.grid(row=1, column=2, sticky="w", padx=5, pady=5)
                
        if data:            
            create_entries(data)            
            
    def on_double_click(event):
        item = table_list_remesas.focus()
        id_remesa = table_list_remesas.item(item)['values'][0]
        search_remesa(id_remesa)

    
    frame_search_remesa = ttk.Frame(frame,)
    frame_search_remesa.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="wens" )
    frame_search_remesa.grid_columnconfigure(0, weight=1)
    # frame_search_remesa.grid_rowconfigure(0, weight=1)
    
    
    frame_list_remesas = ttk.Frame(frame_search_remesa)
    frame_list_remesas.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="")
    
    table_list_remesas = ttk.Treeview(frame_list_remesas, columns=("id_remesa", "manifiesto", "conductor", "fecha", "ingreso_operativo_total", "rentabilidad"), show="headings", height=10)
    for col in table_list_remesas["columns"]:
        table_list_remesas.column(col, width=200, anchor="center")
    
    table_list_remesas.grid(row=0, column=0, sticky="wes", padx=(10), pady=10,)
    
    table_list_remesas.bind("<Double-1>", on_double_click)
        
    
    frame_search_single_remesa = ttk.Frame(frame_search_remesa)
    frame_search_single_remesa.grid(row=1, column=0, columnspan=1, padx=10, pady=10, sticky="")    
    
    
    entry_search_remesa = ttk.Entry(frame_search_single_remesa)
    entry_search_remesa.grid(row=1, column=1, padx=5, pady=5)    
    
    
    btn_search_remesa = ttk.Button(frame_search_single_remesa, text="Buscar Remesa", command=lambda: search_remesa(entry_search_remesa.get()))
    btn_search_remesa.grid(row=1, column=0, sticky="w", padx=5, pady=5) 
    
    
    
    tabs_remesas.add(frame_search_remesa, text="Buscar Remesa")
    
    list_remesas()

