import tkinter as tk
import sqlite3

import config
import pandas as pd

from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox,filedialog
from tkcalendar import DateEntry



def _convert_stringval(value):
    if hasattr(value, 'typename'):
        value = str(value)
        try:
            value = int(value)
        except (ValueError, TypeError):
            pass
    return value

ttk._convert_stringval = _convert_stringval # type: ignore


# from ventana_destinos import select_destino

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
        cobro =int(table.item(item, "values")[8])
        # valor = int(table.item(item, "values")[7])
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
        
      entry_total_uds.state(["!readonly"])
      entry_total_uds.delete(0,tk.END)
      entry_total_uds.delete(0,tk.END)
      entry_total_uds.insert(0, str(total_unidades))
      entry_total_uds.state(["readonly"])
  
      entry_total_kg.state(["!readonly"])
      entry_total_kg.delete(0,tk.END)
      entry_total_kg.insert(0, str(total_kilos))
      entry_total_kg.state(["readonly"])
  
      entry_flete_coord_rtp.state(["!readonly"])
      entry_flete_coord_rtp.delete(0,tk.END)
      entry_flete_coord_rtp.insert(0, str(total_valor))
      entry_flete_coord_rtp.state(["readonly"])
      
      # Actualiza los valores en los Entry respectivos
      entry_total_uds.state(["!readonly"])
      entry_total_uds.delete(0,tk.END)
      entry_total_uds.insert(0, str(total_unidades))
      entry_total_uds.state(["readonly"])
  
      entry_total_kg.state(["!readonly"])
      entry_total_kg.delete(0,tk.END)
      entry_total_kg.insert(0, str(total_kilos))
      entry_total_kg.state(["readonly"])
      
      entry_total_volumen.state(["!readonly"])
      entry_total_volumen.delete(0,tk.END)
      entry_total_volumen.insert(0, str(total_volumen))
      entry_total_volumen.state(["readonly"])
      
      entry_cobro_total.state(["!readonly"])
      entry_cobro_total.delete(0,tk.END)
      entry_cobro_total.insert(0, str(total_cobro))
      entry_cobro_total.state(["readonly"])
      
      entry_ingreso_operativo_total.state(["!readonly"])
      entry_ingreso_operativo_total.delete(0,tk.END)
      entry_ingreso_operativo_total.insert(0, str(total_valor))
      entry_ingreso_operativo_total.state(["readonly"])
      
      
      entry_gasto_operativo.delete(0,tk.END)
      entry_gasto_operativo.insert(0, str(0))
      
      
      entry_utilidad.state(["!readonly"])
      entry_utilidad.delete(0,tk.END)
      entry_utilidad.insert(0, str(total_utilidad))
      entry_utilidad.state(["readonly"])
      
      entry_rentabilidad.state(["!readonly"])
      entry_rentabilidad.delete(0,tk.END)
      entry_rentabilidad.insert(0, str(total_rentabilidad))
      entry_rentabilidad.state(["readonly"])
  
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
    def get_info_guia(id_guia):
        clean_fields_guia()
        connection = sqlite3.connect(config.db_path)
        query = f"SELECT guias.numero_guia, guias.unidades, guias.peso_Kg, guias.volumen_m3, guias.destino, guias.fecha_de_asignacion, guias.destinatario, destinos.valor_destino_1,  (guias.balance_RCE + guias.balance_FCE) AS balance_cobro  FROM guias JOIN destinos ON destinos.destino = guias.destino WHERE guias.numero_guia = '{id_guia}';"
        result = connection.execute(query)
        data = result.fetchall()
        connection.close()
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
    def calc_utilidad():        
        total_ingreso = int(entry_ingreso_operativo_total.get())
        total_gasto = int(entry_gasto_operativo.get())
        total_utilidad = total_ingreso - total_gasto
        if total_utilidad < 1:
            total_utilidad = 0
        entry_utilidad.state(["!readonly"])
        entry_utilidad.delete(0, tk.END)
        entry_utilidad.insert(0, str(total_utilidad))
        entry_utilidad.state(["readonly"])
    def calc_rentabilidad():
        rentabilidad = 0.0
        total_utilidad = entry_utilidad.get()                
        if total_utilidad == 0 or total_utilidad == None:
            total_utilidad = 1
        else: total_utilidad = int(total_utilidad)
        
        
            
        total_ingreso = int(entry_ingreso_operativo_total.get())
        rentabilidad = float((total_utilidad / total_ingreso)*100).__round__(2)
        entry_rentabilidad.state(["!readonly"])
        entry_rentabilidad.delete(0, tk.END)
        entry_rentabilidad.insert(0, str(rentabilidad))
        entry_rentabilidad.state(["readonly"])
    def calc_gans():               
        calc_utilidad()
        calc_rentabilidad()
    def save_remesa():
        id_remesa = entry_id_remesa.get()
        id_manifiesto = entry_manifiesto.get()
        conductor = entry_conductor.get()
        fecha_remesa = entry_fecha.get()
        total_uds = entry_total_uds.get()
        total_kg = entry_total_kg.get()
        total_volumen = entry_total_volumen.get()
        cobro_total = entry_cobro_total.get()
        flete_coord_rtp = entry_flete_coord_rtp.get()
        ingreso_operativo_total = entry_ingreso_operativo_total.get()
        gasto_operativo = entry_gasto_operativo.get()
        utilidad = entry_utilidad.get()
        rentabilidad = entry_rentabilidad.get()
        destino_remesa = cbbx_destino_remesa.get()
        if not destino_remesa:
                messagebox.showerror("", "El campo Destino no puede estar vacío")
                return        
        
        connection = sqlite3.connect(config.db_path)
        query = f"INSERT INTO remesas (id_remesa, manifiesto, conductor, destino, fecha, total_uds, total_kg, total_vol, cobro_total, flete_coord_rtp, ingreso_operativo_total, gasto_operativo, utilidad, rentabilidad) VALUES ('{id_remesa}', '{id_manifiesto}', '{conductor}', '{destino_remesa}', '{fecha_remesa}', '{total_uds}', '{total_kg}', '{total_volumen}', '{cobro_total}', '{flete_coord_rtp}', '{ingreso_operativo_total}', '{gasto_operativo}', '{utilidad}', '{rentabilidad}');"
        
        #create the list for insert guias
        rows_to_insert = []
        for row in table.get_children():
            row_values = table.item(row)["values"]
            rows_to_insert.append(row_values)
      
        #create the query for the insert
        query_remesas = f"INSERT INTO remesas_guias (remesa_id, guia_id ) VALUES "
        
        for i in range(len(rows_to_insert)):
            row = rows_to_insert[i]
            query_remesas += f"('{id_remesa}', '{row[0]}')"
            if i != len(rows_to_insert) - 1:
                query_remesas += ", "
            else:
                query_remesas += ";"
        
        #     #inserting remesa with headers
        #     try:
        #         result = connection.execute(query)
        #         connection.commit()
        #     except Exception as e:
        #         messagebox.showerror("", f"Error al guardar la remesa: {str(e)}")
        
        # #inserting guias to remesa
        try:
            result = connection.execute(query)
            result = connection.execute(query_remesas)
            connection.commit()
            if result:
                messagebox.showinfo("", "Remesa guardada con éxito")
                clean_entries_remesa()
                clean_table_remesas()
                clean_table_guias()
                list_remesas()         
        except Exception as e:
            error_message = str(e)
            if "UNIQUE constraint failed" in error_message:
                messagebox.showerror("", f"Ya existe la remesa: {id_remesa}")
            
            # messagebox.showerror("", f"Error al guardar las guias: {str(e)}")
            
        connection.close()
       
    def delete_remesa(id_remesa):
            try:
                confirmed = messagebox.askyesno("Confirmar", f"Desea borrar la remesa {id_remesa}?")
                if not confirmed:
                    return
                connection = sqlite3.connect(config.db_path)
                cursor = connection.cursor()

                # Primera consulta para eliminar de la tabla remesas_guias
                query_remesas_guias = f"DELETE FROM remesas_guias WHERE remesa_id = '{id_remesa}';"
                
                cursor.execute(query_remesas_guias)

                # Segunda consulta para eliminar de la tabla remesas
                query_remesas = f"DELETE FROM remesas WHERE id_remesa = '{id_remesa}';"
                cursor.execute(query_remesas)

                connection.commit()
                connection.close()

                messagebox.showinfo("", "Remesa eliminada con éxito")
            except sqlite3.Error as e:
                messagebox.showerror("", f"Error al eliminar la remesa: {e}")
            
            clean_table_remesas()
            list_remesas()
    def enable_entries():
        entry_id_remesa.state(["!readonly"])
        entry_manifiesto.state(["!readonly"])
        entry_conductor.state(["!readonly"])
        entry_fecha.state(["!readonly"])
        entry_total_uds.state(["!readonly"])
        entry_total_kg.state(["!readonly"])
        entry_total_volumen.state(["!readonly"])
        entry_cobro_total.state(["!readonly"])
        entry_flete_coord_rtp.state(["!readonly"])
        entry_ingreso_operativo_total.state(["!readonly"])
        entry_gasto_operativo.state(["!readonly"])
        entry_utilidad.state(["!readonly"])
        entry_rentabilidad.state(["!readonly"])  
    def disable_entries():
        entry_total_uds.state(["readonly"])
        entry_total_kg.state(["readonly"])
        entry_total_volumen.state(["readonly"])
        entry_cobro_total.state(["readonly"])
        entry_flete_coord_rtp.state(["readonly"])
        entry_ingreso_operativo_total.state(["readonly"])
        entry_gasto_operativo.state(["readonly"])
        entry_utilidad.state(["readonly"])
        entry_rentabilidad.state(["readonly"])
    def clean_entries_remesa():
        enable_entries()
        
        entry_id_remesa.delete(0, tk.END)   
        entry_manifiesto.delete(0, tk.END)
        entry_conductor.delete(0, tk.END)
        entry_fecha.delete(0, tk.END)
        entry_total_uds.delete(0, tk.END)        
        entry_total_kg.delete(0, tk.END)
        entry_total_volumen.delete(0, tk.END)
        entry_cobro_total.delete(0, tk.END)
        entry_flete_coord_rtp.delete(0, tk.END)
        entry_ingreso_operativo_total.delete(0, tk.END)
        entry_gasto_operativo.delete(0, tk.END)
        entry_utilidad.delete(0, tk.END)
        entry_rentabilidad.delete(0, tk.END)
        cbbx_destino_remesa.set('')      
    def list_remesas():
        connection = sqlite3.connect(config.db_path)
        query = f'''
                    SELECT 
                        remesas.id_remesa, 
                        remesas.manifiesto, 
                        remesas.destino, 
                        remesas.conductor, 
                        remesas.fecha, 
                        remesas.ingreso_operativo_total, 
                        remesas.rentabilidad, 
                        COUNT(remesas_guias.remesa_id) AS total_guias,
                        COUNT(CASE WHEN guias.en_factura <> 'no' THEN 1 END) AS guias_facturadas,
                        COUNT(CASE WHEN guias.en_factura = 'no' THEN 1 END) AS guias_sin_facturar 
                    FROM 
                        remesas
                    LEFT JOIN 
                        remesas_guias ON remesas.id_remesa = remesas_guias.remesa_id
                    LEFT JOIN 
                        guias ON remesas_guias.guia_id = guias.numero_guia
                    GROUP BY 
                        remesas.id_remesa
                    ORDER BY 
                        remesas.id_remesa DESC;
                '''
        
        result = connection.execute(query)
        data = result.fetchall()
        
        for row in data:
             # Set the column headings
            table_list_remesas.heading("id_remesa", text="ID Remesa")
            table_list_remesas.heading("manifiesto", text="Manifiesto")
            table_list_remesas.heading("destino", text="Destino")
            table_list_remesas.heading("conductor", text="Conductor")
            table_list_remesas.heading("fecha", text="Fecha")
            table_list_remesas.heading("ingreso_operativo_total", text="Ing. Op. Total")
            table_list_remesas.heading("rentabilidad", text="Rentabilidad")
            table_list_remesas.heading("total_guias", text="Total Guias")
            table_list_remesas.heading("guias_facturadas", text="G. Facturadas")
            table_list_remesas.heading("guias_sin_facturar", text="G. Pendientes")
            table_list_remesas.insert("", "end", values=row)
        connection.close()  
    def get_destinos_db() :
        connection = sqlite3.connect(config.db_path)
        query = "SELECT destino FROM destinos;"
        result = connection.execute(query)
        data = result.fetchall()
        options = [item[0] for item in data]        
        connection.close()
        return options
    def clean_table_remesas():
            table_list_remesas.delete(*table_list_remesas.get_children())       
    def clean_table_guias():
        table.delete(*table.get_children())
    def import_remesa():
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:           
            # Convierte el DataFrame a string y divídelo por líneas para crear una lista de filas
            df = pd.read_excel(file_path, header=None)
            
            def get_remesa(df):
                clean_entries_remesa()
                # Check if the last row contains the word "Total"
                #if ther is title has a header, is removed
                first_row = df.iloc[0].to_string()
                if 'relacion' in first_row.lower():
                    df= df.drop(df.index[0])

                #get the drivers name
                conductor = df.iloc[0].to_string()
                if 'conductor' in conductor.lower():
                    conductor = str(df.iat[0,0])
                    conductor = conductor.split(':')[1].strip()
                    conductor = conductor.replace("CONDUCTOR", "").strip()

                #get the headers data
                id_remesa = df.iat[0, 5].strip()
                manifiesto = df.iat[0, 7].strip()
                fecha = str(df.iat[1, 8])
                formated_date = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
                formated_date = formated_date.strftime('%d-%m-%Y')

                # delete last row if has total word 
                del_total_row = df.iloc[-1].to_string()
                if 'total' in del_total_row.lower():
                    df = df.drop(df.index[-1])

                df.columns = df.iloc[1]
                df = df.iloc[2:]
                df.rename(columns={df.columns[8]: 'COBRO'},  inplace=True)

                # dated formated with dd/mm/yy format
                df.iloc[:, 5] = pd.to_datetime(df.iloc[:, 5]).dt.strftime('%d-%m-%Y')

                # delet characters in column cobros
                
                df['COBRO'] = df['COBRO'].apply(lambda x: str(x).replace('.', ''))
                df['COBRO'] = df['COBRO'].apply(lambda x: ''.join(c for c in x if c.isdigit()))
                df['COBRO'] = df['COBRO'].apply(lambda x: 0 if not str(x).isdigit() else x)
                df['COBRO'] = pd.to_numeric(df['COBRO'])                
                
                kg_sum = df.iloc[:, 3].sum()
                cobro_sum = df.iloc[:, 8].sum()
                uds_sum = df.iloc[:, 2].sum()
                cobro_sum = df.iloc[:, 8].sum()
                valor_sum = df.iloc[:, 6].sum()
                          
                entry_id_remesa.insert(0, id_remesa)            
                entry_manifiesto.insert(0, manifiesto)
                entry_conductor.insert(0, conductor)
                entry_fecha.insert(0, formated_date)
                entry_total_uds.insert(0, str(uds_sum))
                entry_total_kg.insert(0, str(kg_sum))
                entry_flete_coord_rtp.insert(0, str(valor_sum))
                entry_ingreso_operativo_total.insert(0, str(valor_sum))
                entry_cobro_total.insert(0, str(cobro_sum))
                
                guias = df.values.tolist()
                guias = [row[1:] for row in guias]
                for guia in guias:
                    table.insert("", "end", values=guia)
            # clean_table_remesas()
            # list_remesas()
            get_remesa(df)
    
    tabs_remesas = ttk.Notebook(frame,)
    tabs_remesas.grid(row=0, column=0, padx=20, pady=10, sticky="nswe")
    tabs_remesas.grid_rowconfigure(0, weight=1)

    frame_remesas = ttk.Frame(frame )
    frame_remesas.grid(row=0, column=0, columnspan=2,  pady=10, sticky="nswe")
    frame_remesas.grid_columnconfigure(0, weight=1)
    
    
    frame_add_remesa = Frame(frame_remesas, )
    frame_add_remesa.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
    frame_add_remesa.grid_columnconfigure(0, weight=1)
    

    frame_form_remesa = LabelFrame(frame_add_remesa, text="Datos de la Remesa" )
    frame_form_remesa.grid(row=1, column=0, padx=(10,10), pady=10, sticky="we")

    tk.Label(frame_form_remesa, text="Remesa: (RTP)").grid(  row=1, column=0, sticky="w", padx=10 )
    entry_id_remesa = ttk.Entry(frame_form_remesa)
    entry_id_remesa.grid(row=1, column=1, padx=5, pady=5)
    entry_id_remesa.insert(0, "RTP24-")

    tk.Label(frame_form_remesa, text="Manifiesto:").grid( row=1, column=2, sticky="w", padx=10  )
    entry_manifiesto = ttk.Entry(frame_form_remesa)
    entry_manifiesto.grid(row=1, column=3, padx=5, pady=5)
    entry_manifiesto.insert(0, "MCP24-")

    ttk.Label(frame_form_remesa, text="Conductor:").grid( row=1, column=4, sticky="w", padx=10)
    entry_conductor = ttk.Entry(frame_form_remesa)
    entry_conductor.grid(row=1, column=5, padx=5, pady=5)

    ttk.Label(frame_form_remesa, text="Fecha:").grid( row=1, column=6, sticky="w", padx=10 )
    entry_fecha = DateEntry(frame_form_remesa,   foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
    # entry_fecha = Entry(frame_form_remesa, )
    # entry_fecha.insert(0, "dd/mm/yyyy")
    
    entry_fecha.grid(row=1, column=7, padx=5, ipadx=15, pady=5, )

    ttk.Label(frame_form_remesa, text="Total Unidades:").grid(row=2, column=0, sticky="w", padx=10    )
    entry_total_uds = ttk.Entry(frame_form_remesa)
    entry_total_uds.grid(row=2, column=1, padx=5, pady=5,)

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
    
    destinos_db = get_destinos_db()
    ttk.Label(frame_form_remesa, text="Destino:").grid(row=4, column=2, sticky="w", padx=10)    
    cbbx_destino_remesa = ttk.Combobox(frame_form_remesa, values=destinos_db, state="readonly")
    cbbx_destino_remesa.grid(row=4, column=3, padx=5, pady=5)

    
    
    #* FRAME TREE VIEW
    #? TABLE FOR PREVIEW
    list_camps = ("numero_guia", "unidades", "peso_Kg",  "destino", "fecha_de_asignacion", "valor", "cliente","balance_cobro",) # add volumen when be needed
    table = ttk.Treeview(frame_add_remesa,columns=list_camps, show="headings", height=10)
    table.grid(row=3, column=0, columnspan=10, sticky="wes", padx=(10,20), pady=10,)

    # Create a vertical scrollbar
    scrollbar = ttk.Scrollbar(frame_add_remesa, orient="vertical", command=table.yview)
    scrollbar.grid(row=3, column=8, sticky="wns", pady=20,) 
    table.configure(yscrollcommand=scrollbar.set)

    table.column("#0", width=0, stretch=False, anchor="center")
    table.column("numero_guia", width=120, stretch=False, anchor="center")
    table.column("unidades", width=60, stretch=False, anchor="center")
    table.column("peso_Kg", width=50, stretch=False, anchor="center")
    # table.column("volumen_m3", width=50, stretch=False, anchor="center")
    table.column("destino", width=100, stretch=False, anchor="center")
    table.column("fecha_de_asignacion", width=100, stretch=False, anchor="center")
    table.column("valor", width=100, stretch=False, anchor="center")
    table.column("cliente", width=300, stretch=False, anchor="center")
    table.column("balance_cobro", width=100, stretch=False, anchor="center")
    
    # Configurar encabezados de columna
    table.heading("numero_guia", text="Guia")
    table.heading("unidades", text="Uds")
    table.heading("peso_Kg", text="Kg")
    # table.heading("volumen_m3", text="Vol(M3)")
    table.heading("destino", text="Destino")
    table.heading("fecha_de_asignacion", text="F.Asignacion")
    table.heading("valor", text="Valor")
    table.heading("cliente", text="Cliente")
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
    
    
    btn_import_remesa = ttk.Button(frame_remesas, text="Importar Remesa", command= lambda: import_remesa())
    btn_import_remesa.grid(row=4, column=0, sticky='w', padx=25, pady=10)

    btn_guardar = ttk.Button(frame_remesas, text="Guardar Remesa", command= lambda: save_remesa())
    btn_guardar.grid(row=5, column=0, sticky='w', padx=25, pady=10)
    
    calc_total()
    tabs_remesas.add(frame_remesas, text="Agregar Remesa")    
    
    
    #********************************************************* FRAME TAB SEARCH REMESA******************************************************** #
    #********************************************************* FRAME TAB SEARCH REMESA******************************************************** #
    #********************************************************* FRAME TAB SEARCH REMESA******************************************************** #
    
    
    
    def on_double_click(event):
        item = event.widget.selection()[0]
        id_remesa = event.widget.item(item)['values'][0]
        entrysearch_remesa.delete(0, tk.END)
        entrysearch_remesa.insert(0, id_remesa)
        search_remesa(id_remesa)
        search_guias_remesa(id_remesa)
       
    def search_remesa(id_remesa):  
        #function to enable entries for editing  
        entries = [entryid_remesa, entrymanifiesto, entryconductor, entrydestino, entryfecha, entrytotal_kg, entrytotal_uds, entrytotal_volumen, entryflete_coord_rtp, entryingreso_operativo_total, entrygasto_operativo, entryutilidad, entryrentabilidad]
        
       
       
        def entries_state_enabled():               
            for entry in entries:
                entry.state(["!readonly"])
        
        def entries_state_disabled():
            # entries = [entry_id_remesa, entry_manifiesto, entry_conductor, entry_destino, entry_fecha, entry_total_kg, entry_total_uds, entry_total_volumen, entry_flete_coord_rtp, entry_ingreso_operativo_total, entry_gasto_operativo, entry_utilidad, entry_rentabilidad]

            for entry in entries:
                entry.state(["readonly"])    
        
        def entries_state_clear():
            for entry in entries:
                entry.delete(0, tk.END)
    
        
        
        
        connection = sqlite3.connect(config.db_path)
        query = f"SELECT r.id_remesa, r.manifiesto, r.conductor, d.destino, r.fecha, r.total_kg, r.total_uds, total_vol, r.flete_coord_rtp, r.ingreso_operativo_total, r. gasto_operativo, r.utilidad, r.rentabilidad FROM remesas AS r JOIN destinos  AS d ON d.destino = r.destino WHERE id_remesa = '{id_remesa}'";       
        result = connection.execute(query)
        data = result.fetchall() 
        connection.close()                
        if data:            
            btn_edit_remesa = ttk.Button(frame_search_single_remesa, text="Editar", command= lambda: entries_state_enabled(), )
            btn_edit_remesa.grid(row=1, column=3, sticky="w", padx=5, pady=5)
            
            btn_save_remesa = ttk.Button(frame_search_single_remesa, text="Guardar", command= lambda: entries_state_disabled(), )
            btn_save_remesa.grid(row=1, column=4, sticky="w", padx=5, pady=5)
            
            btn_delete_remesa = ttk.Button(frame_search_single_remesa, text="Borrar", command= lambda: delete_remesa(entryid_remesa.get()) )
            btn_delete_remesa.grid(row=1, column=5, sticky="w", padx=5, pady=5)
            
            entries_state_enabled()  
            entries_state_clear()
            entryid_remesa.insert(0, data[0][0])
            entrymanifiesto.insert(0, data[0][1])
            entryconductor.insert(0, data[0][2])
            entrydestino.insert(0, data[0][3])
            entryfecha.insert(0, data[0][4])
            entrytotal_kg.insert(0, data[0][5])
            entrytotal_uds.insert(0, data[0][6])
            entrytotal_volumen.insert(0, data[0][7])
            entryflete_coord_rtp.insert(0, data[0][8])
            entryingreso_operativo_total.insert(0, data[0][9])
            entrygasto_operativo.insert(0, data[0][10])
            entryutilidad.insert(0, data[0][11])
            entryrentabilidad.insert(0,str(data[0][12]))
            entries_state_disabled()

    def search_guias_remesa(id_remesa):
        connection = sqlite3.connect(config.db_path)
        query = f'''
                   SELECT 
                        guias.numero_guia, 
                        guias.estado, 
                        guias.destino, 
                        guias.destinatario, 
                        guias.unidades, 
                        guias.peso_Kg, 
                        guias.volumen_m3, 
                        destinos.valor_destino_1, 
                        guias.fecha_de_asignacion, 
                        COALESCE(anexos_guias.anexo_id, 'SIN ANEXO') AS en_anexo,
                        COALESCE(facturas_guias.factura_id, 'SIN FACT.') AS en_factura
                    FROM 
                        guias 
                    JOIN 
                        remesas_guias ON guias.numero_guia = remesas_guias.guia_id 
                    JOIN 
                        remesas ON remesas.id_remesa = remesas_guias.remesa_id 
                    JOIN 
                        destinos ON destinos.destino = guias.destino 
                    LEFT JOIN 
                        anexos_guias ON guias.numero_guia = anexos_guias.guia_id
                    LEFT JOIN 
                        facturas_guias ON guias.numero_guia = facturas_guias.guia_id
                    WHERE 
                        remesas.id_remesa = '{id_remesa}';                      
                    '''
        result = connection.execute(query)
        data = result.fetchall()
        table_list_guias.delete(*table_list_guias.get_children())      
       
        for row in data:            
            # Configurar encabezados de columna
            # table_list_guias.column("#0", width=0, stretch=False, anchor="center")
            table_list_guias.column("numero_guia", width=150, stretch=False, anchor="center")
            table_list_guias.column("estado", width=180, stretch=False, anchor="center")
            table_list_guias.column("destino", width=150, stretch=False, anchor="center")
            table_list_guias.column("destinatario", width=200, stretch=False, anchor="center")
            table_list_guias.column("unidades", width=50, stretch=False, anchor="center")
            table_list_guias.column("peso_Kg", width=50, stretch=False, anchor="center")
            table_list_guias.column("volumen_m3", width=50, stretch=False, anchor="center")
            table_list_guias.column("valor", width=100, stretch=False, anchor="center")
            table_list_guias.column("fecha_de_asignacion", width=100, stretch=False, anchor="center")
            table_list_guias.column("en_anexo", width=75, stretch=False, anchor="center")
            table_list_guias.column("en_factura", width=75, stretch=False, anchor="center")
            
            
            table_list_guias.heading("numero_guia", text="Guia")
            table_list_guias.heading("estado", text="Estado")
            table_list_guias.heading("destino", text="Destino")
            table_list_guias.heading("destinatario", text="Destinatario")
            table_list_guias.heading("unidades", text="Uds")                        
            table_list_guias.heading("peso_Kg", text="Kg")
            table_list_guias.heading("volumen_m3", text="Vol(M3)")
            table_list_guias.heading("valor", text="Valor")
            table_list_guias.heading("fecha_de_asignacion", text="F. Asignacion")
            table_list_guias.heading("en_anexo", text="Anexo")
            table_list_guias.heading("en_factura", text="Factura")       
            
            # table_list_guias.insert("", "end", values=row)     
            
            if row[10] != 'SIN FACT.':
                table_list_guias.insert("", "end", values=row, tags=("paid_invoice",))
            # elif row[9] != 'no':
            #     table_list_guias.insert("", "end", values=row, tags=("pend_invoice",))
            else: 
                table_list_guias.insert("", "end", values=row, tags=("pend_invoice",) )     
        connection.close()
        return data

    def btnsearch_remesa(id_remesa):        
        if id_remesa:
            found = False
            for item in table_list_remesas.get_children():
                if table_list_remesas.item(item, "values")[0] == id_remesa:
                    table_list_remesas.selection_set(item)
                    found = True
                    break
            
            if not found:
                messagebox.showinfo("Información", "No se encontró la remesa")
            else:
                search_remesa(id_remesa)
                search_guias_remesa(id_remesa)
        else:
            messagebox.showerror("Error", "Por favor, ingrese un ID de remesa")

    
    #********** TABLE LIST  REMESAS **********#
    #********** TABLE LIST  REMESAS **********#
    frame_search_remesa = ttk.Frame(frame,)
    frame_search_remesa.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="wens" )
    # for i in range(8):
    #     frame_search_remesa.grid_columnconfigure(i, weight=1)
    frame_search_remesa.grid_columnconfigure(0, weight=1)
    
    
    entry_cols = ("id_remesa", "manifiesto", "destino", "conductor", "fecha", "ingreso_operativo_total", "rentabilidad", "total_guias", "guias_facturadas", "guias_sin_facturar")
    table_list_remesas = ttk.Treeview(frame_search_remesa, columns= entry_cols, show="headings", height=10)
    for col in entry_cols:
        table_list_remesas.heading(col, text=col)
        table_list_remesas.column(col, width=115, stretch=False, anchor="center")

    table_list_remesas.grid(row=0, column=0, sticky="ew",  pady=5,)
    table_list_remesas.bind("<ButtonRelease-1>", on_double_click)
    
    scrollbar = ttk.Scrollbar(frame_search_remesa, orient="vertical", command=table_list_remesas.yview)
    scrollbar.grid(row=0, column=9, sticky="ns", pady=10,) 
    table_list_remesas.configure(yscrollcommand=scrollbar.set)
    
    
    #***********ENTRIES REMESA***********#
    #***********ENTRIES REMESA***********#
    
    frame_edit_remesa = ttk.Frame(frame_search_remesa)
    frame_edit_remesa.grid(row=2, column=0, pady=10, sticky="")            
    
    frame_search_single_remesa = ttk.Frame(frame_search_remesa,)
    frame_search_single_remesa.grid(row=1, column=0, columnspan=1,  pady=5, sticky="w")    
    
    btn_search_remesa = ttk.Button(frame_search_single_remesa, text="Buscar Remesa", command=lambda: btnsearch_remesa(entrysearch_remesa.get()))
    btn_search_remesa.grid(row=1, column=0, sticky="w",  pady=5)    
    
    entrysearch_remesa = ttk.Entry(frame_search_single_remesa, justify="center")
    entrysearch_remesa.grid(row=1, column=1,  pady=5)    
    
    
    ttk.Label(frame_edit_remesa, text="ID Remesa:").grid(row=0, column=0, sticky="w", padx=5)
    entryid_remesa = ttk.Entry(frame_edit_remesa)
    entryid_remesa.grid(row=0, column=1,  pady=5)
    entryid_remesa.state(["readonly"])
    
    ttk.Label(frame_edit_remesa, text="Manifiesto:").grid(row=0, column=2, sticky="w", padx=5)
    entrymanifiesto = ttk.Entry(frame_edit_remesa)
    entrymanifiesto.grid(row=0, column=3,  pady=5)
    entrymanifiesto.state(["readonly"])
    
    ttk.Label(frame_edit_remesa, text="Conductor:").grid(row=0, column=4, sticky="w", padx=5)
    entryconductor = ttk.Entry(frame_edit_remesa)
    entryconductor.grid(row=0, column=5,  pady=5)        
    entryconductor.state(['readonly'])
    
    ttk.Label(frame_edit_remesa, text="Destino:").grid(row=0, column=6, sticky="w", padx=5)
    entrydestino = ttk.Entry(frame_edit_remesa)
    entrydestino.grid(row=0, column=7,  pady=5)        
    entrydestino.state(['readonly'])
    
    ttk.Label(frame_edit_remesa, text="Fecha:").grid(row=0, column=8, sticky="w", padx=5)
    entryfecha = ttk.Entry(frame_edit_remesa)
    entryfecha.grid(row=0, column=9,  pady=5)        
    entryfecha.state(['readonly'])
    
    ttk.Label(frame_edit_remesa, text="Total Kg:").grid(row=1, column=0, sticky="w", padx=5)
    entrytotal_kg = ttk.Entry(frame_edit_remesa)
    entrytotal_kg.grid(row=1, column=1,  pady=5)        
    entrytotal_kg.state(['readonly'])
    
    ttk.Label(frame_edit_remesa, text="Total Uds:").grid(row=1, column=2, sticky="w", padx=5)
    entrytotal_uds = ttk.Entry(frame_edit_remesa)
    entrytotal_uds.grid(row=1, column=3,  pady=5)        
    entrytotal_uds.state(['readonly'])
    
    ttk.Label(frame_edit_remesa, text="Total Volumen:").grid(row=1, column=4, sticky="w", padx=5)
    entrytotal_volumen = ttk.Entry(frame_edit_remesa)
    entrytotal_volumen.grid(row=1, column=5,  pady=5)        
    entrytotal_volumen.state(['readonly'])

    
    ttk.Label(frame_edit_remesa, text="Flete Coord RTP:").grid(row=1, column=6, sticky="w", padx=5)
    entryflete_coord_rtp = ttk.Entry(frame_edit_remesa)
    entryflete_coord_rtp.grid(row=1, column=7,  pady=5)        
    entryflete_coord_rtp.state(['readonly'])
    
    
    ttk.Label(frame_edit_remesa, text="Ingreso Op. Total:").grid(row=1, column=8, sticky="w", padx=5)
    entryingreso_operativo_total = ttk.Entry(frame_edit_remesa)
    entryingreso_operativo_total.grid(row=1, column=9,  pady=5)        
    entryingreso_operativo_total.state(['readonly'])
    
    ttk.Label(frame_edit_remesa, text="Gasto Operativo:").grid(row=2, column=0, sticky="w", padx=5)
    entrygasto_operativo = ttk.Entry(frame_edit_remesa)
    entrygasto_operativo.grid(row=2, column=1,  pady=5)        
    entrygasto_operativo.state(['readonly'])
    
    ttk.Label(frame_edit_remesa, text="Utilidad:").grid(row=2, column=2, sticky="w", padx=5)
    entryutilidad = ttk.Entry(frame_edit_remesa)
    entryutilidad.state(['readonly'])
    entryutilidad.grid(row=2, column=3,  pady=5)        
    
    ttk.Label(frame_edit_remesa, text="Rentabilidad:").grid(row=2, column=4, sticky="w", padx=5)
    entryrentabilidad = ttk.Entry(frame_edit_remesa)
    entryrentabilidad.grid(row=2, column=5,  pady=5)        
    entryrentabilidad.state(['readonly'])      

    
    #***********TABLE LIST GUIAS-REMESA***********#
    #***********TABLE LIST GUIAS-REMESA***********#    
    
    
    frame_search = ttk.LabelFrame(frame_search_remesa,  )
    frame_search.grid(row=3, column=0, padx=10, pady=10, sticky="we", )
    
    list_camps = ("numero_guia", "estado", "destino", "destinatario", "unidades", "peso_Kg", "volumen_m3", "valor","fecha_de_asignacion", "en_anexo", "en_factura")
    table_list_guias = ttk.Treeview(frame_search_remesa, columns=list_camps, show="headings", height=9)
    table_list_guias.grid(row=3, column=0,  columnspan=2, pady=10, sticky="we")
    
    table_list_guias.tag_configure("paid_invoice", background="#cff6c8")
    table_list_guias.tag_configure("pend_invoice", background="#fefda6")   
    
    vscrollbar = ttk.Scrollbar(frame_search_remesa, orient="vertical", command=table_list_guias.yview)
    vscrollbar.grid(row=3, column=9, sticky="ns")
    table_list_guias.configure(yscrollcommand=vscrollbar.set)
    
    hscrollbar = ttk.Scrollbar(frame_search_remesa, orient="horizontal", command=table_list_guias.xview)
    hscrollbar.grid(row=4, column=0, sticky="wes")
    table_list_guias.configure(xscrollcommand=hscrollbar.set)
    

    tabs_remesas.add(frame_search_remesa, text="Buscar Remesa")
    
    list_remesas()
    