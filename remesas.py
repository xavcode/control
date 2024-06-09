import os
import tkinter as tk
import sqlite3

import colors
import pandas as pd
from config import load_config
from pandas import ExcelWriter
from datetime import datetime
from tkinter import *   # type: ignore # noqa: F403
from tkinter import messagebox
from tkinter import ttk as ttks
import ttkbootstrap as ttk

def _convert_stringval(value):
    if hasattr(value, 'typename'):
        value = str(value)
        try:
            value = int(value)
        except (ValueError, TypeError):
            pass
    return value

ttks._convert_stringval = _convert_stringval # type: ignore

def show_remesas(frame, tab_to_show, width, height):
    config = load_config()
    db_path = config['db_path'] # type: ignore
    def focus_tab(tab):
        tab.select(tab_to_show) 
    for widget in frame.winfo_children():
        widget.grid_forget()

    def calc_total():
        total_unidades = 0
        total_kilos = 0
        total_volumen = 0
        total_cobro = 0
        total_valor = 0
        total_utilidad = 0
        total_rentabilidad = 0
        
        for item in table_add_guia.get_children():
            values = table_add_guia.item(item, "values")
            try:
                unidades = int(values[1])
                kilos = int(values[2])
                volumen = int(values[3])
                valor = int(values[6].replace(",", ""))
                cobro = int(values[8].replace(",", ""))
            except (ValueError, IndexError):
                messagebox.showerror("", "Error obteniendo los valores. ")
                continue

            gasto_operativo = entry_gasto_operativo.get().replace(",", "")
            try:
                gasto_operativo = int(gasto_operativo)
            except ValueError:
                gasto_operativo = 1

            if gasto_operativo == 0:
                gasto_operativo = 1

            total_unidades += unidades
            total_kilos += kilos    
            total_valor += valor    
            total_cobro += cobro                
            total_volumen += volumen
            total_utilidad = (total_valor - gasto_operativo)
            total_rentabilidad = (total_valor / gasto_operativo)
        
        entry_flete_coord_rtp.state(["!readonly"])
        entry_flete_coord_rtp.delete(0,tk.END)
        entry_flete_coord_rtp.insert(0, "{:,}".format(total_valor))
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
        entry_cobro_total.insert(0, "{:,}".format(total_cobro))
        entry_cobro_total.state(["readonly"])
        
        entry_ingreso_operativo_total.state(["!readonly"])
        entry_ingreso_operativo_total.delete(0,tk.END)
        entry_ingreso_operativo_total.insert(0, "{:,}".format(total_valor))
        entry_ingreso_operativo_total.state(["readonly"])
                
        value = entry_gasto_operativo.get().replace(",", "")
        if value == "" or value is None:
            value = 0
        entry_gasto_operativo.delete(0,tk.END)
        entry_gasto_operativo.insert(0, str(value))
       
        entry_utilidad.state(["!readonly"])
        entry_utilidad.delete(0,tk.END)
        entry_utilidad.insert(0, "{:,}".format(total_utilidad))
        entry_utilidad.state(["readonly"])
        
        entry_rentabilidad.state(["!readonly"])
        entry_rentabilidad.delete(0,tk.END)
        entry_rentabilidad.insert(0, str(total_rentabilidad))
        entry_rentabilidad.state(["readonly"])
    def clean_fields_guia():
        enable_entries_guia()
        entry_guia.delete(0, tk.END)
        entry_unidades.delete(0, tk.END)
        entry_peso.delete(0, tk.END)
        entry_volumen.delete(0, tk.END)
        entry_destino.delete(0, tk.END)
        entry_fecha_asignacion.delete(0, tk.END)
        entry_cliente.delete(0, tk.END)
        entry_valor.delete(0, tk.END)
        entry_balance_cobro.delete(0, tk.END)    
        disable_entries_guia()            
    def get_info_guia(id_guia):
        if not id_guia:
            messagebox.showerror("", "Ingrese un número de guía")
            return False
        try:         
            connection = sqlite3.connect(db_path)
            query = f'''
                        SELECT 
                        guias.numero_guia, 
                        guias.unidades, 
                        guias.peso_Kg, 
                        guias.volumen_m3, 
                        guias.destino, 
                        guias.fecha_de_asignacion, 
                        guias.destinatario, 
                        (guias.balance_RCE + guias.balance_FCE) AS balance_cobro,
                        destinos.valor_destino_1,
                        destinos.valor_destino_2,
                        destinos.valor_destino_3,
                        destinos.extra
                        FROM guias 
                        JOIN destinos ON destinos.destino = guias.destino 
                        WHERE guias.numero_guia = '{id_guia}';
                    '''
            result = connection.execute(query)
            data = result.fetchall()
            if not data :
                messagebox.showerror("", "No se encontró la guia")
                entry_guia.delete(0, tk.END)
                # entry_valor.delete(0, tk.END)
                return
            connection.close()
            clean_fields_guia()
            enable_entries_guia()

            for row in data: 
                entry_guia.insert(0, row[0])   
                entry_unidades.insert(0, row[1])
                entry_peso.insert(0, row[2])
                entry_volumen.insert(0, row[3])
                entry_destino.insert(0, row[4])
                entry_fecha_asignacion.insert(0, row[5])
                entry_cliente.insert(0, row[6])
                entry_balance_cobro.insert(0, "{:,}".format(row[7]))
                
            disable_entries_guia()
            entry_valor.insert(0, "{:,}".format(calculate_cost(row[2], row[3], row[1], row[8], row[9], row[10], row[11])))
            entry_valor.select_range(0, tk.END)
            return data
        except Exception as e:
            messagebox.showerror("", f"Error al obtener la guia o no se encuentra: {str(e)}")
        disable_entries_guia()    
    def calculate_cost(peso,volumen,unds, valor_1, valor_2, valor_3, extra):
        greater = max(peso,volumen)
        single_unit = greater/unds
        cost = 0
        if single_unit <=5:
            cost = valor_1*unds

        elif single_unit > 5 and single_unit <= 30:
            cost = int(valor_2*unds)
            
        elif single_unit > 30 and single_unit <= 50:
            cost = int(valor_3*unds)
            
        else:
            remaining = single_unit - 50
            excedent_value = extra * remaining
            cost = int((valor_3 + excedent_value)*unds)
        return cost
    def add_guia_to_remesa():
        data = get_info_guia(entry_guia.get())
        if data is None:
            return        
        try: 
            entry_guia_value = entry_guia.get().strip()
            for item in table_add_guia.get_children():
                if entry_guia_value == table_add_guia.item(item, "values")[0]:
                    messagebox.showerror("", "La guia ya ha sido agregada")
                    return
            data = [
                entry_guia_value,
                int(entry_unidades.get()),
                int(entry_peso.get()),
                int(entry_volumen.get()),
                entry_destino.get().strip(),
                entry_fecha_asignacion.get().strip(),
                int(entry_valor.get().replace(",", "")),
                entry_cliente.get().strip(),
                int(entry_balance_cobro.get().replace(",", ""))
            ]        

            data[6] = "{:,}".format(int(data[6]))
            data[8] = "{:,}".format(int(data[8]))
            
            if data[8] != 0:
                # table_add_guia.insert("", "end", values=data, tags=("has_cobro")) ENABLE THIS LINE TO ADD A COLOR TO THE ROW
                table_add_guia.insert("", "end", values=data, )
            else:
                table_add_guia.insert("", "end", values=data)
            calc_total()
            # entry_guia.focus_set()            
            entry_guia.select_range(0, tk.END)
        except Exception as e:
            messagebox.showerror("", f"Error al agregar la guia: {str(e)}")  
    def double_click_guia(event):
        item = event.widget.selection()[0]
        guia = table_add_guia.item(item)['values'][0]
        entry_guia.delete(0, tk.END)
        entry_guia.insert(0, guia)
    def delete_row():
        selected_item = table_add_guia.selection()
        if selected_item:
            table_add_guia.delete(*selected_item)  
        calc_total()
        calc_gans()
    def calc_utilidad():        
        total_ingreso = int(entry_ingreso_operativo_total.get().replace(",", ""))
        if "," in str(total_ingreso):
            total_gasto = int(entry_gasto_operativo.get().replace(",", ""))
        else:
            total_gasto = int(entry_gasto_operativo.get())
            
        total_utilidad = total_ingreso - total_gasto
        
        if total_utilidad < 1:
            total_utilidad = 0
        entry_utilidad.state(["!readonly"])
        entry_utilidad.delete(0, tk.END)
        entry_utilidad.insert(0, "{:,}".format(total_utilidad))
        entry_utilidad.state(["readonly"])
    def calc_rentabilidad():
        rentabilidad = 0.0
        total_utilidad = int(entry_utilidad.get().replace(",",""))                
        if total_utilidad == 0 or total_utilidad is None:
            total_utilidad = 1
        else:
            total_utilidad = int(total_utilidad)                
        total_ingreso = int(entry_ingreso_operativo_total.get().replace(",",""))
        rentabilidad = float((total_utilidad / total_ingreso)*100).__round__(2)
        entry_rentabilidad.state(["!readonly"])
        entry_rentabilidad.delete(0, tk.END)
        entry_rentabilidad.insert(0, "{:.2f}".format(rentabilidad))
        entry_rentabilidad.state(["readonly"])
    def calc_gans():               
        calc_utilidad()
        calc_rentabilidad()
    def save_remesa():                
        id_remesa = entry_id_remesa.get()
        if not id_remesa:
            messagebox.showerror("", "Ingrese un número de remesa")
            return
        id_manifiesto = entry_manifiesto.get()
        if not id_manifiesto:
            messagebox.showerror("", "Ingrese un número de manifiesto")
            return
        conductor = entry_conductor.get()
        fecha_remesa = entry_fecha.entry.get()
        total_uds = entry_total_uds.get()
        total_kg = entry_total_kg.get()
        total_volumen = entry_total_volumen.get()
        cobro_total = entry_cobro_total.get().replace(",", "")
        flete_coord_rtp = entry_flete_coord_rtp.get().replace(",", "")
        ingreso_operativo_total = entry_ingreso_operativo_total.get().replace(",", "")
        gasto_operativo = entry_gasto_operativo.get().replace(",", "")
        utilidad = entry_utilidad.get().replace(",", "")
        rentabilidad = entry_rentabilidad.get()
        destino_remesa = cbbx_destino_remesa.get()
        if not table_add_guia.get_children():
            messagebox.showerror("", "No se han agregado guias a la remesa")
            return
        if not destino_remesa:
            messagebox.showerror("", "El campo Destino no puede estar vacío")
            return        
        connection = sqlite3.connect(db_path)
        query = f'''
                    INSERT INTO remesas(
                        id_remesa, 
                        manifiesto, 
                        conductor, 
                        destino, 
                        fecha, total_uds, 
                        total_kg, 
                        total_vol, 
                        cobro_total, 
                        flete_coord_rtp, 
                        ingreso_operativo_total, 
                        gasto_operativo,
                        utilidad, 
                        rentabilidad)
                        VALUES ('{id_remesa}', '{id_manifiesto}', '{conductor}', '{destino_remesa}', '{fecha_remesa}', '{total_uds}', '{total_kg}', '{total_volumen}', '{cobro_total}', '{flete_coord_rtp}', '{ingreso_operativo_total}', '{gasto_operativo}', '{utilidad}', '{rentabilidad}');
                 '''        
        #create the list for insert guias
        rows_to_insert = []
        for row in table_add_guia.get_children():
            row_values = table_add_guia.item(row)["values"]        
            rows_to_insert.append(row_values)
      
        #create the query for the insert
        query_remesas = "INSERT INTO remesas_guias (remesa_id, guia_id, valor ) VALUES "
        
        for i in range(len(rows_to_insert)):
            row = rows_to_insert[i]
            query_remesas += f"('{id_remesa}', '{row[0]}','{str(row[6]).replace(',', '')}')"
            if i != len(rows_to_insert) - 1:
                query_remesas += ", "
            else:
                query_remesas += ";"
        try:
            result = connection.execute(query)
            result = connection.execute(query_remesas)
            connection.commit()
            if result:
                clean_table_remesas()
                get_latest_remesa()
                list_remesas()
                clean_entries_remesa()
                clean_table_guias()
                clean_fields_guia()
                calc_total()
                messagebox.showinfo("", "Remesa guardada con éxito")
        except Exception as e:
            error_message = str(e)
            if "UNIQUE constraint failed" in error_message:
                messagebox.showerror("", f"Ya existe la remesa: {id_remesa}")
            connection.close() 
        connection.close() 
        entry_editar_remesa.delete(0, tk.END)
        get_latest_remesa()
    def delete_remesa(id_remesa):
        try:
            confirmed = messagebox.askyesno("Confirmar", f"Desea borrar la remesa {id_remesa}?")
            if not confirmed:
                return
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()

            # Primera consulta para eliminar de la tabla remesas_guias
            query_remesas_guias = f"DELETE FROM remesas_guias WHERE remesa_id = '{id_remesa}';"
            
            cursor.execute(query_remesas_guias)
            connection.commit()

            # Segunda consulta para eliminar de la tabla remesas
            query_remesas = f"DELETE FROM remesas WHERE id_remesa = '{id_remesa}';"
            cursor.execute(query_remesas)

            connection.commit()
            connection.close()
            messagebox.showinfo("", "Remesa eliminada con éxito")
            clean_table_remesas()
            list_remesas()
        except sqlite3.Error as e:
            messagebox.showerror("", f"Error al eliminar la remesa: {e}")
        
        table_list_guias.delete(*table_list_guias.get_children())
        clean_table_remesas()

        list_entries_remesa_search = entryid_remesa, entrymanifiesto, entryconductor, entryfecha, entrytotal_kg, entrytotal_uds, entrytotal_volumen, entryflete_coord_rtp, entryingreso_operativo_total, entrygasto_operativo, entryutilidad, entryrentabilidad

        for entry in list_entries_remesa_search:
            entry.state(["!readonly"])
        for entry in list_entries_remesa_search:
            entry.delete(0, tk.END)
        for entry in list_entries_remesa_search:
            entry.config(state="readonly")
        

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
    def enable_entries_guia():
        entry_unidades.state(["!readonly"])
        entry_peso.state(["!readonly"])
        entry_volumen.state(["!readonly"])
        entry_destino.state(["!readonly"])
        entry_fecha_asignacion.state(["!readonly"])
        entry_cliente.state(["!readonly"])
        # entry_valor.state(["!readonly"])
        entry_balance_cobro.state(["!readonly"])
    def disable_entries_guia():
        entry_unidades.state(["readonly"])
        entry_peso.state(["readonly"])
        entry_volumen.state(["readonly"])
        entry_destino.state(["readonly"])
        entry_fecha_asignacion.state(["readonly"])
        entry_cliente.state(["readonly"])
        # entry_valor.state(["readonly"])
        entry_balance_cobro.state(["readonly"])    
    def disable_entries():
        entry_total_uds.state(["readonly"])
        entry_total_kg.state(["readonly"])
        entry_total_volumen.state(["readonly"])
        entry_cobro_total.state(["readonly"])
        entry_flete_coord_rtp.state(["readonly"])
        entry_ingreso_operativo_total.state(["readonly"])
        # entry_gasto_operativo.state(["readonly"])
        entry_utilidad.state(["readonly"])
        entry_rentabilidad.state(["readonly"])
    def clean_entries_remesa():
        enable_entries()
        entry_id_remesa.delete(0, tk.END)   
        entry_manifiesto.delete(0, tk.END)
        entry_conductor.delete(0, tk.END)
        entry_fecha.entry.delete(0, tk.END)
        entry_total_uds.delete(0, tk.END)        
        entry_total_kg.delete(0, tk.END)
        entry_total_volumen.delete(0, tk.END)
        entry_cobro_total.delete(0, tk.END)
        entry_flete_coord_rtp.delete(0, tk.END)
        entry_ingreso_operativo_total.delete(0, tk.END)
        entry_gasto_operativo.delete(0, tk.END)
        entry_gasto_operativo.delete(0, tk.END)
        entry_utilidad.delete(0, tk.END)
        entry_rentabilidad.delete(0, tk.END)

        cbbx_destino_remesa.set('')      
    def new_remesa():
        clean_entries_remesa()
        clean_table_guias()
        clean_fields_guia()
        calc_total()
        cbbx_destino_remesa.set('')
        actual_date = datetime.now().strftime("%d-%m-%Y")
        entry_fecha.entry.insert(0,str(actual_date))
        get_latest_remesa()
    def list_remesas():
        connection = sqlite3.connect(db_path)
        query = '''
                    SELECT 
                        remesas.id_remesa, 
                        remesas.manifiesto, 
                        remesas.destino, 
                        remesas.conductor, 
                        remesas.fecha, 
                        remesas.ingreso_operativo_total, 
                        remesas.rentabilidad, 
                        COUNT(remesas_guias.remesa_id) AS 'Total Guias',
						COUNT(facturas_guias.remesa_id) AS 'Facturadas',
						COUNT(remesas_guias.remesa_id) - COUNT(facturas_guias.remesa_id) as 'Por facturar'

                    FROM 
                        remesas
                    LEFT JOIN 
                        remesas_guias ON remesas.id_remesa = remesas_guias.remesa_id
                    LEFT JOIN 
                        facturas_guias ON facturas_guias.guia_id = remesas_guias.guia_id
					GROUP BY 
                        remesas.id_remesa
                    ORDER BY 
                    SUBSTR(remesas.id_remesa, 1, INSTR(remesas.id_remesa, '-') - 1), 
                    CAST(SUBSTR(remesas.id_remesa, INSTR(remesas.id_remesa, '-') + 1) AS INTEGER)DESC
                '''
        
        result = connection.execute(query)
        data = result.fetchall()
        
        for row in data:
            row_list = list(row)            
            row_list[5] = "{:,}".format(row_list[5])
            table_list_remesas.insert("", "end", values=row_list)
        connection.close()  
    def get_destinos_db() :
        connection = sqlite3.connect(db_path)
        query = "SELECT destino FROM destinos;"
        result = connection.execute(query)
        data = result.fetchall()
        options = [item[0] for item in data]        
        connection.close()
        return options
    def clean_table_remesas():
            table_list_remesas.delete(*table_list_remesas.get_children())       
    def clean_table_guias():
        table_add_guia.delete(*table_add_guia.get_children())
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
        id_remesa = str(df.iat[0, 5].strip())
        manifiesto = str(df.iat[0, 7].strip())
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
        #adding vol column filled with ceros,
        df.insert(3, 'Vol', 0)
        
        # delet characters in column cobros
        
        df['COBRO'] = df['COBRO'].apply(lambda x: str(x).replace('.', ''))
        df['COBRO'] = df['COBRO'].apply(lambda x: ''.join(c for c in x if c.isdigit()))
        df['COBRO'] = df['COBRO'].apply(lambda x: 0 if not str(x).isdigit() else x)
        df['COBRO'] = pd.to_numeric(df['COBRO'])                
        
        kg_sum = df.iloc[:, 4].sum()
        cobro_sum = df.iloc[:, 9].sum()
        uds_sum = df.iloc[:, 2].sum()
        cobro_sum = df.iloc[:, 9].sum()
        valor_sum = df.iloc[:, 7].sum()
        
        entry_id_remesa.insert(0, id_remesa)            
        entry_manifiesto.insert(0, manifiesto)
        entry_conductor.insert(0, conductor)
        entry_fecha.entry.insert(0, formated_date)
        entry_total_uds.insert(0, str(uds_sum))
        entry_total_kg.insert(0, str(kg_sum))
        entry_total_volumen.insert(0, str(0))
        entry_flete_coord_rtp.insert(0, str(valor_sum))
        entry_ingreso_operativo_total.insert(0, str(valor_sum))
        entry_gasto_operativo.insert(0, str(0)) 
        entry_cobro_total.insert(0, str(cobro_sum))
        entry_utilidad.insert(0, str(valor_sum - cobro_sum))
        entry_rentabilidad.insert(0, str((valor_sum / 1) * 100))
        
        guias = df.values.tolist()
        guias = [row[1:] for row in guias]
        
        clean_table_guias()
        for guia in guias:
            if guia[8] != 0:
                # table_add_guia.insert("", "end", values=guia, tags=("has_cobro",))  ENABLE THIS LINE TO ADD A COLOR TO THE ROW
                table_add_guia.insert("", "end", values=guia)
            else :
                table_add_guia.insert("", "end", values=guia)   
            
                table_add_guia.insert("", "end", values=guia)
        # clean_table_remesas()
        # list_remesas()
    def import_remesa_from_app():
                
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        file_path = os.path.join(desktop_path, "plantilla_remesas.xlsx")
        if not os.path.exists(file_path):
            messagebox.showerror("", "No se encontró la plantilla de remesas en el escritorio")
            return
        
        if file_path:           
            # Convierte el DataFrame a string y divídelo por líneas para crear una lista de filas
            df = pd.read_excel(file_path, header=None)
            get_remesa(df)   
    def export_remesa():
        if not entry_id_remesa.get():
            messagebox.showerror("", "Ingrese un número de remesa")
            return
        if not entry_manifiesto.get():
            messagebox.showerror("", "Ingrese un número de manifiesto")
            return
        
        if not table_add_guia.get_children():
            messagebox.showerror("", "No se han agregado guias a la remesa")
            return
        
        # file_location = config['remesas_path'] # type: ignore
        # file_name = f"{entry_id_remesa.get()}.xlsx"
        # file_path = filedialog.asksaveasfilename(initialdir=file_location, initialfile=file_name, filetypes=[("Excel Files", "*.xlsx")])
        
        file_location = config['remesas_path'] # type: ignore
        file_name = f"{entry_id_remesa}.xlsx"
        file_path = os.path.join(file_location, file_name)
        if not os.path.exists(file_location):
            os.makedirs(file_location)
    
        
        if file_path:
        # Create a DataFrame from the table_add_guia
            data_remesa = []
            for item in table_add_guia.get_children():
                values = list(table_add_guia.item(item, 'values'))
                values[0] = str(values[0]) # type: ignore
                values[1] = int(values[1]) # type: ignore
                values[2] = int(values[2]) # type: ignore
                values[3] = int(values[3]) # type: ignore
                values[6] = int(values[6].replace(",", "")) # type: ignore
                values[8] = int(values[8].replace(",", "")) # type: ignore
                data_remesa.append(values)
                values.pop(3)
            
            df_remesa = pd.DataFrame(data_remesa, columns=["GUIA", "CANT", "Kg",  "DESTINO", "FE. RECEP", "VALOR", "CLIENTE", "COBRO"], )            
            df_remesa["VALOR"] = " "
            df_remesa.index += 1

            with ExcelWriter(file_path, engine='xlsxwriter') as writer:
                df_remesa.to_excel(writer, index=True, sheet_name='Hoja1', header=True, startrow=2)
                df_remesa = df_remesa.drop(df_remesa.columns[4], axis=1)
        
                # Acceder a la hoja de cálculo activa
                worksheet = writer.sheets['Hoja1']

                # Combina las celdas para el encabezado
                conductor = entry_conductor.get()
                id_remesa = entry_id_remesa.get()
                fecha = entry_fecha.entry.get()
                manifiesto = entry_manifiesto.get()
                destino = cbbx_destino_remesa.get()
                
                worksheet.merge_range('A1:I1', 'RELACION REMISIONES ENTREGADAS AL CONDUCTOR - COORDINADORA', writer.book.add_format({'align': 'center', 'font_size': 9,'bg_color': colors.bg_relaciones_conductor, 'border': 1, 'bold': True})) # type: ignore
                
                worksheet.merge_range('A2:B2', 'CONDUCTOR:', writer.book.add_format({'align': 'center', 'font_size': 9,'border': 1, 'bold': True})) # type: ignore
                
                worksheet.merge_range('C2:E2', conductor, writer.book.add_format({'align': 'center', 'border': 1, 'font_size': 9, 'bold': True})) # type: ignore
                
                worksheet.write(1, 5, id_remesa, writer.book.add_format({'align': 'center', 'font_size': 9, 'border': 1, 'bold': True})) # type: ignore
                worksheet.write(1, 6, manifiesto, writer.book.add_format({'align': 'center', 'font_size': 9, 'border': 1, 'bold': True})) # type: ignore                
                # worksheet.write(1, 7, destino, writer.book.add_format({'align': 'center', 'font_size': 9, 'text_wrap': False, 'border': 1, 'bold': True})) # type: ignore
                worksheet.write(1, 7, 'FECHA', writer.book.add_format({'align': 'center', 'font_size': 9, 'border': 1, 'bold': True})) # type: ignore
                worksheet.write(1, 8, fecha, writer.book.add_format({'align': 'center', 'font_size': 9, 'num_format': 'dd/mmmm/yyyy', 'border': 1, 'bold': True})) # type: ignore
                worksheet.write(2, 0, 'No.', writer.book.add_format({'align': 'center', 'font_size': 9, 'bold': True, 'border': 1})) # type: ignore
                
                #SET THE WIDTH OF THE WHOLE COLUMNS
                worksheet.set_column('A2:I2', cell_format=writer.book.add_format({'align': 'center', 'font_size': 9})) # type: ignore
                worksheet.set_column('A:A', 3, cell_format=writer.book.add_format({'align': 'center', 'font_size': 9, 'num_format': '@'})) # type: ignore
                worksheet.set_column('B:B', 10, cell_format=writer.book.add_format({'align': 'center', 'font_size': 9})) # type: ignore
                worksheet.set_column('C:C', 4, cell_format=writer.book.add_format({'align': 'center', 'font_size': 9})) # type: ignore
                worksheet.set_column('D:D', 4, cell_format=writer.book.add_format({'align': 'center', 'font_size': 9})) # type: ignore
                # worksheet.set_column('E:E', 4, cell_format=writer.book.add_format({'align': 'center','font_size': 9,})) # type: ignore
                worksheet.set_column('E:E', max(len(destino),14), cell_format=writer.book.add_format({'align': 'center', 'font_size': 9})) # type: ignore
                worksheet.set_column('F:F', max(len(manifiesto), 9), cell_format=writer.book.add_format({'align': 'center', 'font_size': 9})) # type: ignore
                worksheet.set_column('G:G', 10, cell_format=writer.book.add_format({'align': 'center', 'font_size': 9,'num_format': '"$"#,##0'})) # type: ignore
                worksheet.set_column('H:H', max(len(fecha), 15), cell_format=writer.book.add_format({'align': 'center', 'font_size': 9})) # type: ignore
                worksheet.set_column('I:I', 9, cell_format=writer.book.add_format({'align': 'center', 'font_size': 9, 'num_format': '"$"#,##0'})) # type: ignore
                
                num_rows_anexo = len(df_remesa)                
                cell_range_anexo = f'A3:I{num_rows_anexo+3}'
                # cell_range_anexo_1 = f'A3:J{num_rows_anexo+3}'
                worksheet.conditional_format(cell_range_anexo, {'type': 'no_blanks', 'format': writer.book.add_format({'border': 1})}) #type: ignore
                worksheet.conditional_format(cell_range_anexo, {'type': 'blanks', 'format': writer.book.add_format({'border': 1})}) #type: ignore
            
            if os.path.exists(file_path):
                file_name, file_extension = os.path.splitext(file_path)
                file_number = 1
                new_file = f"{file_name}_{file_number}{file_extension}"
                while os.path.exists(new_file):
                    file_number += 1
                    new_file = f"{file_name}_{file_number}{file_extension}"
                file = new_file
                os.rename(file_path, new_file)                  
                os.startfile(file)                       
                messagebox.showinfo("", f"Remesa {id_remesa} exportada con éxito")
            else :
                file = file_path
                os.startfile(file)
                messagebox.showinfo("", f"Remesa {id_remesa} exportada con éxito")


            os.startfile(file_path)
    def search_remesas_edit(id_remesa):
        if not id_remesa:
            messagebox.showerror("", "Ingrese un número de remesa")
            return
        try: #get the data of remesas from the database
            connection = sqlite3.connect(db_path)
            query = f'''
                        SELECT 
                            id_remesa, 
                            manifiesto, 
                            conductor, 
                            destino, 
                            fecha, 
                            total_uds, 
                            total_kg, 
                            total_vol, 
                            cobro_total, 
                            flete_coord_rtp, 
                            ingreso_operativo_total, 
                            gasto_operativo, 
                            utilidad, 
                            rentabilidad
                        FROM remesas 
                        WHERE id_remesa = '{id_remesa}';        
                    '''
            result = connection.execute(query)
            data = result.fetchall()
            if not data:
                messagebox.showerror("", "No se encontró la remesa")
                return
            connection.close()
            for row in data:
                enable_entries()
                clean_entries_remesa()
                entry_id_remesa.insert(0, row[0])
                entry_manifiesto.insert(0, row[1])
                entry_conductor.insert(0, row[2])
                entry_fecha.entry.insert(0, row[4])
                entry_total_uds.insert(0, row[5])
                entry_total_kg.insert(0, row[6])
                entry_total_volumen.insert(0, row[7]) 
                entry_cobro_total.insert(0, "{:,}".format(int(row[8]))) 
                entry_flete_coord_rtp.insert(0, "{:,}".format(row[9])) 
                entry_ingreso_operativo_total.insert(0, "{:,}".format(row[10])) 
                entry_gasto_operativo.insert(0, "{:,}".format(row[11])) 
                entry_utilidad.insert(0, "{:,}".format(row[12])) 
                entry_rentabilidad.insert(0, "{:.2f}".format(row[13])) 
                cbbx_destino_remesa.set(row[3])                
                # disable_entries()                
                
        except Exception as e:
            messagebox.showerror("", f"Error al buscar la remesa: {str(e)}")    
        
        try: #get the data of guias of every remesa from the database
            connection = sqlite3.connect(db_path)
            query = f'''                        
                   SELECT 
                        COALESCE(remesas_guias.guia_id, 'SIN GUIA') AS numero_guia,
                        COALESCE(guias.unidades, 0), 
                        COALESCE(guias.peso_Kg, 0), 
                        COALESCE(guias.volumen_m3, 0), 
                        COALESCE(guias.destino,  'SIN GUIA' ),
                        COALESCE(guias.fecha_de_asignacion,  'SIN GUIA'), 
                        COALESCE(remesas_guias.valor, 0),
                        COALESCE(guias.destinatario,  'SIN GUIA' ),
                        COALESCE((guias.balance_RCE + guias.balance_FCE), 0)

                    FROM 
                        remesas_guias
                    LEFT JOIN 
                        guias ON remesas_guias.guia_id = guias.numero_guia
                    WHERE 
                        remesas_guias.remesa_id = '{id_remesa}'
                    ORDER BY 
                        guias.fecha_insercion ASC;
                                              
                    '''
            result = connection.execute(query)
            data = result.fetchall()
            if not data:
                messagebox.showerror("", "No se encontraron guias")
                return
            clean_table_guias()
            clean_fields_guia()
            for row in data:
                row_list = list(row)
                row_list[6] = "{:,}".format(int(row_list[6]))
                row_list[8] = "{:,}".format(int(row_list[8]))
                
                if row_list[8] != 0:
                    # table_add_guia.insert("", "end", values=row, tags=("has_cobro",))  ENABLE THIS LINE TO ADD A COLOR TO THE ROW
                    table_add_guia.insert("", "end", values=row_list)
                else :
                    table_add_guia.insert("", "end", values=row_list)
                calc_total()
            calc_gans()
            # disable_entries()

        except Exception as e:
            messagebox.showerror("", f"Error al buscar la guia: {str(e)}")
    def update_remesa():
        id_remesa = entry_id_remesa.get()
        manifiesto = entry_manifiesto.get()
        conductor = entry_conductor.get()
        destino = cbbx_destino_remesa.get()
        fecha = entry_fecha.entry.get()
        total_kg = entry_total_kg.get()
        total_uds = entry_total_uds.get()
        flete_coord_rtp = (entry_flete_coord_rtp.get().replace(",", ""))
        ingreso_operativo_total = (entry_ingreso_operativo_total.get().replace(",", ""))
        gasto_operativo = (entry_gasto_operativo.get().replace(",", ""))
        utilidad = (entry_utilidad.get().replace(",", ""))
        rentabilidad = entry_rentabilidad.get()
        total_vol = entry_total_volumen.get()
        cobro_total = entry_cobro_total.get().replace(",", "")
        entry_id_remesa.state(["!readonly"])
        #HERE IS THE QUERY TO UPDATE THE REMESA ENTRIES
        connection = sqlite3.connect(db_path)
        try:
            query = f'''
                        UPDATE remesas
                        SET 
                        manifiesto = '{manifiesto}',
                        conductor = '{conductor}',
                        destino = '{destino}',
                        fecha= '{fecha}',
                        total_kg = '{total_kg}',
                        total_uds = '{total_uds}',
                        flete_coord_rtp = '{flete_coord_rtp}',
                        ingreso_operativo_total = '{ingreso_operativo_total}',
                        gasto_operativo = '{gasto_operativo}',
                        utilidad = '{utilidad}',
                        rentabilidad = '{rentabilidad}',                        
                        total_vol = '{total_vol}',
                        cobro_total = '{cobro_total}'
                        WHERE id_remesa = '{id_remesa}';                        
                    '''
            cursor = connection.cursor()
            cursor.execute(query)
        except Exception as e:
            messagebox.showerror("", f"Error al actualizar los datos de la remesa: {str(e)}") 
            connection.close()
       
        try:
            #create the list for update the values of the remesas_guias table
            rows_to_update = []
            for row in table_add_guia.get_children():
                row_values = list(table_add_guia.item(row)["values"])
                rows_to_update.append(row_values)
                
            cursor = connection.cursor()
            #create the query for the update 
            cursor.execute("DELETE FROM remesas_guias WHERE remesa_id = ?", (id_remesa,))
            for guia in rows_to_update:
                cursor.execute(f"INSERT INTO remesas_guias (remesa_id, guia_id, valor) VALUES ('{id_remesa}', '{guia[0]}', {guia[6].replace(',', '')}) ")
            connection.commit()
            connection.close()
            clean_table_remesas()
            list_remesas()
            # search_remesas_edit(id_remesa)
            
            messagebox.showinfo("", "Remesa actualizada con éxito")
        except Exception as e:
            messagebox.showerror("", f"Error al actualizar las guias: {str(e)}") 
            connection.close()

        connection.close()
    def get_latest_remesa():
        try:
            connection = sqlite3.connect(db_path)
            query = '''
                        SELECT id_remesa 
                        FROM remesas
                        ORDER BY 
                            SUBSTR(id_remesa, 1, INSTR(id_remesa, '-') - 1), 
                            CAST(SUBSTR(id_remesa, INSTR(id_remesa, '-') + 1) AS INTEGER)DESC
                        LIMIT 1
                    '''
            result = connection.execute(query)
            data = result.fetchone()
            connection.close()
            if not data:
                messagebox.showerror("", "No se encontraron remesas")
                return
            last_remesa = data[0]            
            prefix, num = last_remesa.split('-')            
            next_remesa = f"{prefix}-{int(num) + 1}"
            entry_id_remesa.delete(0, tk.END)
            entry_id_remesa.insert(0, next_remesa)
            

        except Exception as e:
            messagebox.showerror("", f"Error al obtener la remesa: {str(e)}")
            connection.close()
        finally:
            connection.close()

    for widget in frame.winfo_children():
        widget.grid_forget()
    
    tabs_remesas = ttk.Notebook(frame, bootstyle = 'secondary', width=width, height=height ) # type: ignore
    tabs_remesas.grid(row=0, column=0, sticky="wens")
    tabs_remesas.grid_propagate(False)
    tabs_remesas.columnconfigure(0, weight=1)
    tabs_remesas.rowconfigure(0, weight=1)

    frame_remesas = ttk.Frame(tabs_remesas)
    frame_remesas.grid(row=0, column=0, sticky="")
    frame_remesas.columnconfigure(0, weight=1)
    frame_remesas.rowconfigure(0, weight=1)
    
    frame_add_remesa = ttk.Frame(frame_remesas, )
    frame_add_remesa.grid(row=0, column=0, padx=10, pady=10, sticky="we")
    frame_add_remesa.columnconfigure(0, weight=1)
        
    frame_form_remesa = ttk.LabelFrame(frame_add_remesa, text="Datos de la Remesa")
    frame_form_remesa.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Configuración de filas y columnas para expandirse
    for i in range(5):
        frame_form_remesa.grid_rowconfigure(i, weight=1)
    for i in range(8):
        frame_form_remesa.grid_columnconfigure(i, weight=1)

    ttk.Label(frame_form_remesa, text="Remesa: (RTP)", anchor="e").grid(row=1, column=0, sticky="e", padx=10)
    entry_id_remesa = ttk.Entry(frame_form_remesa)
    entry_id_remesa.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_form_remesa, text="Manifiesto:", anchor="e").grid(row=1, column=2, sticky="e", padx=10)
    entry_manifiesto = ttk.Entry(frame_form_remesa)
    entry_manifiesto.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_form_remesa, text="Fecha:", anchor="e").grid(row=1, column=4, sticky="e", padx=10)
    entry_fecha = ttk.DateEntry(frame_form_remesa, dateformat='%d-%m-%Y' )
    entry_fecha.grid(row=1, column=5, padx=5, ipadx=15, pady=5, sticky="ew")

    ttk.Label(frame_form_remesa, text="Conductor:", anchor="e").grid(row=1, column=6, sticky="e", padx=10)
    entry_conductor = ttk.Entry(frame_form_remesa)
    entry_conductor.grid(row=1, column=7, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_form_remesa, text="Total Unidades:", anchor="e").grid(row=2, column=0, sticky="ew", padx=10)
    entry_total_uds = ttk.Entry(frame_form_remesa)
    entry_total_uds.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_form_remesa, text="Total Kg:", anchor="e").grid(row=2, column=2, sticky="ew", padx=10)
    entry_total_kg = ttk.Entry(frame_form_remesa)
    entry_total_kg.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_form_remesa, text="Total Vol:", anchor="e").grid(row=2, column=4, sticky="ew", padx=10)
    entry_total_volumen = ttk.Entry(frame_form_remesa)
    entry_total_volumen.grid(row=2, column=5, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_form_remesa, text="Cobro Total:", anchor="e").grid(row=2, column=6, sticky="ew", padx=10)
    entry_cobro_total = ttk.Entry(frame_form_remesa)
    entry_cobro_total.grid(row=2, column=7, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_form_remesa, text="Flete Coord RTP:", anchor="e").grid(row=3, column=0, sticky="ew", padx=10)
    entry_flete_coord_rtp = ttk.Entry(frame_form_remesa)
    entry_flete_coord_rtp.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_form_remesa, text="Ingreso Op. Total:", anchor="e").grid(row=3, column=2, sticky="ew", padx=10)
    entry_ingreso_operativo_total = ttk.Entry(frame_form_remesa)
    entry_ingreso_operativo_total.grid(row=3, column=3, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_form_remesa, text="Gasto Operativo:", anchor="e").grid(row=3, column=4, sticky="ew", padx=10)
    entry_gasto_operativo = ttk.Entry(frame_form_remesa)
    entry_gasto_operativo.grid(row=3, column=5, padx=5, pady=5, sticky="ew")
    entry_gasto_operativo.bind("<KeyRelease>", lambda event: calc_gans())

    ttk.Label(frame_form_remesa, text="Utilidad:", anchor="e").grid(row=3, column=6, sticky="ew", padx=10)
    entry_utilidad = ttk.Entry(frame_form_remesa)
    entry_utilidad.grid(row=3, column=7, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_form_remesa, text="Rentabilidad:", anchor="e").grid(row=4, column=0, sticky="ew", padx=10)
    entry_rentabilidad = ttk.Entry(frame_form_remesa)
    entry_rentabilidad.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
    entry_rentabilidad.bind("<KeyRelease>", lambda event: calc_gans())

    destinos_db = get_destinos_db()
    ttk.Label(frame_form_remesa, text="Destino:", anchor="e").grid(row=4, column=2, sticky="ew", padx=10)
    cbbx_destino_remesa = ttk.Combobox(frame_form_remesa, values=destinos_db, state="readonly")
    cbbx_destino_remesa.grid(row=4, column=3, padx=5, pady=5, sticky="ew")
    
    list_camps = ("Numero Guia", "Unidades", "Peso Kg", "Volumen M3", "Destino", "Fecha de Asignacion",  "Valor", "Cliente", "Balance Cobro")
    
    frame_add_guia = ttk.Frame(frame_add_remesa, )
    frame_add_guia.grid(row=3, column=0, padx=10, pady=10, sticky="nswe")
    frame_add_guia.columnconfigure(0, weight=1)
    
    table_add_guia = ttks.Treeview(frame_add_guia, columns=list_camps, show="headings", height=20)
    table_add_guia.grid(row=3, column=0, columnspan=2, sticky="we",)

    table_add_guia.bind("<Double-Button-1>", double_click_guia)
    table_add_guia.bind("<Delete>", lambda event: delete_row())
    
    for i in list_camps:
        table_add_guia.heading(i, text=i)
        table_add_guia.column(i, width=100, anchor="center", stretch=True)
   
    vscrollbar = ttk.Scrollbar(frame_add_guia, bootstyle = 'primary-round', orient="vertical", command=table_add_guia.yview) # type: ignore
    vscrollbar.grid(row=3, column=3, sticky="ns", ) 
    table_add_guia.configure(yscrollcommand=vscrollbar.set)
    
    # if the balance is != 0, the row will be colored in yellow
    table_add_guia.tag_configure("has_cobro", background=colors.bg_has_cobro)
    table_add_guia.column("#0", width=0, stretch=False, anchor="center")
    
    #*  FRAME GUIAS!!!!

    # # Crear y ubicar los widgets para cada elemento de la tabla
    frame_guia = ttk.Frame(frame_add_remesa, )
    frame_guia.grid(row=2, column=0,  padx=(10, 0), sticky="")

    ttk.Label(frame_guia, text="Guia:").grid(row=0, column=0, padx=10,)
    entry_guia = ttk.Entry(frame_guia, width=15, justify="center")
    entry_guia.grid(row=1, column=0,)
    
    ttk.Button(frame_guia, text="  ➡️" , command= lambda: get_info_guia(entry_guia.get().strip()), width=4).grid(row=1, column=1, padx=(5,0), ipady=1, sticky='w')
    entry_guia.bind("<Return>", lambda event: add_guia_to_remesa())
    
    ttk.Label(frame_guia, text="Uds:").grid(row=0, column=2, padx=5,)
    entry_unidades = ttk.Entry(frame_guia, width=8, justify="center", state="readonly")
    entry_unidades.grid(row=1, column=2, padx=5,)

    ttk.Label(frame_guia, text="Peso (Kg):").grid(row=0, column=3, padx=5,)
    entry_peso = ttk.Entry(frame_guia, width=8, justify="center", state="readonly" )
    entry_peso.grid(row=1, column=3, padx=5,)
      
    ttk.Label(frame_guia, text="Volumen (M3):").grid(row=0, column=4, padx=5,)
    entry_volumen = ttk.Entry(frame_guia, width=8, justify="center", state="readonly" )
    entry_volumen.grid(row=1, column=4, padx=5,)

    ttk.Label(frame_guia, text="Destino:").grid(row=0, column=5, padx=5,)
    entry_destino = ttk.Entry(frame_guia, width= 20, justify="center", state="readonly" )
    entry_destino.grid(row=1, column=5, padx=5,)

    ttk.Label(frame_guia, text="Fecha de Asignacion:").grid(row=0, column=6, padx=5,)
    entry_fecha_asignacion = ttk.Entry(frame_guia, width=12, justify="center", state="readonly" )
    entry_fecha_asignacion.grid(row=1, column=6, padx=5,)

    ttk.Label(frame_guia, text="Cliente:").grid(row=0, column=7, padx=5,)
    entry_cliente = ttk.Entry(frame_guia, width=60, justify="center", state="readonly" )
    entry_cliente.grid(row=1, column=7, padx=5,)

    ttk.Label(frame_guia, text="Valor:").grid(row=0, column=8, padx=5,)
    entry_valor = ttk.Entry(frame_guia, justify="center")
    entry_valor.bind("<Return>", lambda event: add_guia_to_remesa())
    entry_valor.grid(row=1, column=8, padx=5,)

    ttk.Label(frame_guia, text="Balance Cobro:").grid(row=0, column=9, padx=5,)
    entry_balance_cobro = ttk.Entry(frame_guia, width=10, justify="center", state="readonly")
    entry_balance_cobro.grid(row=1, column=9, padx=5,  )

    ttk.Button(frame_guia, text="✅", width=4, command= lambda: add_guia_to_remesa()).grid(row=1, column=10, padx=5, pady=5, )    
    ttk.Button(frame_guia, text="❌", width=4, command= lambda: delete_row()).grid(row=1, column=11, padx=5, pady=5,)
    
    #FRAME BUTTONS
    frame_buttons = ttk.Frame(frame_add_remesa, )
    frame_buttons.grid(row=4, column=0, columnspan=10, padx=(10, 0), pady=10, sticky="we")
    
    btn_import_remesa = ttk.Button(frame_buttons, text="Importar Remesa", command= lambda: import_remesa_from_app())
    btn_import_remesa.grid(row=4, column=0, sticky='w', padx=(0,5), pady=10)
    
    btn_export_remesa = ttk.Button(frame_buttons, text="Exportar Remesa Cond", command= lambda: export_remesa())
    btn_export_remesa.grid(row=4, column=1, sticky='w', padx=5, pady=10)
    
    btn_nueva_remesa = ttk.Button(frame_buttons, text="Nueva Remesa", command= lambda: new_remesa())
    btn_nueva_remesa.grid(row=4, column=2, sticky='w', padx=5, pady=10)
    
    frame_btn_edit_remesa = ttk.LabelFrame(frame_buttons, text="Editar Remesa",)
    frame_btn_edit_remesa.grid(row=4, column=3, sticky='e', padx=(20,5))
    
    entry_editar_remesa = ttk.Entry(frame_btn_edit_remesa, width=20, justify='center')
    entry_editar_remesa.grid(row=4, column=5, sticky='e', padx=5, pady=10)
    entry_editar_remesa.bind("<Return>", lambda event: search_remesas_edit(entry_editar_remesa.get().strip()))
    
    btn_search = ttk.Button(frame_btn_edit_remesa, text="Buscar", command= lambda: search_remesas_edit(entry_editar_remesa.get().upper().strip()))
    btn_search.grid(row=4, column=6, sticky='e', padx=5, pady=10)
    
    btn_actualizar_remesa = ttk.Button(frame_btn_edit_remesa, text="Actualizar", command= lambda: update_remesa())
    btn_actualizar_remesa.grid(row=4, column=7, sticky='e', padx=5, pady=10)    
    
    btn_guardar = ttk.Button(frame_remesas, text="Guardar Remesa", command= lambda: save_remesa())
    btn_guardar.grid(row=5, column=0, sticky='s', padx=25, pady=10, )
    
    calc_total()
    tabs_remesas.add(frame_remesas, text="Agregar Remesa")        
    
    #******************************************** FRAME TAB SEARCH REMESA******************************************************** #
    #******************************************** FRAME TAB SEARCH REMESA******************************************************** #
    #******************************************** FRAME TAB SEARCH REMESA******************************************************** #
    
    def on_double_click(event):
        item = event.widget.selection()[0]        
        id_remesa = event.widget.item(item)['values'][0]
        entrysearch_remesa.delete(0, tk.END)
        entrysearch_remesa.insert(0, id_remesa)
        entry_export_remesa_factura.delete(0, tk.END)
        entry_export_remesa_factura.insert(0, id_remesa)
        search_remesa(id_remesa)
        search_guias_remesa(id_remesa)
    def search_guias_remesa(id_remesa):
        if not id_remesa:
            messagebox.showerror("", "Ingrese un número de remesa")
            return
        try:
            connection = sqlite3.connect(db_path)
            query = f'''
                        WITH ranked_results AS (
                                SELECT
                                    COALESCE (remesas_guias.guia_id, 'SIN GUIA') AS guia_id,
                                    COALESCE (guias.estado, 'SIN GUIA') AS estado,
                                    COALESCE (guias.destinatario, 'SIN GUIA') AS destinatario,
                                    COALESCE (guias.destino, 'SIN GUIA') AS destino,
                                    COALESCE (guias.unidades, 'SIN GUIA') AS unidades,
                                    COALESCE (guias.peso_Kg, 'SIN GUIA') AS peso_Kg,
                                    COALESCE (guias.volumen_m3, 'SIN GUIA') AS volumen_m3,
                                    COALESCE (remesas_guias.valor, 'SIN GUIA') AS valor,
                                    COALESCE (guias.fecha_de_asignacion, 'SIN GUIA') AS fecha_de_asignacion,
                                    COALESCE (anexos_guias.anexo_id, 'SIN ANEXO') AS en_anexo,
                                    COALESCE (facturas_guias.factura_id, 'SIN FACT.') AS en_factura,
                                    ROW_NUMBER() OVER (
                                        PARTITION BY remesas_guias.guia_id 
                                        ORDER BY 
                                            SUBSTR(anexos_guias.guia_id, 1, INSTR(anexos_guias.guia_id, '-') - 1), 
                                            CAST(SUBSTR(anexos_guias.guia_id, INSTR(anexos_guias.guia_id, '-') + 1) AS INTEGER)
                                    ) AS rn
                                FROM 
                                    remesas_guias
                                LEFT JOIN 
                                    guias ON remesas_guias.guia_id = guias.numero_guia
                                LEFT JOIN 
                                    anexos_guias ON guias.numero_guia = anexos_guias.guia_id
                                LEFT JOIN 
                                    facturas_guias ON guias.numero_guia = facturas_guias.guia_id
                                WHERE 
                                    remesas_guias.remesa_id = '{id_remesa}'
                            )
                            SELECT
                                guia_id,
                                estado,
                                destinatario,
                                destino,
                                unidades,
                                peso_Kg,
                                volumen_m3,
                                valor,
                                fecha_de_asignacion,
                                en_anexo,
                                en_factura
                            FROM
                                ranked_results
                            WHERE
                                rn = 1
                            ORDER BY
                                SUBSTR(guia_id, 1, INSTR(guia_id, '-') - 1), 
                                CAST(SUBSTR(guia_id, INSTR(guia_id, '-') + 1) AS INTEGER);
                        '''
            result = connection.execute(query)
            if result is None:
                messagebox.showerror("", "No se encontraron guias")
                return            
            data = result.fetchall()
            table_list_remesas.focus_set()
                     
            table_list_guias.delete(*table_list_guias.get_children())      
            connection.close()       
            for row in data:
                row_list = list(row)
                row_list[7] = "{:,}".format(int(row_list[7]))

                if row_list[10] != 'SIN FACT.':
                    # table_list_guias.insert("", "end", values=row_list, tags=("paid_invoice",))  ENABLE THIS LINE TO ADD A COLOR TO THE ROW
                    table_list_guias.insert("", "end", values=row_list)
                else: 
                    # table_list_guias.insert("", "end", values=row_list, tags=("pend_invoice",) )  ENABLE THIS LINE TO ADD A COLOR TO THE ROW
                    table_list_guias.insert("", "end", values=row_list )   
            connection.close()
        except Exception as e:
            messagebox.showerror("", f"Error al buscar la remesa: {str(e)}")
        finally:
            connection.close()
    def btnsearch_remesa(id_remesa):        
        if id_remesa:
            search_remesa(id_remesa)
            search_guias_remesa(id_remesa)               
        else:
            messagebox.showerror("Error", "Por favor, ingrese un ID de remesa")    
    def search_remesa(id_remesa):  
        #function to enable entries for editing  
        entries = [entryid_remesa, entrymanifiesto, entryconductor, entrydestino, entryfecha, entrytotal_kg, entrytotal_uds, entrytotal_volumen, entryflete_coord_rtp, entryingreso_operativo_total, entrygasto_operativo, entryutilidad, entryrentabilidad]
        
        def entries_state_enabled():               
            for entry in entries:
                entry.state(["!readonly"])
        
        def entries_state_disabled():
            for entry in entries:
                entry.state(["readonly"])    
        
        def entries_state_clear():
            for entry in entries:
                entry.delete(0, tk.END)
        
        connection = sqlite3.connect(db_path)
        
        query = f'''
                    SELECT DISTINCT r.id_remesa,
                    r.manifiesto, r.conductor, 
                    d.destino, r.fecha, r.total_kg, 
                    r.total_uds, total_vol, r.flete_coord_rtp, r.ingreso_operativo_total, 
                    r. gasto_operativo, r.utilidad, r.rentabilidad 
                    FROM remesas AS r JOIN destinos  AS d ON d.destino = r.destino 
                    WHERE id_remesa = '{id_remesa}';       
                    '''
        result = connection.execute(query)
        data = result.fetchall() 
        connection.close()                
       
        btn_delete_remesa = ttk.Button(frame_search_single_remesa, text="Eliminar", style='Danger',command= lambda: delete_remesa(entryid_remesa.get()) )
        btn_delete_remesa.grid(row=1, column=5, sticky="w", padx=5, )            
    
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
        entryflete_coord_rtp.insert(0, "{:,}".format(data[0][8]))
        entryingreso_operativo_total.insert(0, "{:,}".format(data[0][9]))
        entrygasto_operativo.insert(0, "{:,}".format(data[0][10]))
        entryutilidad.insert(0,"{:,}".format(data[0][11]))
        entryrentabilidad.insert(0,str(data[0][12]))
        entries_state_disabled()

        list_guias = table_list_guias.get_children()
        for item in list_guias:
            if table_list_guias.item(item, "values")[0] == id_remesa:
                table_list_guias.selection_set(item)                    
                table_list_guias.see(item)
    def export_remesa_to_factura(id_remesa):
        remesa, manifiesto, conductor, fecha = '', '', '', ''
        total_kg, total_uds, ingreso_operativo_total, cobro_total = 0,0,0,0
        
        if not id_remesa:
            messagebox.showerror("", "Ingrese un número de remesa")
            return        
        
        try:
            connection = sqlite3.connect(db_path)
            query_header = f''' 
                                SELECT id_remesa, manifiesto, conductor, fecha, total_kg, total_uds, ingreso_operativo_total, cobro_total 
                                FROM remesas
                                WHERE id_remesa = '{id_remesa}';
                                '''
            result_header = connection.execute(query_header)
            data_header = result_header.fetchall()
            for row in data_header:
                remesa = row[0]
                manifiesto = row[1]
                conductor = row[2]
                fecha = row[3]
                total_kg = row[4]
                total_uds = row[5]
                ingreso_operativo_total = row[6]
                cobro_total = row[7]
                
                
            if not data_header:
                messagebox.showerror("", "No se encontró la remesa")
                return
           

            query = f'''
                        SELECT 
                            Guia,
                            Cant,
                            Kg,
                            Destino,
                            [Fe. Recep],
                            Valor,
                            Cobro,
                            Anexo,
                            Factura
                        FROM (
                            SELECT 
                                COALESCE(remesas_guias.guia_id, '') AS 'Guia',
                                COALESCE(guias.unidades, '0') AS 'Cant',
                                COALESCE(guias.peso_Kg, '0') AS 'Kg',
                                COALESCE(guias.destino, 'SIN GUIA') AS 'Destino',
                                COALESCE(guias.fecha_de_asignacion, '') AS 'Fe. Recep',
                                COALESCE(anexos_guias.valor, '0') AS 'Valor',
                                COALESCE((guias.balance_FCE + guias.balance_RCE), '0') AS 'Cobro',
                                COALESCE(anexos_guias.anexo_id, '') AS 'Anexo',
                                COALESCE(facturas_guias.factura_id, '') AS 'Factura',
                                ROW_NUMBER() OVER (PARTITION BY remesas_guias.guia_id ORDER BY remesas_guias.guia_id) AS RowNum
                            FROM 
                                remesas_guias
                            LEFT JOIN 
                                anexos_guias ON anexos_guias.guia_id = remesas_guias.guia_id
                            LEFT JOIN 
                                guias ON remesas_guias.guia_id = guias.numero_guia
                            LEFT JOIN 
                                facturas_guias ON guias.numero_guia = facturas_guias.guia_id
                            WHERE remesas_guias.remesa_id = '{id_remesa}'
                        ) AS Subquery
                        WHERE RowNum = 1;

                      '''
            result = connection.execute(query)
            data = result.fetchall()
            if not data:
                messagebox.showerror("", "No se encontraron guias")
                return
            
            file_location = config['remesas_path'] # type: ignore
            file_name = f"{id_remesa}.xlsx"
            file_path = os.path.join(file_location, file_name)
            if not os.path.exists(file_location):
                os.makedirs(file_location)
            
            df = pd.DataFrame(data, columns=["Guia", "Cant", "Kg", "Destino", "Fe. Recep", "Valor", "Cobro", "Anexo", "Factura"])
            df.insert(0, "No", range(1, len(df) + 1))
            df['Cant'] = df['Cant'].astype(int)
            df['Kg'] = df['Kg'].astype(int)
            df['Valor'] = df['Valor'].astype(int)
            df['Cobro'] = df['Cobro'].astype(int)
            with ExcelWriter(file_path, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Hoja1', index=False, startrow=2)
    
                worksheet = writer.sheets['Hoja1']
                worksheet.merge_range('A1:J1', 'RELACION REMISIONES ENTREGADAS AL CONDUCTOR.', writer.book.add_format({'bold': True, 'font_size': 12, 'align': 'center', 'border':1, 'bg_color': colors.bg_relaciones_conductor})) #type: ignore
                worksheet.merge_range('A2:D2', f'COND: {conductor}', writer.book.add_format({'bold': True, 'font_size': 11, 'align': 'center', 'border':1 })) #type: ignore
                
                worksheet.write('E2:E2', f'{remesa}', writer.book.add_format({'bold': True, 'font_size': 11, 'align': 'center', 'border':1 })) #type: ignore
                
                worksheet.merge_range('F2:G2', f'{manifiesto}', writer.book.add_format({'bold': True, 'font_size': 11, 'align': 'center', 'border':1 })) #type: ignore
                worksheet.write('H2:H2', 'Fecha', writer.book.add_format({'bold': True, 'font_size': 11, 'align': 'center', 'border':1 })) #type: ignore
                worksheet.merge_range('I2:J2', f'{fecha}', writer.book.add_format({'bold': True, 'font_size': 11, 'align': 'center', 'border':1 })) #type: ignore
                
                worksheet.set_column('A:A', 3, writer.book.add_format({'align': 'center', 'font_size': 9})) # type: ignore
                worksheet.set_column('B:B', 10, writer.book.add_format({'align': 'center', 'font_size': 9})) # type: ignore
                worksheet.set_column('C:C', 5, writer.book.add_format({'align': 'center', 'font_size': 9, 'num_format': '0'})) # type: ignore
                worksheet.set_column('D:D', 5, writer.book.add_format({'align': 'center', 'font_size': 9, 'num_format': '0'})) # type: ignore
                worksheet.set_column('E:E', 15, writer.book.add_format({'align': 'center', 'font_size': 9})) # type: ignore
                worksheet.set_column('F:F', 9, writer.book.add_format({'align': 'center', 'font_size': 9})) # type: ignore
                worksheet.set_column('G:H', 10, writer.book.add_format({'align': 'center', 'num_format': '"$"#,##0', 'font_size': 9})) # type: ignore                    
                worksheet.set_column('I:J', 7, writer.book.add_format({'align': 'center', 'num_format': '"$"#,##0', 'font_size': 9})) # type: ignore
                
                total_uds = df['Cant'].sum()
                total_kg = df['Kg'].sum()
                total_valor = df['Valor'].sum()
                cobro_total = df['Cobro'].sum()

                worksheet.write(len(df) + 3, 1, 'TOTAL', writer.book.add_format({'bold': True, 'align': 'center', 'border':1})) #type: ignore
                worksheet.write(len(df) + 3, 2, total_uds, writer.book.add_format({'bold': True, 'align': 'center', 'border':1, 'num_format': '0'})) #type: ignore
                worksheet.write(len(df) + 3, 3, total_kg, writer.book.add_format({'bold': True, 'align': 'center', 'border':1, 'num_format': '0'})) #type: ignore
                worksheet.write(len(df) + 3, 6, total_valor, writer.book.add_format({'bold': True, 'align': 'center', 'border':1, 'num_format': '"$"#,##0'})) #type: ignore
                worksheet.write(len(df) + 3, 7, cobro_total, writer.book.add_format({'bold': True, 'align': 'center', 'border':1, 'num_format': '"$"#,##0'})) #type: ignore
                
                num_rows_anexo = len(df)                
                cell_range_anexo = f'A3:J{num_rows_anexo+4}'
                cell_range_anexo_1 = f'A3:J{num_rows_anexo+3}'
                worksheet.conditional_format(cell_range_anexo, {'type': 'no_blanks', 'format': writer.book.add_format({'border': 1})}) #type: ignore
                worksheet.conditional_format(cell_range_anexo, {'type': 'blanks', 'format': writer.book.add_format({'border': 1})}) #type: ignore
                worksheet.conditional_format(cell_range_anexo_1, {'type': 'text', 'criteria': 'containing','value': 'SIN GUIA','format': writer.book.add_format({'bg_color': colors.bg_cell_error})})#type: ignore
                
               
                worksheet.merge_range('L2:N2', "INGRESO FTE TOTAL:", writer.book.add_format({'align': 'left', 'border': '1', 'bold':True })) # type: ignore
                worksheet.write('O2', int(entryingreso_operativo_total.get().replace(",", "")), writer.book.add_format({'align': 'center', 'num_format': '"$"#,##0',  'border': '1', 'bold':True})) #type: ignore

                worksheet.merge_range('L3:N3', "GASTO OPERATIVO:", writer.book.add_format({'align': 'left',  'border': '1', 'bold': True })) # type: ignore
                worksheet.write('O3', int(entrygasto_operativo.get().replace(",", "")), writer.book.add_format({'align': 'center', 'num_format': '"$"#,##0', 'border': '1', 'bold':True})) #type: ignore

                worksheet.merge_range('L4:N4', "UTILIDAD DE LA OPERACION:", writer.book.add_format({'align': 'left',  'border': '1', 'bold':True})) # type: ignore
                worksheet.write('O4', int(entryutilidad.get().replace(",", "")), writer.book.add_format({'align': 'center', 'num_format': '"$"#,##0',  'border': '1', 'bold':True})) #type: ignore

                worksheet.merge_range('L5:N5', "RENTABILIDAD:", writer.book.add_format({'align': 'left',  'border': '1', 'bold':True})) # type: ignore
                worksheet.write('O5', float(entryrentabilidad.get())/100, writer.book.add_format({'align': 'center', 'num_format': '0.00%',  'border': '1', 'bold':True })) #type: ignore 
                                                               
            if os.path.exists(file_path):
                file_name, file_extension = os.path.splitext(file_path)
                file_number = 1
                new_file = f"{file_name}_{file_number}{file_extension}"
                while os.path.exists(new_file):
                    file_number += 1
                    new_file = f"{file_name}_{file_number}{file_extension}"
                file = new_file
                os.rename(file_path, new_file)                  
                os.startfile(file)                       
                messagebox.showinfo("", f"Remesa {id_remesa} exportada con éxito")
            else :
                file = file_path
                os.startfile(file)
                messagebox.showinfo("", f"Remesa {id_remesa} exportada con éxito")
            connection.close()
        except Exception as e:
            messagebox.showerror("", f"Error al exportar la remesa: {str(e)}")  
        finally:
            connection.close()

    #********** TABLE LIST  REMESAS **********#
    #********** TABLE LIST  REMESAS **********#
    
    frame_search_remesa = ttk.Frame(tabs_remesas)
    frame_search_remesa.grid(row=0, column=0, padx=10, sticky="nsew" )
    frame_search_remesa.grid_columnconfigure(0, weight=1)
    for i in range(3):
        frame_search_remesa.grid_rowconfigure(i, weight=1)  

    entry_cols = ("Id Remesa", "Manifiesto", "Destino", "Conductor", "Fecha", "Ingreso Operativo Total", "Rentabilidad", "Total Guias", "Guias Facturadas", "Guias Sin Facturar")
    
    frame_table_remesas = ttk.Frame(frame_search_remesa, )
    frame_table_remesas.grid(row=0, column=0, padx=0, pady=20, sticky="wens")
    frame_table_remesas.grid_columnconfigure(0, weight=1)
    frame_table_remesas.grid_rowconfigure(0, weight=1)
    table_list_remesas = ttk.Treeview(frame_table_remesas, columns= entry_cols, )    
    table_list_remesas.heading("Id Remesa", text="Remesa")
    table_list_remesas.heading("Manifiesto", text="Manifiesto")
    table_list_remesas.heading("Destino", text="Destino")
    table_list_remesas.heading("Conductor", text="Conductor")
    table_list_remesas.heading("Fecha", text="Fecha")
    table_list_remesas.heading("Ingreso Operativo Total", text="Ing. Op. Total")
    table_list_remesas.heading("Rentabilidad", text="Rent.")
    table_list_remesas.heading("Total Guias", text="T.Guias")
    table_list_remesas.heading("Guias Facturadas", text="G. Facturadas")
    table_list_remesas.heading("Guias Sin Facturar", text="G. Pendientes")  
    table_list_remesas.grid(row=0, column=0, columnspan=2, sticky="wnse")
    table_list_remesas.bind("<Delete>", lambda event: delete_remesa(table_list_remesas.item(table_list_remesas.selection()[0], 'values')[0]))

    
    for i in entry_cols:
        table_list_remesas.heading(i, text=i)
        table_list_remesas.column(i, width=100, anchor="center", stretch=True)
    table_list_remesas.column("#0", width=0, stretch=False, anchor="center")
    table_list_remesas.bind("<ButtonRelease-1>", on_double_click)    
    vscrollbar1 = ttk.Scrollbar(frame_table_remesas, bootstyle = 'primary-round', orient="vertical", command=table_list_remesas.yview,) # type: ignore
    vscrollbar1.grid(row=0, column=3, sticky="ns", ) 
    table_list_remesas.configure(yscrollcommand=vscrollbar1.set)
    
    #***********ENTRIES REMESA***********#
    #***********ENTRIES REMESA***********#
    
    frame_edit_remesa = ttk.Frame(frame_search_remesa)
    frame_edit_remesa.grid(row=2, column=0, sticky="ns")            
    
    frame_search_single_remesa = ttk.Frame(frame_search_remesa,)
    frame_search_single_remesa.grid(row=1, column=0, pady=20,  sticky="ns")  

    btn_search_remesa = ttk.Button(frame_search_single_remesa, text="Buscar Remesa", command=lambda: btnsearch_remesa(entrysearch_remesa.get()))
    btn_search_remesa.grid(row=1, column=0, padx=10, sticky="w",  )    
    
    entrysearch_remesa = ttk.Entry(frame_search_single_remesa, justify="center")
    entrysearch_remesa.grid(row=1, column=1,  )
    entrysearch_remesa.bind("<Return>", lambda event: btnsearch_remesa(entrysearch_remesa.get()))
    
    ttk.Label(frame_edit_remesa, text="ID Remesa:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    entryid_remesa = ttk.Entry(frame_edit_remesa)
    entryid_remesa.grid(row=0, column=1,  pady=5)
    entryid_remesa.state(["readonly"])
    
    ttk.Label(frame_edit_remesa, text="Manifiesto:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
    entrymanifiesto = ttk.Entry(frame_edit_remesa)
    entrymanifiesto.grid(row=0, column=3,  pady=5)
    entrymanifiesto.state(["readonly"])
    
    ttk.Label(frame_edit_remesa, text="Conductor:").grid(row=0, column=4, sticky="w", padx=5, pady=5)
    entryconductor = ttk.Entry(frame_edit_remesa)
    entryconductor.grid(row=0, column=5,  pady=5)        
    entryconductor.state(['readonly'])
    
    ttk.Label(frame_edit_remesa, text="Destino:").grid(row=0, column=6, sticky="w", padx=5, pady=5)
    entrydestino = ttk.Entry(frame_edit_remesa, state="readonly")
    entrydestino.grid(row=0, column=7,  pady=5)        
    
    ttk.Label(frame_edit_remesa, text="Fecha:").grid(row=0, column=8, sticky="w", padx=5, pady=5)
    entryfecha = ttk.Entry(frame_edit_remesa)
    entryfecha.grid(row=0, column=9,  pady=5)        
    entryfecha.state(['readonly'])
    
    ttk.Label(frame_edit_remesa, text="Total Kg:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    entrytotal_kg = ttk.Entry(frame_edit_remesa)
    entrytotal_kg.grid(row=1, column=1,  pady=5)        
    entrytotal_kg.state(['readonly'])
    
    ttk.Label(frame_edit_remesa, text="Total Uds:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
    entrytotal_uds = ttk.Entry(frame_edit_remesa)
    entrytotal_uds.grid(row=1, column=3,  pady=5)        
    entrytotal_uds.state(['readonly'])
    
    ttk.Label(frame_edit_remesa, text="Total Volumen:").grid(row=1, column=4, sticky="w", padx=5, pady=5)
    entrytotal_volumen = ttk.Entry(frame_edit_remesa)
    entrytotal_volumen.grid(row=1, column=5,  pady=5)        
    entrytotal_volumen.state(['readonly'])
    
    ttk.Label(frame_edit_remesa, text="Flete Coord RTP:").grid(row=1, column=6, sticky="w", padx=5, pady=5)
    entryflete_coord_rtp = ttk.Entry(frame_edit_remesa)
    entryflete_coord_rtp.grid(row=1, column=7,  pady=5)        
    entryflete_coord_rtp.state(['readonly'])
    
    ttk.Label(frame_edit_remesa, text="Ingreso Op. Total:").grid(row=1, column=8, sticky="w", padx=5, pady=5)
    entryingreso_operativo_total = ttk.Entry(frame_edit_remesa)
    entryingreso_operativo_total.grid(row=1, column=9,  pady=5)        
    entryingreso_operativo_total.state(['readonly'])
    
    ttk.Label(frame_edit_remesa, text="Gasto Operativo:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    entrygasto_operativo = ttk.Entry(frame_edit_remesa)
    entrygasto_operativo.grid(row=2, column=1,  pady=5)        
    entrygasto_operativo.state(['readonly'])
    
    ttk.Label(frame_edit_remesa, text="Utilidad:").grid(row=2, column=2, sticky="w", padx=5, pady=5)
    entryutilidad = ttk.Entry(frame_edit_remesa)
    entryutilidad.state(['readonly'])
    entryutilidad.grid(row=2, column=3,  pady=5)        
    
    ttk.Label(frame_edit_remesa, text="Rentabilidad:").grid(row=2, column=4, sticky="w", padx=5, pady=5)
    entryrentabilidad = ttk.Entry(frame_edit_remesa)
    entryrentabilidad.grid(row=2, column=5,  pady=5)        
    entryrentabilidad.state(['readonly'])      
    
    #***********TABLE LIST GUIAS-REMESA***********#
    #***********TABLE LIST GUIAS-REMESA***********#    
    
    frame_search = ttk.LabelFrame(frame_search_remesa,  )
    frame_search.grid(row=3, column=0, padx=10, pady=10, sticky="ns" )
    
    list_camps = ("Numero Guia", "Estado", "Destinatario", "Destino", "Unidades", "Peso Kg", "Volumen M3", "Valor","Fecha de Asignacion", "En Anexo", "En Factura")
    
    frame_table_list_guias = ttk.Frame(frame_search_remesa, )
    frame_table_list_guias.grid(row=3, column=0, padx=0, pady=10, sticky="we")
    frame_table_list_guias.grid_columnconfigure(0, weight=1)
    
    table_list_guias = ttk.Treeview(frame_table_list_guias, columns=list_camps, height=15)
    table_list_guias.grid(row=0, column=0,  columnspan=2,sticky="we")
    
    table_list_guias.tag_configure("paid_invoice", background="#cff6c8")
    table_list_guias.tag_configure("pend_invoice", background="#fefda6")   
    
    for col in list_camps:
        table_list_guias.heading(col, text=col)
        table_list_guias.column(col, width=100, stretch=True, anchor="center")    
    table_list_guias.column("#0", width=0, stretch=False, anchor="center")    
    
    vscrollbar2 = ttk.Scrollbar(frame_table_list_guias, bootstyle = 'primary-round', orient="vertical", command=table_list_guias.yview) # type: ignore
    vscrollbar2.grid(row=0, column=3, sticky="ns")
    table_list_guias.configure(yscrollcommand=vscrollbar2.set)    
    
    hscrollbar2 = ttk.Scrollbar(frame_table_list_guias, bootstyle = 'primary-round', orient="horizontal", command=table_list_guias.xview) # type: ignore
    hscrollbar2.grid(row=1, column=0, columnspan=2, sticky="we")
    table_list_guias.configure(xscrollcommand=hscrollbar2.set)
        
    entry_export_remesa_factura = ttk.Entry(frame_search_single_remesa)
    entry_export_remesa_factura.grid(row=1, column=6, padx=5, pady=5, )
    btn_export_remesa_factura = ttk.Button(frame_search_single_remesa, text="Exportar Remesa Int", command= lambda: export_remesa_to_factura(entry_export_remesa_factura.get().strip()) )
    btn_export_remesa_factura.grid(row=1, column=5, padx=(140,5), pady=5)
    
    tabs_remesas.add(frame_search_remesa, text="Buscar Remesa")
    focus_tab(tabs_remesas)
    list_remesas()
    get_latest_remesa()
    