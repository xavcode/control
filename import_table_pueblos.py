from datetime import datetime
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import os
import sqlite3

import config

# Lee la tabla de Excel

def import_remesa_from_excel():
   
    
    file_path = r"I:\RELACION PUEBLOS 2024.xlsm"

    if not os.path.exists(file_path):
        messagebox.showerror(
            "", "No se encontró el archivo"
        )
        return
    if file_path:        
        df = pd.read_excel(
            f"{file_path}", header=None, sheet_name="plantilla_remesa"
        )
        
        # # Check if the last row contains the word "Total"
        # #if ther is title has a header, is removed
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
        print(id_remesa)
        
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
        
        destino = f"{df.iat[0, 5].upper().strip()}"
        
        if not destino.endswith('(NAR)'):
            destino = f"{destino} (NAR)"
        
        if destino == 'PIEDRANCHA (NAR)':
            destino = 'PIEDRAHANCHA (NAR)'
       
        
        guias = df.values.tolist()
        guias = [row[1:] for row in guias]
        # print(guias)
        
        connection = sqlite3.connect(config.db_path)
        
        cursor = connection.cursor()
        try:            
            query = f'''    
                        INSERT INTO 'remesas'(
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
                        VALUES ('{id_remesa}', '{manifiesto}', '{conductor}', '{destino}', '{formated_date}', {uds_sum}, {kg_sum}, {0}, {cobro_sum}, {valor_sum}, {valor_sum}, {0}, {0}, {0});
                    '''
            print(query)
            cursor.execute(query)
            for guia in guias:
                cursor.execute(f"INSERT INTO remesas_guias (remesa_id, guia_id, valor) VALUES ('{id_remesa}', '{guia[0]}', {guia[6]}) ")
            
            connection.commit()            
            messagebox.showinfo("", f"Remesa {id_remesa} guardada correctamente")
            
        except Exception as e:
            connection.rollback()
            if 'UNIQUE' in str(e):
                messagebox.showerror("Error", f"La remesa {id_remesa} ya existe")
            else:
                messagebox.showerror("Error", f"Ocurrió un error al guardar la remesa: {str(e)}")
        connection.close()

root = tk.Tk()
root.withdraw()

import_remesa_from_excel()