import os
import pandas as pd
import pdfplumber
import tkinter as tk
import PyPDF2
import re
import sqlite3
from pandas import ExcelWriter

from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry

from config import load_config
import pandas as pd
import os
import pandas as pd
import os
import xlsxwriter



def _convert_stringval(value):
    if hasattr(value, 'typename'):
        value = str(value)
        try:
            value = int(value)
        except (ValueError, TypeError):
            pass
    return value
ttk._convert_stringval = _convert_stringval # type: ignore

num =1
def show_facturacion(frame):
    config = load_config()
    db_path = config['db_path'] 
    
    for widget in frame.winfo_children():
        widget.grid_forget()
    
    anexos_list_summary = {}
    def clean_entries_factura():
        entry_id_factura.delete(0, 'end')
        entry_cliente.delete(0, 'end')
        entry_agregar_guia.delete(0, 'end')
        entry_agregar_anexo.delete(0, 'end')
        entry_borrar_anexo.delete(0, 'end')
        entry_total_factura.delete(0, 'end')
    
    def clean_treeview_summary_anexos():
        for item in treeview_summary_anexos.get_children():
            treeview_summary_anexos.delete(item)
    
    def print_summary_anexos():
        for anexo in anexos_list_summary:
            treeview_summary_anexos.insert('', 'end', values=(anexo, anexos_list_summary[anexo]['guias'], anexos_list_summary[anexo]['valor']))
    
    def enumerate_rows(treeview):
        for i, item in enumerate(treeview.get_children(''), 1):
                treeview.set(item, 0, i)  
    
    def get_anexos():
        global num
        id_anexo = entry_agregar_anexo.get().strip()
        
        if not id_anexo:
            messagebox.showerror("", "Por favor ingrese un anexo")
            return
        
        if id_anexo in anexos_list_summary:
            messagebox.showerror("", "El anexo ya ha sido agregado")
            return
        
        connection = sqlite3.connect(db_path)
        try:            
            query_show_detail = f'''SELECT 
                                        remesa_id, 
                                        guia_id, 
                                        anexo_id, 
                                        destino, 
                                        unidades, 
                                        peso_Kg, 
                                        valor 
                                    FROM (
                                        SELECT 
                                            COALESCE(remesas_guias.remesa_id, 'SIN REMESA') AS remesa_id, 
                                            COALESCE(anexos_guias.guia_id,  'SIN GUIA') AS guia_id,                                      
                                            COALESCE(anexos_guias.anexo_id, 'SIN ANEXO') AS anexo_id,
                                            COALESCE(guias.destino, 'SIN GUIA') AS destino, 
                                            COALESCE(guias.unidades, '0') AS unidades, 
                                            COALESCE(guias.peso_Kg, '0') AS peso_Kg, 
                                            COALESCE(anexos_guias.valor, 'SIN GUIA') AS valor,
                                            ROW_NUMBER() OVER(PARTITION BY anexos_guias.guia_id ORDER BY remesas_guias.remesa_id DESC) AS rn
                                        FROM 
                                            anexos_guias 
                                        LEFT JOIN 
                                            guias ON anexos_guias.guia_id = guias.numero_guia 
                                        LEFT JOIN 
                                            remesas_guias ON guias.numero_guia = remesas_guias.guia_id 
                                        WHERE 
                                            anexos_guias.anexo_id = '{id_anexo}'
                                    ) t
                                    WHERE rn = 1
                                '''
            result = connection.execute(query_show_detail).fetchall()
            if not result:
                raise Exception(id_anexo)
            query_summary_anexo = f'''  SELECT DISTINCT factura_id
                                        FROM facturas_guias
                                        WHERE facturas_guias.anexo_id = '{id_anexo}';            
                                    '''
            result_summary = connection.execute(query_summary_anexo).fetchall()
            if result_summary:
                messagebox.showwarning("", f"El anexo {id_anexo} ya ha sido agregado a la factura {result_summary[0][0]}")
                return            
            
            for row in result:
                treeview_guias.insert("", "end", values=[num] + list(row))
                num += 1
            
            connection.close()
            clean_treeview_summary_anexos()            
            anexos_list_summary[id_anexo] = {'anexo': id_anexo, 'guias': len(result), 'valor': sum([int(row[-1]) for row in result])}
            enumerate_rows(treeview_guias)
            print_summary_anexos()
            entry_agregar_anexo.delete(0, 'end')
            sum_total_factura()
        except Exception as e:
            messagebox.showerror("", f"No se encontro el anexo: {str(e)}")

    def delete_anexo(anexo_id):
        # anexo_id = entry_borrar_anexo.get().strip()
        selected_item = treeview_guias.focus()
        if selected_item:
            selected_value = treeview_guias.item(selected_item)['values'][0]
            anexo_id = selected_value
        
        if not anexo_id:
            messagebox.showerror("", "Por favor ingrese un anexo")
            return
        if anexo_id not in anexos_list_summary:
            messagebox.showerror("", "El anexo no ha sido agregado")
            return
        items = treeview_guias.get_children()
        confirm = messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres eliminar el anexo {anexo_id}?")
        if confirm:
            for item in items:
                if treeview_guias.item(item, 'values')[3] == anexo_id:        
                    treeview_guias.delete(item)
            enumerate_rows(treeview_guias)
            anexos_list_summary.pop(anexo_id)
            clean_treeview_summary_anexos()
            print_summary_anexos()
            sum_total_factura()
        entry_borrar_anexo.delete(0, 'end')
   
    def sum_total_factura():
        total = 0
        for item in treeview_guias.get_children():
            total += int(treeview_guias.item(item, 'values')[-1])
        entry_total_factura.delete(0, 'end')
        entry_total_factura.insert(0, "{:,}".format(total)) # type: ignore
   
    def clean_treeview_facturas():
        for item in treeview_facturas.get_children():
            treeview_facturas.delete(item)
        entry_delete_factura.delete(0, 'end')
        entry_search_factura.delete(0, 'end')
       
    def clean_treeview_guias():
        for item in treeview_guias.get_children():
            treeview_guias.delete(item)
        for item in treeview_summary_anexos.get_children():
            treeview_summary_anexos.delete(item)
        entry_id_factura.delete(0, 'end')
        entry_total_factura.delete(0, 'end')
        entry_agregar_guia.delete(0, 'end')
        entry_agregar_anexo.delete(0, 'end')
        anexos_list_summary.clear()
    
    def on_double_click_delete_anexo(event):
        selected_item = treeview_summary_anexos.focus()
        if selected_item:
            values = treeview_summary_anexos.item(selected_item, 'values')
            if values:
                entry_borrar_anexo.delete(0, 'end')
                entry_borrar_anexo.insert(0, values[0])
    
    def get_latest_factura():
        connection = sqlite3.connect(db_path)
        try:
            query_get_list_anexos = f"SELECT id_anexo FROM anexos ORDER BY id_anexo DESC;"
        except Exception as e:
            messagebox.showerror("", f"Error al obtener los anexos: {str(e)}")        
        connection.close()
           
    def get_list_anexos():
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT anexo_id FROM anexos_guias")
        result = cursor.fetchall()
        connection.close()
        return [row[0] for row in result]
    
    def save_factura():
        id_factura = entry_id_factura.get().strip().upper()
        if not entry_id_factura.get():
            messagebox.showerror("", "Por favor ingrese el numero de factura")
            return
        fecha_factura = date_entry_factura.get()
   
        connection = sqlite3.connect(db_path)
        try:
            query_insert_factura = f'''
                                    INSERT INTO facturas (
                                        id_factura, 
                                        fecha_factura, 
                                        cliente_factura, 
                                        valor_factura) 
                                        VALUES (
                                        '{id_factura}', 
                                        '{fecha_factura}', 
                                        '{entry_cliente.get()}', 
                                         {int(entry_total_factura.get().replace(',', ''))});
                                    ''' 
            connection.execute(query_insert_factura)
        except Exception as e:
            messagebox.showerror("", f"Error al guardar la factura: {str(e)}")
            return            
        try:
            values_list = []
            
            for item in treeview_guias.get_children():
                values = treeview_guias.item(item, 'values')
                values_list.append(values)
            

            cursor = connection.cursor()
            for value in values_list:
                cursor.execute(f"INSERT OR IGNORE INTO facturas_guias (factura_id, remesa_id, guia_id, anexo_id, destino, unidades, peso_Kg, valor) VALUES ('{entry_id_factura.get()}', '{value[1]}', '{value[2]}', '{value[3]}', '{value[4]}', {value[5]}, {value[6]}, {value[7]})") 
            connection.commit()            

            messagebox.showinfo("", "Factura guardada correctamente")
            clean_treeview_facturas()
            get_facturas()
        
            file = exportar_factura_excel()
            if file:
                # Check if the file  exists
                os.startfile(file)
        except Exception as e:
            messagebox.showerror("", f"Error al guardar las guias en la factura: {str(e)}")
        connection.close()
             
    def exportar_factura_excel():
        
        if not entry_id_factura.get():
            messagebox.showerror("", "Por favor ingrese el numero de factura")
            return
        
        id_factura = entry_id_factura.get()
        cliente = entry_cliente.get()
        fecha_factura = date_entry_factura.get_date() 
        
        file_location = "D:/intermodal/control/facturas"
        file_name = f"{entry_id_factura.get()}.xlsx"
        file_path = os.path.join(file_location, file_name)
        
        if file_path:        
            data_anexos = []
            # Get the data from the treeview
                        
            for item in treeview_guias.get_children():
                values = list(treeview_guias.item(item, 'values'))  # Convert tuple to list                
                values[5] = int(values[5]) #type: ignore
                values[6] = int(values[6]) #type: ignore
                values[7] = int(values[7]) #type: ignore
                data_anexos.append(values)
            
            # Create a DataFrame from the data
            df = pd.DataFrame(data_anexos, columns=['Num','Remesa', 'Guia', 'Anexo', 'Destino', 'Cant', 'Peso', 'Valor'])
            df.drop(columns=['Num'], inplace=True)
            df.sort_values(by='Anexo', ascending=True, inplace=True)
            
            with ExcelWriter(file_path, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Hoja1', index=False, startrow=2)
                
                #Access the XlsxWriter workbook and worksheet objects from the dataframe.
                
                worksheet = writer.sheets['Hoja1']
                worksheet.merge_range('A1:G1', f'LIQUIDACION REEXPEDICIONES COORDINADORA S.A.', writer.book.add_format({'bold': True, 'font_size': 12, 'align': 'center', 'border':1 })) #type: ignore
                
                worksheet.merge_range('A2:D2', f'RELACION DE GUIAS  R.T.P FACTURADAS ', writer.book.add_format({'bold': True, 'font_size': 12, 'align': 'center', 'border':1})) #type: ignore  
                worksheet.merge_range('E2:G2', f'FACTURA No. {id_factura} - {fecha_factura}' , writer.book.add_format({'bold': True, 'font_size': 12, 'align': 'center','border':1})) #type: ignore
                
                worksheet.set_column('A:G', 13, writer.book.add_format({'align': 'center'})) #type: ignore
                worksheet.set_column('D:D', 25, writer.book.add_format({'align': 'center'})) #type: ignore
                worksheet.set_column('G:G', 14, writer.book.add_format({'align': 'center', 'num_format': '"$"#,##0'})) #type: ignore
                
                total_valor = df['Valor'].sum()
                worksheet.write(len(df) + 3, 5, 'TOTAL', writer.book.add_format({'bold': True, 'align': 'center', 'border':1})) #type: ignore
                worksheet.write(len(df) + 3, 6, total_valor, writer.book.add_format({'bold': True, 'align': 'center', 'border':1, 'num_format': '"$"#,##0'})) #type: ignore
                
                # Set the border for the cells with data
                num_rows_anexo = len(df)                
                cell_range_anexo = f'A3:H{num_rows_anexo+3}'
                worksheet.conditional_format(cell_range_anexo, {'type': 'no_blanks', 'format': writer.book.add_format({'border': 1})}) #type: ignore
             
        #  Create a summary DataFrame
                data_summary_anexos = []
                for item in treeview_summary_anexos.get_children():
                    values = list(treeview_summary_anexos.item(item, 'values'))  # Convert tuple to list
                    values[1] = int(values[1]) #type:ignore
                    values[2] = int(values[2]) #type:ignore                                        
                    data_summary_anexos.append(values)                    
                
                df_anexos = pd.DataFrame(data_summary_anexos, columns=columns_summary)
                df_anexos.to_excel(writer, sheet_name='Hoja1', index=False, startrow=2, startcol=8)
                
                worksheet.merge_range('I2:K2', f'RESUMEN DE ANEXOS', writer.book.add_format({'bold': True, 'font_size': 12, 'align': 'center', 'border':1})) #type: ignore
                
                num_rows_summary = len(df_anexos)
                cell_range_summary = f'I3:K{num_rows_summary+3}'
                worksheet.conditional_format(cell_range_summary, {'type': 'no_blanks', 'format': writer.book.add_format({'border': 1,})}) #type: ignore               
                worksheet.set_column('I:K', 13, writer.book.add_format({'align': 'center'})) #type: ignore
                worksheet.set_column('K:K', 14, writer.book.add_format({'align': 'center', 'num_format': '"$"#,##0'})) #type: ignore
                
        # os.startfile(file_path)
        if os.path.exists(file_path):
        # Generate a new file name with a number suffix
            file_name, file_extension = os.path.splitext(file_path)
            file_number = 1
            new_file = f"{file_name}_{file_number}{file_extension}"
            while os.path.exists(new_file):
                file_number += 1
                new_file = f"{file_name}_{file_number}{file_extension}"
            file = new_file
            os.rename(file_path, new_file)
            os.startfile(file)
        return file

    def search_edit_factura(factura):
        # clean_treeview_guias()
        get_anexos_in_factura(factura)
        if not factura:
            messagebox.showerror("", "Por favor ingrese una factura")
            return
        
        connection = sqlite3.connect(db_path)
        try:
            query_search_factura = f'''
                                        SELECT
                                        id_factura,
                                        cliente_factura,
                                        fecha_factura,
                                        valor_factura                                    
                                        FROM facturas 
                                        WHERE id_factura = '{factura}';
                                    '''
            result = connection.execute(query_search_factura).fetchall()            
            if not result:
                raise Exception(factura)
            
            clean_entries_factura()
            entry_id_factura.insert(0, result[0][0])
            entry_cliente.insert(0, result[0][1])
            date_entry_factura.set_date(result[0][2])
            entry_total_factura.insert(0, "{:,}".format(result[0][3])) # type: ignore
            
            clean_treeview_guias()
            guias = get_facturas_detail(factura)
            for row in guias:
                treeview_guias.insert("", "end", values=[num] + list(row))
            enumerate_rows(treeview_guias)

        except Exception as e:
            messagebox.showerror("", f"Error al buscar la remesa: {str(e)}")
        
        connection.close()
    
    def get_anexos_in_factura(factura):
        connection = sqlite3.connect(db_path)
        try:
            query_get_anexos_from_factura = f'''
                                    SELECT facturas_guias.anexo_id, COUNT(facturas_guias.anexo_id), SUM(facturas_guias.valor)   
                                    FROM facturas_guias  
                                    WHERE factura_id = '{factura}'    
                                    GROUP BY anexo_id;                       
                                '''
            result = connection.execute(query_get_anexos_from_factura).fetchall()
            connection.close()
            treeview_summary_anexos.delete(*treeview_summary_anexos.get_children())
            for row in result:
                treeview_summary_anexos.insert('', 'end', values=(row))
                
            
            return result
        except Exception as e:
            messagebox.showerror("", f"Error al obtener los anexos: {str(e)}")
    
    def update_factura(factura):
        if not factura:
            messagebox.showerror("", "Por favor ingrese una factura")
            return
        search_edit_factura(factura)
        
        
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            
            query_update_factura = f'''
                                    UPDATE facturas 
                                    SET
                                    id_factura = '{entry_id_factura.get()}',
                                    cliente_factura = '{entry_cliente.get()}',
                                    fecha_factura = '{date_entry_factura.get()}',
                                    valor_factura = {int(entry_total_factura.get().replace(',', ''))}
                                    WHERE id_factura = '{factura}';
                                    '''
            cursor.execute(query_update_factura)            
            query_delete_facturas_guias = f'''DELETE FROM facturas_guias WHERE factura_id = '{factura}';'''
            cursor.execute(query_delete_facturas_guias)
            
            rows_to_update = []
            for item in treeview_guias.get_children():
                values = list(treeview_guias.item(item, 'values'))
                rows_to_update.append(values)
                
            for row in rows_to_update:
                cursor.execute(f"INSERT INTO facturas_guias (factura_id, remesa_id, guia_id, anexo_id, destino, unidades, peso_Kg, valor) VALUES ('{entry_id_factura.get()}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', {row[5]}, {row[6]}, {row[7]})")
            connection.commit()
            messagebox.showinfo("", "Remesa actualizada correctamente") 
        except Exception as e:
            messagebox.showerror("", f"Error al actualizar la remesa: {str(e)}")
            
        connection.close()    
        
        
    tab_facturacion = ttk.Notebook(frame)
    tab_facturacion.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
    tab_facturacion.grid_columnconfigure(0, weight=1)
    
    frame_facturacion = ttk.LabelFrame(tab_facturacion, )
    frame_facturacion.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
    frame_facturacion.grid_columnconfigure(0, weight=1)
    
    frame_crear_factura = ttk.Frame(frame_facturacion,)
    frame_crear_factura.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
    frame_crear_factura.grid_columnconfigure(0, weight=1)
    
    # Create elements for creating a factura
    frame_date_factura = ttk.Frame(frame_crear_factura,)
    frame_date_factura.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
    for i in range(12):
        frame_date_factura.grid_columnconfigure(i, weight=1)    
    
    Label_Cliente = ttk.Label(frame_date_factura, text='Cliente:')
    Label_Cliente.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    
    entry_cliente = ttk.Combobox(frame_date_factura, values=["Coordinadora", "TCC"])
    entry_cliente.current(0)
    entry_cliente.grid(row=0, column=1, padx=5, pady=5, columnspan=3, sticky='we')
    entry_cliente.state(['readonly'])
    
    lbl_id_factura = ttk.Label(frame_date_factura, text='Factura:').grid(row=1, column=0, padx=5, pady=5, sticky='w')    
    entry_id_factura = ttk.Entry(frame_date_factura)
    entry_id_factura.grid(row=1, column=1, padx=5,  pady=5,sticky='we' )
    
    lbl_fecha = ttk.Label(frame_date_factura, text='Fecha:').grid(row=1, column=2, padx=5, pady=5, sticky='e')    
    date_entry_factura = DateEntry(frame_date_factura, foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy' )
    date_entry_factura.grid(row=1, column=3, padx=5, pady=5, sticky='we',  )
    
    label_agregar_guia = ttk.Label(frame_date_factura, text='Agregar Guia:').grid(row=2, column=0, padx=5, pady=5, sticky='w', )
    entry_agregar_guia = ttk.Entry(frame_date_factura, state='disabled')
    entry_agregar_guia.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='we')
    
    btn_agregar_guia = ttk.Button(frame_date_factura, text='Agregar Guia', state='disabled')
    btn_agregar_guia.grid(row=2, column=3, padx=5, pady=5, sticky='we')
    
    label_agregar_anexo = ttk.Label(frame_date_factura, text='Agregar Anexo:').grid(row=3, column=0, padx=5, pady=5, sticky='w', )
    entry_agregar_anexo = ttk.Combobox(frame_date_factura, values=get_list_anexos())
    entry_agregar_anexo.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky='we')    
    
    btn_agregar_anexo = ttk.Button(frame_date_factura, text='Agregar Anexo', command=get_anexos)
    btn_agregar_anexo.grid(row=3, column=3, padx=5, pady=10, sticky='we')
    
    label_borrar_anexo = ttk.Label(frame_date_factura, text='Borrar Anexo:').grid(row=4, column=0, padx=5, pady=5, sticky='w', )
    entry_borrar_anexo = ttk.Entry(frame_date_factura)
    entry_borrar_anexo.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky='we')
    
    btn_borrar_anexo = ttk.Button(frame_date_factura, text='Borrar Anexo', command= lambda: delete_anexo(entry_borrar_anexo.get().strip()))
    btn_borrar_anexo.grid(row=4, column=3, padx=5, pady=5, sticky='we')
    
    camps_factura = ['Num','Remesa', 'Guia', 'Anexo', 'Destino', 'Unidades', 'Peso Kg', 'Valor']
    
    treeview_guias = ttk.Treeview(frame_crear_factura, height=15, columns=camps_factura, selectmode='browse', show='headings' )
    treeview_guias.grid(row=2, column=0, columnspan=6, padx=5, pady=5, sticky= 'nswe')
    vscrollbar = ttk.Scrollbar(frame_crear_factura, orient="vertical", command=treeview_guias.yview)
    vscrollbar.grid(row=2, column=8, sticky='ns')
    treeview_guias.configure(yscrollcommand=vscrollbar.set)
    
    treeview_guias.config(columns=camps_factura)
    for camp in camps_factura:
        treeview_guias.heading(camp,  text=camp )
    
    treeview_guias.column('Num', width=50, anchor='center', stretch=False)
    treeview_guias.column('Remesa', width=80, anchor='center', stretch=False)
    treeview_guias.column('Guia', width=80, anchor='center', stretch=False)
    treeview_guias.column('Anexo', width=80, anchor='center', stretch=False)
    treeview_guias.column('Destino', width=200, anchor='center', stretch=False)
    treeview_guias.column('Unidades', width=80, anchor='center', stretch=False)
    treeview_guias.column('Peso Kg', width=80, anchor='center', stretch=False)
    treeview_guias.column('Valor', width=80, anchor='center', stretch=False)
        
    #************************************************************************************************
    #************************************************************************************************
    #************************************************************************************************
    
    columns_summary = ['Anexo', 'Guias', 'Valor']
    label_summary_anexos = ttk.Label(frame_date_factura, text='Anexos:').grid(row=0, column=6, padx=5, pady=5, sticky='ew')
    treeview_summary_anexos = ttk.Treeview(frame_date_factura, height=6, columns= columns_summary, selectmode='browse', show='headings')
    treeview_summary_anexos.grid(row=1, column=6, columnspan=6, padx=5, pady=5, sticky='we', rowspan=4, )
    
    treeview_summary_anexos.column('Anexo', width=80, anchor='center', stretch=False)
    treeview_summary_anexos.column('Guias', width=80, anchor='center', stretch=False)
    treeview_summary_anexos.column('Valor', width=80, anchor='center', stretch=False)
    treeview_summary_anexos.bind('<Delete>', lambda event: delete_anexo(treeview_summary_anexos.item(treeview_summary_anexos.focus(), 'values')[0])) # type: ignore

    treeview_summary_anexos.bind('<Double-1>', on_double_click_delete_anexo)
    
    treeview_summary_anexos.heading('Anexo', text='Anexo')
    treeview_summary_anexos.heading('Guias', text='Guias')
    treeview_summary_anexos.heading('Valor', text='Valor')
    
    treeview_summary_anexos.bind('<Delete>', lambda event: delete_anexo(treeview_summary_anexos.item(treeview_summary_anexos.focus(), 'values')[0])) # type: ignore
    
    vscrollbar_summary_anexos = ttk.Scrollbar(frame_date_factura, orient="vertical", command=treeview_summary_anexos.yview)
    vscrollbar_summary_anexos.grid(row=1, column=12,  rowspan=4, sticky='ns')
    treeview_summary_anexos.configure(yscrollcommand=vscrollbar_summary_anexos.set)
    
    frame_totals = ttk.Frame(frame_crear_factura)
    frame_totals.grid(row=5, column=0, padx=5, pady=5, sticky='e')
    
    frame_search_single_factura = ttk.Frame(frame_crear_factura)
    frame_search_single_factura.grid(row=5, column=0, padx=5, pady=5, sticky='w')
    
    entry_search_single_factura = ttk.Entry(frame_search_single_factura, width=15)
    entry_search_single_factura.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    
    btn_search_single_factura = ttk.Button(frame_search_single_factura, text='Buscar Factura', command= lambda: search_edit_factura(entry_search_single_factura.get().strip()))
    btn_search_single_factura.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    
    btn_update_factura = ttk.Button(frame_search_single_factura, text='Actualizar Factura', command= lambda: update_factura(entry_search_single_factura.get()))
    btn_update_factura.grid(row=0, column=2, padx=5, pady=5, sticky='w')
    
    label_total_factura = ttk.Label(frame_totals, text='Total Factura:').grid(row=5, column=0, padx=5, pady=5, sticky='w')
    entry_total_factura = ttk.Entry(frame_totals)
    entry_total_factura.grid(row=5, column=1, padx=5, pady=5, sticky='e')
    
    frame_buttons = ttk.Frame(frame_crear_factura)
    frame_buttons.grid(row=6, column=0, padx=5, pady=5, sticky='nsew')
    
    btn_guardar_factura = ttk.Button(frame_buttons, text='Guardar Factura', command= lambda: save_factura())
    btn_guardar_factura.grid(row=0, column=0, padx=5, pady=5, sticky='')
    
    btn_exportar_factura = ttk.Button(frame_buttons, text='Exportar Factura', command= lambda: exportar_factura_excel())
    btn_exportar_factura.grid(row=0, column=1, padx=5, pady=5, sticky='')
    
    btn_nueva_factura = ttk.Button(frame_buttons, text='Nueva Factura', command= lambda: clean_treeview_guias())
    btn_nueva_factura.grid(row=0, column=2, padx=5, pady=5, sticky='')
    
    tab_facturacion.add(frame_facturacion, text='Crear Factura')

    #***********************************TAB-SEARCH-REMESAS*************************************************************
    #***********************************TAB-SEARCH-REMESAS*************************************************************
    #***********************************TAB-SEARCH-REMESAS*************************************************************
    
    def get_facturas():
        connection = sqlite3.connect(db_path)
        try:
            query_get_facturas = f'''SELECT * FROM facturas;'''
            result = connection.execute(query_get_facturas).fetchall()
            for row in result:
                treeview_facturas.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("", f"Error al obtener las facturas: {str(e)}")
        connection.close()
    
    def delete_factura(factura_id):
        if not factura_id:
            messagebox.showerror("", "Por favor ingrese un numero de factura")
            return
        items = treeview_facturas.get_children()
        factura_found = False
        for item in items:
            if treeview_facturas.item(item, 'values')[0] == factura_id:
                factura_found = True
                break
        if factura_found:
            confirm = messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres eliminar la factura {factura_id}?")
            if confirm:
                connection = sqlite3.connect(db_path)
                treeview_facturas.delete(item)
                try:
                    query_delete_factura = f'''DELETE FROM facturas WHERE id_factura = '{factura_id}';'''
                    connection.execute(query_delete_factura)
                    connection.commit()
                    
                    query_delete_facturas_guias = f'''DELETE FROM facturas_guias WHERE factura_id = '{factura_id}';'''
                    connection.execute(query_delete_facturas_guias)
                    connection.commit()
                    entry_search_factura.delete(0, 'end')
                    entry_delete_factura.delete(0, 'end')
                    treeview_facturas_detail.delete(*treeview_facturas_detail.get_children())
                    messagebox.showinfo("", "Factura eliminada correctamente")
                except Exception as e:
                    messagebox.showerror("", f"Error al eliminar la factura: {str(e)}")        
                connection.close()
        else:
            messagebox.showerror("", f"La factura {factura_id} no existe")
        
    
    def get_facturas_detail(factura_id):
        for item in treeview_facturas_detail.get_children():
            treeview_facturas_detail.delete(item)
        
        connection = sqlite3.connect(db_path)
        try:
            query_get_facturas_detail = f'''
                    SELECT 
                            Remesa,
                            guia_id,
                            anexo_id,
                            destino,
                            unidades,
                            peso_Kg,
                            valor
                        FROM (
                            SELECT 
                                COALESCE (remesas_guias.remesa_id, 'SIN REMESA') AS Remesa,
                                facturas_guias.guia_id, 
                                facturas_guias.anexo_id, 
                                facturas_guias.destino, 
                                facturas_guias.unidades, 
                                facturas_guias.peso_Kg, 
                                facturas_guias.valor,
                                ROW_NUMBER() OVER(PARTITION BY facturas_guias.guia_id ORDER BY remesas_guias.remesa_id DESC) AS rn
                            FROM 
                                facturas_guias
                            LEFT JOIN 
                                remesas_guias ON remesas_guias.guia_id = facturas_guias.guia_id
                            WHERE 
                                factura_id = '{factura_id}'
                        ) AS sub
                        WHERE rn = 1
                        ORDER BY anexo_id ASC;
                    '''
            result = connection.execute(query_get_facturas_detail).fetchall()
            if not result:
                raise Exception(factura_id)
                        
            for row in result:
                treeview_facturas_detail.insert("", "end", values=[num] + list(row))
            enumerate_rows(treeview_facturas_detail)                
            
        except Exception as e:
            messagebox.showinfo("", f"No se encuentra la factura: {str(e)}")
        connection.close()
        return result
    
    #**** Facturas****
    #**** Facturas****
    
    frame_search_factura = ttk.LabelFrame(tab_facturacion, text='')
    frame_search_factura.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
    
    frame_get_facturas = ttk.LabelFrame(frame_search_factura, text='Facturas')
    frame_get_facturas.grid(row=0, column=0, padx=5, pady=5, sticky='nsw')
    
    label_search_factura = ttk.Label(frame_get_facturas, text='Buscar Factura:').grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_search_factura = ttk.Entry(frame_get_facturas)
    entry_search_factura.grid(row=0, column=1, padx=5, pady=5, sticky='we') 
    
    btn_search_factura = ttk.Button(frame_get_facturas, text='Buscar Factura', command= lambda: get_facturas_detail(entry_search_factura.get()))
    btn_search_factura.grid(row=0, column=2, padx=5, pady=5, sticky='we')
    
    label_delete_factura = ttk.Label(frame_get_facturas, text='Eliminar Factura:').grid(row=1, column=0, padx=5, pady=5, sticky='w')
    entry_delete_factura = ttk.Entry(frame_get_facturas)
    entry_delete_factura.grid(row=1, column=1, padx=5, pady=5, sticky='we')
    
    btn_delete_factura = ttk.Button(frame_get_facturas, text='Eliminar Factura', command= lambda: delete_factura(entry_delete_factura.get()))
    btn_delete_factura.grid(row=1, column=2, padx=5, pady=5, sticky='we')
    
    columns_facturas = ['Factura', 'Cliente', 'Fecha', 'Valor']    
    treeview_facturas = ttk.Treeview(frame_get_facturas, height=21, columns=columns_facturas, selectmode='browse', show='headings' )
    treeview_facturas.grid(row=5, column=0, columnspan= 6, padx=5, pady=5, sticky= 'nswe')
    treeview_facturas.column('Factura', width=100, anchor='center')
    treeview_facturas.column('Cliente', width=100, anchor='center')
    treeview_facturas.column('Fecha', width=100, anchor='center')
    treeview_facturas.column('Valor', width=100, anchor='center')    
    treeview_facturas.bind('<Delete>', lambda event: delete_factura(treeview_facturas.item(treeview_facturas.focus(), 'values')[0])) # type: ignore
    treeview_facturas.bind('<ButtonRelease-1>', lambda event: get_facturas_detail(treeview_facturas.item(treeview_facturas.focus(), 'values')[0]))

    def on_double_click_delete_factura(event):
        selected_item = treeview_facturas.focus()
        if selected_item:
            values = treeview_facturas.item(selected_item, 'values')
            if values:
                entry_delete_factura.delete(0, 'end')
                entry_delete_factura.insert(0, values[0])
  
    treeview_facturas.bind('<Double-1>', on_double_click_delete_factura)
    
    for camp in columns_facturas:
        treeview_facturas.heading(camp,  text=camp, anchor='center')
    vscrollbar = ttk.Scrollbar(frame_get_facturas, orient="vertical", command=treeview_facturas.yview)
    vscrollbar.grid(row=5, column=7, sticky='ns')
    
    #****Facturas_detail****
    #****Facturas_detail****
    
    frame_facturas_detail = ttk.LabelFrame(frame_search_factura, text='Detalle Factura')
    frame_facturas_detail.grid(row=0, column=1, padx=5, pady=5, sticky='nse')
    
    columns_facturas_detail = ['Num','Remesa', 'Guia', 'Anexo', 'Destino', 'Unidades', 'Peso Kg', 'Valor']
    treeview_facturas_detail = ttk.Treeview(frame_facturas_detail, height=25, columns=columns_facturas_detail, selectmode='browse', show='headings' )
    treeview_facturas_detail.grid(row=1, column=0, columnspan=6, padx=5, pady=5, sticky= 'nswe')
    treeview_facturas_detail.column('Num', width=50, anchor='center', stretch=False)
    treeview_facturas_detail.column('Remesa', width=80, anchor='center', stretch=False)
    treeview_facturas_detail.column('Guia', width=80, anchor='center', stretch=False)
    treeview_facturas_detail.column('Anexo', width=80, anchor='center', stretch=False)
    treeview_facturas_detail.column('Destino', width=200, anchor='center', stretch=False)
    treeview_facturas_detail.column('Unidades', width=60, anchor='center', stretch=False)
    treeview_facturas_detail.column('Peso Kg', width=60, anchor='center', stretch=False)
    treeview_facturas_detail.column('Valor', width=80, anchor='center', stretch=False,)
    
    
    for camp in columns_facturas_detail:
        treeview_facturas_detail.heading(camp,  text=camp, anchor='center')    
    
    vscrollbar = ttk.Scrollbar(frame_facturas_detail, orient="vertical", command=treeview_facturas_detail.yview)
    vscrollbar.grid(row=1, column=9, sticky='ns')
    treeview_facturas_detail.configure(yscrollcommand=vscrollbar.set)

    
    get_facturas()
    
    
    tab_facturacion.add(frame_search_factura, text='Buscar Factura')
    