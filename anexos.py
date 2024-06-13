import os
import pandas as pd
import pdfplumber
import tkinter as tk
import PyPDF2
import re
import sqlite3
from config import load_config
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk

def _convert_stringval(value):
    if hasattr(value, 'typename'):
        value = str(value)
        try:
            value = int(value)
        except (ValueError, TypeError):
            pass
    return value

ttk._convert_stringval = _convert_stringval # type: ignore

def show_anexos(frame, tab_to_show, width, height,):
    config =load_config()
    db_path = config['db_path']  # type: ignore
    def focus_tab(tab):
        tab.select(tab_to_show) 
    def extract_table():
        full_table = []
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            tree.delete(*tree.get_children())
            clean_table_show_anexos()
            # for get the number of the anexo
            with open(file_path, "rb") as file:
                # extraer el numero del anexo con re
                pdf_reader = PyPDF2.PdfReader(file)
                text = pdf_reader.pages[0].extract_text()
                number_anexo = r"Documento No: (\d+)"
                date_anexo = r"Fecha: (\d{4}-\d{2}-\d{2})"  # Updated regular expression pattern for date
                result_number = re.search(number_anexo, text)
                result_date = re.search(date_anexo, text)
                if result_number:
                    numero_documento = result_number.group(1)
                    entry_num_anexo.insert(0, numero_documento)
                if result_date:
                    entry_fecha_anexo.insert(0, result_date.group(1))

                file.close()

            with pdfplumber.open(file_path) as pdf:
                # Iterar sobre las páginas del PDF
                total_pages = len(pdf.pages)
                last_page = total_pages - 1
                text = pdf.pages[last_page].extract_text()
                for page in pdf.pages:
                    # Extraer todas las tablas de la página
                    tables = page.extract_tables()
                    # Iterar sobre las tablas extraídas
                    for table in tables:
                        # Omitir la primera fila (suponiendo que es la fila de encabezados)
                        table_data = table[2:]  # Comenzar desde la segunda fila
                        # Agregar las filas de la tabla (sin los encabezados) a la lista

                        full_table.extend(table_data)
                        df = pd.DataFrame(full_table)
                        df = df.dropna(axis="columns", how="all")
                        
            df.columns = [ "GUIA", "PRODUCTO", "DESTINO", "UDS", "PESO", "FTE FIJO", "FTE VARIABLE", "FTE TOTAL", "TIPO",]
            # set names to columns            
            
            #setting types to columns
            df["GUIA"] = df["GUIA"].astype(str)

            # Antes de convertir a numérico, elimina los puntos de los números que representan miles
            df['FTE FIJO'] = df['FTE FIJO'].str.replace('.', '').astype(float)
            df['FTE VARIABLE'] = df['FTE VARIABLE'].str.replace('.', '').astype(float)
            df['FTE TOTAL'] = df['FTE TOTAL'].str.replace('.', '').astype(float)

            # Ahora puedes convertir a enteros o dejarlos como flotantes si así lo prefieres
            df['FTE FIJO'] = df['FTE FIJO'].astype(int)
            df['FTE VARIABLE'] = df['FTE VARIABLE'].astype(int)
            df['FTE TOTAL'] = df['FTE TOTAL'].astype(int)


            df[["UDS", "FTE FIJO", "PESO", "FTE VARIABLE", "FTE TOTAL"]] = df[
                ["UDS", "FTE FIJO", "PESO", "FTE VARIABLE", "FTE TOTAL"]
            ].apply(pd.to_numeric, errors="coerce")
                    
            
            df[["FTE FIJO", "FTE TOTAL", "FTE VARIABLE"]] = df[["FTE FIJO", "FTE TOTAL", "FTE VARIABLE"]].astype(int)
            
            # Clear the treeview before inserting data
            
        
        
            for index, row in df.iterrows():
                values = [str(value) for value in row]
                values[5] = "{:,}".format(int(values[5]))
                values[7] = "{:,}".format(int(values[7]))
                tree.insert("", "end", values=values)        
            
        
            sum_items = int(df["UDS"].sum())
            sum_fte = int((df["FTE TOTAL"]).sum())
            # sum_kg = (df["PESO"]).sum()
            num_records = int(len(df))

            entry_total_unidades.insert(0, str(sum_items))
            entry_total_guias.insert(0, str(num_records))
            entry_total_fte.insert(0, "{:,}".format(sum_fte))

            # Add sum_items and sum_fte to the dataframe
            df.loc["Blanck Space"] = ["", "", "", "", "", "", "", "", ""]
            df.loc["Sum Items"] = ["","","","","","","","TOTAL GUIAS",num_records, ]
            df.loc["Total Unidades"] = ["","","","","","","","TOTAL UNIDADES",sum_items,]
            df.loc["Sum Values"] = ["", "", "", "", "", "", "", "VALOR TOTAL", sum_fte]

        return df 
    def export_pdf():
        export = extract_table()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")]
        )
        if file_path:
            export.to_excel(file_path, index=False)
            os.startfile(file_path)
    def clean_table_show_anexos():
        entry_fecha_anexo.delete(0, tk.END)
        entry_num_anexo.delete(0, tk.END)
        entry_total_guias.delete(0, tk.END)
        entry_total_unidades.delete(0, tk.END)
        entry_total_fte.delete(0, tk.END)
        for i in tree.get_children():
            tree.delete(i)
    def save_anexo():
        id_anexo = entry_num_anexo.get()
        fecha = entry_fecha_anexo.get()
        total_unidades = entry_total_unidades.get()
        total_guias = entry_total_guias.get()
        fte_total = entry_total_fte.get().replace(",", "")

        list_guias_to_insert = []
        try : 
            for row in tree.get_children():
                list_guias_values = [tree.item(row)["values"][0], tree.item(row)["values"][2]]
                list_guias_values = tree.item(row)["values"]
                list_guias_to_insert.append((list_guias_values[0], list_guias_values[2], list_guias_values[3], list_guias_values[4], list_guias_values[7], list_guias_values[8]))
                
        
        except Exception as e:
            messagebox.showerror("", f"Error al obtener la lista: {str(e)}")
            return

        #insert anexo into the database
        try:
            connection = sqlite3.connect(db_path)
            query = f"INSERT INTO anexos (id_anexo, fecha_anexo, total_unidades, total_guias, fte_total) VALUES ('{id_anexo}', '{fecha}', '{(int(total_unidades))}', '{int(total_guias)}', '{(fte_total)}');"
            result = connection.execute(query)
            connection.commit()
            if result:
                messagebox.showinfo("", "Anexo guardado con éxito")
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror("", f"El anexo {id_anexo} ya existe")
            
        #insert guias to anexos_guias
        query_anexos = "INSERT INTO anexos_guias (anexo_id, guia_id, destino, unds, peso, valor, tipo ) VALUES "
        for i in range(len(list_guias_to_insert)):
            row = list(list_guias_to_insert[i])
            row[4]=row[4].replace(",", "")
            query_anexos += f"('{id_anexo}', '{row[0]}', '{row[1]}', {row[2]}, {row[3]}, {(row[4])}, '{row[5]}' )"
                  
            if i != len(list_guias_to_insert) - 1:
                query_anexos += ", "
            else:
                query_anexos += ";" 
        
        try:
            result = connection.execute(query_anexos)
            connection.commit()
        except Exception as e:
            if "incomplete input" in str(e):
                messagebox.showerror("", "Seleccione un anexo: ")
                return
        
        connection.close()
        clean_table_show_anexos()
        get_anexos()
    def delete_anexo():
        # id_anexo_del = entry_num_anexo.get()
        id_anexo_delete =  tree_search.item(tree_search.focus())["values"][0]
        confirmed = messagebox.askyesno("Confirmar", f"¿Desea borrar el anexo {id_anexo_delete} ?")
        if not confirmed:
            return
        connection = sqlite3.connect(db_path)
        
         # Primera consulta para eliminar de la tabla anexos_guias
        try:
            query_anexos_guias = f"DELETE FROM anexos_guias WHERE anexo_id = '{id_anexo_delete}';"
            connection.execute(query_anexos_guias)
            connection.commit()
         
        except sqlite3.Error as e:
            messagebox.showerror("", f"Error al eliminar guias del anexo: {e}")
         
        # Segunda consulta para eliminar de la tabla anexos
        
        try:
            query_anexos = f"DELETE FROM anexos WHERE id_anexo = '{id_anexo_delete}';"
            result = connection.execute(query_anexos)
            connection.commit()
            if result:
                messagebox.showinfo("", "Anexo eliminado con éxito")
        except sqlite3.Error as e:
            messagebox.showerror("", f"Error al eliminar el anexo: {e}")
        
        
        connection.close()
        clean_anexos()
        clean_detail()
        get_anexos()
    for widget in frame.winfo_children():
        widget.grid_forget()    
        
    tab_anexos = ttk.Notebook(frame, bootstyle="secondary", width=width, height=height) # type: ignore
    tab_anexos.grid(row=0, column=0, sticky="nswe")

    tab_anexos.grid_propagate(False)
    tab_anexos.grid_columnconfigure(0, weight=1)
    tab_anexos.grid_rowconfigure(0, weight=1)
    
    frame_anexos = ttk.Frame(tab_anexos, )
    frame_anexos.grid(row=0, column=0, sticky="snwe", padx= 10, pady=20)
    frame_anexos.grid_columnconfigure(0, weight=1)
    frame_anexos.grid_rowconfigure(0, weight=0)
    frame_anexos.grid_rowconfigure(1, weight=1)
    frame_anexos.grid_rowconfigure(2, weight=0)
    
    tree = ttk.Treeview(frame_anexos, show="headings", selectmode="browse")
    tree.grid(row=1, column=0, columnspan=4, sticky="wens", padx=10, pady=10)

    # Define columns
    tree["columns"] = ( "GUIA", "PRODUCTO", "DESTINO", "UDS", "PESO", "FTE FIJO", "FTE VARIABLE", "FTE TOTAL", "TIPO", )

    # Format columns
    tree.column("GUIA", width=100, anchor="center")
    tree.column("PRODUCTO", width=100, anchor="center")
    tree.column("DESTINO", width=100, anchor="center")
    tree.column("UDS", width=50, anchor="center")
    tree.column("PESO", width=50, anchor="center")
    tree.column("FTE FIJO", width=100, anchor="center")
    tree.column("FTE VARIABLE", width=100, anchor="center")
    tree.column("FTE TOTAL", width=100, anchor="center")
    tree.column("TIPO", width=100, anchor="center")

    # Create headings
    tree.heading("GUIA", text="GUIA")
    tree.heading("PRODUCTO", text="PRODUCTO")
    tree.heading("DESTINO", text="DESTINO")
    tree.heading("UDS", text="UDS")
    tree.heading("PESO", text="KG")
    tree.heading("FTE FIJO", text="FTE FIJO")
    tree.heading("FTE VARIABLE", text="FTE VARIABLE")
    tree.heading("FTE TOTAL", text="FTE TOTAL")
    tree.heading("TIPO", text="TIPO")

    # Add a scrollbar to the treeview
    scrollbar = ttk.Scrollbar(frame_anexos, bootstyle = 'primary-round', orient="vertical", command=tree.yview) # type: ignore
    scrollbar.grid(row=1, column=4, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    frame_add_anexos = ttk.Frame(frame_anexos)
    frame_add_anexos.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="se")

    # Button to add anexos
    btn_save_anexos = ttk.Button(frame_add_anexos, text="Guardar Anexo", command=lambda: save_anexo())
    btn_save_anexos.grid(row=0, column=0, padx=10, pady=5, sticky="e")

    btn_add_anexos = ttk.Button(frame_add_anexos, text="Seleccionar Anexo", command=lambda: extract_table())
    btn_add_anexos.grid(row=0, column=2, padx=10, pady=5, sticky="e")

    btn_export_anexos = ttk.Button(frame_add_anexos, text="Exportar excel", command=lambda: export_pdf())
    btn_export_anexos.grid(row=0, column=3, padx=10, pady=5, sticky="e")

    ttk.Label(frame_anexos, text="Fecha Anexo:").grid(row=0, column=2, padx=10, pady=5, sticky="e")
    entry_fecha_anexo = ttk.Entry(frame_anexos)
    entry_fecha_anexo.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
    entry_fecha_anexo.config(justify="center")

    ttk.Label(frame_anexos, text="Numero de Anexo:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_num_anexo = ttk.Entry(frame_anexos)
    entry_num_anexo.grid( row=0, column=1, padx=10, pady=5, sticky="ew", )
    entry_num_anexo.config(justify="center")

    ttk.Label(frame_anexos, text="Total Guias:").grid(row=4, column=2, padx=10, pady=5, sticky="e")
    entry_total_guias = ttk.Entry(frame_anexos)
    entry_total_guias.grid(row=4, column=3, padx=10, pady=5, sticky="ew")
    entry_total_guias.config(justify="center")

    ttk.Label(frame_anexos, text="Total Unidades:").grid(row=5, column=2, padx=10, pady=5, sticky="e")
    entry_total_unidades = ttk.Entry(frame_anexos)
    entry_total_unidades.grid(row=5, column=3, padx=10, pady=5, sticky="ew")
    entry_total_unidades.config(justify="center")

    ttk.Label(frame_anexos, text="Total FTE:").grid(row=6, column=2, padx=10, pady=5, sticky="e")
    entry_total_fte = ttk.Entry(frame_anexos)
    entry_total_fte.grid(row=6, column=3, padx=10, pady=5, sticky="ew")
    entry_total_fte.config(justify="center")
    
    tab_anexos.add(frame_anexos, text="Agregar Anexo")

##********************************************************************************************************************
##********************************************TAB SEARCH ANEXOS ******************************************************
##********************************************TAB SEARCH ANEXOS ******************************************************
##********************************************TAB SEARCH ANEXOS ******************************************************
##********************************************************************************************************************
    
    def get_anexos():
        clean_anexos()
        tree_search.delete(*tree_search.get_children())
        connection = sqlite3.connect(db_path)
        # Execute the query to search for the anexo
        query = "SELECT id_anexo, fecha_anexo, total_unidades, total_guias, fte_total FROM anexos ORDER BY id_anexo DESC;"
        result = connection.execute(query).fetchall()
        for row in result:
            row_list = list(row)
            row_list[4] = "{:,}".format(int(row_list[4]))
            
            tree_search.insert("", "end", values=row_list)
        # Close the database connection
        connection.close()
    def clean_detail():
        tree_detail.delete(*tree_detail.get_children())
    def clean_anexos():
        tree_search.delete(*tree_search.get_children())
    def clean_anexo_summary():
        tree_anexo_summary.delete(*tree_anexo_summary.get_children())
    def get_detail_anexo(id_anexo):
        if not id_anexo:
            messagebox.showerror("", "Ingrese un anexo")
            return
        clean_detail()
        clean_anexo_summary()
        connection = sqlite3.connect(db_path)
        #get the remesas and details of the anexo
        try:            
            query_show_detail = f'''SELECT DISTINCT
                                        anexos_guias.guia_id, 
                                        COALESCE(remesas_guias.remesa_id, 'SIN REMESA') AS remesa_id, 
                                        COALESCE(anexos_guias.destino, 'SIN GUIA') AS destino, 
                                        COALESCE(anexos_guias.unds, 'N/A') AS unidades, 
                                        COALESCE(anexos_guias.peso, 'N/A') AS peso_Kg, 
                                        COALESCE(anexos_guias.valor, 'SIN GUIA') AS valor, 
                                        COALESCE(anexos_guias.tipo, 'SIN GUIA') AS tipo
                                    FROM 
                                        anexos_guias 
                                    LEFT JOIN 
                                        remesas_guias ON remesas_guias.guia_id = anexos_guias.guia_id 
                                    WHERE 
                                        anexos_guias.anexo_id = '{id_anexo}' 
                                    ORDER BY 
                                        remesas_guias.remesa_id DESC;
                                '''
            result = connection.execute(query_show_detail).fetchall()
            if not result:
                messagebox.showerror("", f"No se encontró el anexo {id_anexo}")
                return
            for row in result:
                row_list = list(row)
                row_list[5] = "{:,}".format(int(row_list[5]))
                tree_detail.insert("", "end", values=row_list)
        except Exception as e:
            messagebox.showerror("", f"Error al obtener las guias del anexo: {str(e)}")            
        
        #get the disctint remesas and the sum of values and total guias in the anexo of each remesa
        try:
            query_summary_anexo= f'''
                                    SELECT 
                                            COALESCE(remesa_id, 'SIN REMESA') AS remesa_id,
                                            COUNT(DISTINCT anexos_guias.guia_id) AS count_guias,
                                            SUM(anexos_guias.valor) AS suma_valores
                                        FROM 
                                            anexos_guias
                                            LEFT JOIN remesas_guias ON remesas_guias.guia_id = anexos_guias.guia_id
                                        WHERE 
                                            anexos_guias.anexo_id = '{id_anexo}'
                                        GROUP BY 
                                            remesa_id;
                                '''
            resultado = connection.execute(query_summary_anexo).fetchall()
            for row in resultado:
                row_list = list(row)
                row_list[2] = "{:,}".format(int(row_list[2]))
                tree_anexo_summary.insert("", "end", values=row_list)
        except Exception as e:
            messagebox.showerror("", f"Error al obtener datos del anexo: {str(e)}")
            connection.close()
        finally:
            connection.close()
        for item in tree_search.get_children():
            if  tree_search.item(item, "values")[0] == id_anexo:
                tree_search.selection_set(item)
                tree_search.see(item)      
    def on_double_click(event):
        item = event.widget.selection()[0]
        id_anexo = event.widget.item(item)["values"][0]
        get_detail_anexo(id_anexo)        
        entry_search_anexo.delete(0, tk.END)
        entry_search_anexo.insert(0, id_anexo)   
    def btnsearch_anexos(id_anexo):
        id_anexo = entry_search_anexo.get().strip()
        clean_detail()
        clean_anexo_summary()
        get_detail_anexo(id_anexo)
    def get_guia_detail(id_guia):
        if not id_guia:
            messagebox.showerror("", "Ingrese un guia")
            return
        try: 
            connection = sqlite3.connect(db_path)
            query_show_guia = f'''                                   
                                SELECT DISTINCT
                                rg.remesa_id, 
                                ag.anexo_id, 
                                ag.destino, 
                                COALESCE(ag.unds, 'SIN GUIA') AS unds,
                                COALESCE(ag.peso, 'SIN GUIA') AS peso,
                                ag.valor,
                                ag.tipo
                                FROM anexos_guias AS ag
                                LEFT JOIN remesas_guias as rg USING (guia_id)
                                WHERE ag.guia_id = '{id_guia}'
                                '''
            result = connection.execute(query_show_guia).fetchall()
            if not result:
                messagebox.showerror("", f"No se encontró la guia {id_guia}")
                return
            
            list_entries = [entry_remesa, entry_anexo, entry_destino, entry_unidades, entry_peso, entry_valor]
            for entry in list_entries:
                entry.config(state="normal")
                entry.delete(0, tk.END)

            for row in result:
                entry_remesa.insert(0, row[0])
                entry_anexo.insert(0, row[1])
                entry_destino.insert(0, row[2])
                entry_unidades.insert(0, row[3])
                entry_peso.insert(0, row[4])
                entry_valor.insert(0, "{:,}".format(row[5]))

            for entry in list_entries:
                entry.config(state="readonly")
            connection.close()
        except Exception as e:
            messagebox.showerror("", f"Error al obtener la guia: {str(e)}")
            connection.close()
        finally:
            connection.close()

    #Create the search frame
    frame_search_anexos = ttk.Frame(tab_anexos)
    frame_search_anexos.grid(row=0, column=0, sticky="wens", )
    frame_search_anexos.grid_columnconfigure(0, weight=1)
    frame_search_anexos.grid_columnconfigure(1, weight=1)
    frame_search_anexos.grid_rowconfigure(0, weight=1)
    frame_search_anexos.grid_rowconfigure(1, weight=0)
    
        
    frame_anexo_selected = ttk.Frame(frame_search_anexos)
    frame_anexo_selected.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")
    frame_anexo_selected.grid_columnconfigure(0, weight=1)
    frame_anexo_selected.grid_rowconfigure(0, weight=1)
    
    # Create the detail treeview
    tree_search = ttk.Treeview(frame_anexo_selected, height=25, show="headings", selectmode="browse")
    tree_search.grid(row=0, column=0, columnspan=6, sticky="nswe", padx=10, pady=10)

    # Define columns
    tree_search["columns"] = ("ID Anexo", "Fecha Anexo", "Total Unidades", "Total Guias", "FTE Total")

    # Format columns
    tree_search.column("#0", width=0, stretch=tk.NO)
    tree_search.column("ID Anexo", width=100, anchor="center")
    tree_search.column("Fecha Anexo", width=100, anchor="center")
    tree_search.column("Total Unidades", width=100, anchor="center")
    tree_search.column("Total Guias", width=100, anchor="center")
    tree_search.column("FTE Total", width=100, anchor="center",)
    
    # Create headings
    tree_search.heading("#0", text="")
    tree_search.heading("ID Anexo", text="Anexo")
    tree_search.heading("Fecha Anexo", text="Fecha Anexo")
    tree_search.heading("Total Unidades", text="Total Unidades")
    tree_search.heading("Total Guias", text="Total Guias")
    tree_search.heading("FTE Total", text="Total")
    # Bind the function get_detail_anexo to the treeview
    tree_search.bind("<ButtonRelease-1>", lambda event: on_double_click(event))
    # tree_search.bind("<Double-1>", on_double_click)

    # Add a scrollbar to the treeview
    scrollbar_detail = ttk.Scrollbar(frame_anexo_selected, bootstyle = 'primary-round', orient="vertical", command=tree_search.yview) # type: ignore
    scrollbar_detail.grid(row=0, column=4, sticky="ns")
    tree_search.configure(yscrollcommand=scrollbar_detail.set)
    
    frame_search_anexos_info = ttk.Frame(frame_search_anexos)
    frame_search_anexos_info.grid(row=1, column=0, padx=10, pady=10, sticky="nswe")        
    # Create the search anexo section

    entry_remesa= ttk.Entry(frame_search_anexos_info, state="readonly")
    entry_remesa.grid(row=3, column=1, padx=5, pady=5, sticky="we",)
    entry_remesa.config(justify="center")
    ttk.Label(frame_search_anexos_info, text="Remesa:").grid(row=4, column=1, padx=5, pady=5, sticky="")

    entry_anexo = ttk.Entry(frame_search_anexos_info, state="readonly")
    entry_anexo.grid(row=3, column=2, padx=5, pady=5, sticky="we") 
    entry_anexo.config(justify="center")
    ttk.Label(frame_search_anexos_info, text="Anexo:").grid(row=4, column=2, padx=5, pady=5, sticky="")

    entry_destino = ttk.Entry(frame_search_anexos_info, state="readonly")
    entry_destino.grid(row=3, column=3, padx=5, pady=5, sticky="we")
    entry_destino.config(justify="center")
    ttk.Label(frame_search_anexos_info, text="Destino:").grid(row=4, column=3, padx=5, pady=5, sticky="")

    entry_unidades = ttk.Entry(frame_search_anexos_info, state="readonly")
    entry_unidades.grid(row=3, column=4, padx=5, pady=5, sticky="we")
    entry_unidades.config(justify="center")
    ttk.Label(frame_search_anexos_info, text="Uds:").grid(row=4, column=4, padx=5, pady=5, sticky="")

    entry_peso = ttk.Entry(frame_search_anexos_info, state="readonly")
    entry_peso.grid(row=3, column=5, padx=5, pady=5, sticky="we")
    entry_peso.config(justify="center")
    ttk.Label(frame_search_anexos_info, text="Peso:").grid(row=4, column=5, padx=5, pady=5, sticky="")

    entry_valor = ttk.Entry(frame_search_anexos_info, state="readonly")
    entry_valor.grid(row=3, column=6, padx=5, pady=5, sticky="we")
    entry_valor.config(justify="center")
    ttk.Label(frame_search_anexos_info, text="Valor:", justify='center').grid(row=4, column=6, padx=5, pady=5, sticky="", )

    label_search = ttk.Label(frame_search_anexos_info, text="Anexo:")
    label_search.grid(row=1, column=0, padx=5, pady=5, sticky="")

    entry_search_anexo = ttk.Entry(frame_search_anexos_info)
    entry_search_anexo.grid(row=1, column=1, padx=5, pady=5, sticky="we")
    entry_search_anexo.config(justify="center")
    entry_search_anexo.bind("<Return>", lambda event: btnsearch_anexos(entry_search_anexo.get().strip()))

    btn_search = ttk.Button(frame_search_anexos_info, text="Buscar", command= lambda: btnsearch_anexos(entry_search_anexo.get()))
    btn_search.grid(row=1, column=2, padx=5, pady=5, sticky="we")
    
    btn_delete = ttk.Button(frame_search_anexos_info, text="Elminar Anexo", style='Danger', command= lambda: delete_anexo())
    btn_delete.grid(row=1, column=3, padx=5, pady=5, sticky="we")
    
    # Create the search guias section

    ttk.Label(frame_search_anexos_info, text="Guia:").grid(row=2, column=0, padx=5, pady=5, sticky="")

    entry_search_guia = ttk.Entry(frame_search_anexos_info)
    entry_search_guia.grid(row=2, column=1, padx=5, pady=5, sticky="we")
    entry_search_guia.config(justify="center")
    entry_search_guia.bind("<Return>", lambda event: get_guia_detail(entry_search_guia.get().strip()))

    btn_search_guia = ttk.Button(frame_search_anexos_info, text="Buscar", command= lambda: get_guia_detail(entry_search_guia.get()))
    btn_search_guia.grid(row=2, column=2, padx=5, pady=5, sticky="we")
    
    frame_cant_remesas = ttk.Frame(frame_search_anexos)
    frame_cant_remesas.grid(row=1, column=1, padx=10, pady=10, sticky="we")
    
    label_remesas = ttk.Label(frame_cant_remesas, text="Remesas en el anexo: ")
    label_remesas.grid(row=0, column=0, padx=10, pady=5, sticky="we")
    
    list_camps = ("Remesa", "Guias", "Valor")
    tree_anexo_summary = ttk.Treeview(frame_cant_remesas, columns=list_camps, height=7, show="headings", selectmode="browse")
    tree_anexo_summary.grid(row=1, column=0, sticky="w", padx=10, pady=0)

    for col in list_camps:
        tree_anexo_summary.heading(col, text=col)
        tree_anexo_summary.column(col, width=100, stretch=True, anchor="center")
    
    scrollbar_summary = ttk.Scrollbar(frame_cant_remesas, bootstyle = 'primary-round', orient="vertical", command=tree_anexo_summary.yview) # type: ignore
    scrollbar_summary.grid(row=1, column=1, sticky="ns")
    tree_anexo_summary.configure(yscrollcommand=scrollbar_summary.set)
    
#********************************************************************************************************************    
#****************************************DETAIL_SIDE_ANEXOS**********************************************************    
#********************************************************************************************************************
    
    frame_detail = ttk.Frame(frame_search_anexos)
    frame_detail.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")
    frame_detail.grid_columnconfigure(0, weight=1)
    frame_detail.grid_rowconfigure(0, weight=1)

    # Create the detail treeview
    tree_detail = ttk.Treeview(frame_detail, height=25, show="headings",  selectmode="browse", name="tree_detail")
    tree_detail.grid(row=0, column=0, columnspan=4, sticky="nswe", padx=10, pady=10)

    # Define columns
    tree_detail["columns"] = ("guia", "remesa", "destino","unidades", "peso", "valor", "tipo")

    # Format columns
    tree_detail.column("guia", width=100, anchor="center")
    tree_detail.column("remesa", width=100, anchor="center")
    tree_detail.column("destino", width=100, anchor="center")    
    tree_detail.column("unidades", width=50, anchor="center")
    tree_detail.column("peso", width=50, anchor="center")
    tree_detail.column("valor", width=80, anchor="center")
    tree_detail.column("tipo", width=80, anchor="center")

    # Create headings
    tree_detail.heading("guia", text="Guia")
    tree_detail.heading("remesa", text="Remesa")
    tree_detail.heading("destino", text="Destino")
    tree_detail.heading("unidades", text="Uds")
    tree_detail.heading("peso", text="Peso")
    tree_detail.heading("valor", text="FTE Total")
    tree_detail.heading("tipo", text="Tipo")

    # Add a scrollbar to the treeview
    scrollbar_detail = ttk.Scrollbar(frame_detail, bootstyle = 'primary-round', orient="vertical", command=tree_detail.yview) # type: ignore
    scrollbar_detail.grid(row=0, column=4, sticky="ns")
    tree_detail.configure(yscrollcommand=scrollbar_detail.set)
    
    tab_anexos.add(frame_search_anexos, text="Buscar Anexos")
    get_anexos()
    focus_tab(tab_anexos)