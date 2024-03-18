import tabula
import pandas as pd
import pdfplumber


full_table =[]
with pdfplumber.open('anexo2024_2.pdf') as pdf:
    # Iterar sobre las páginas del PDF
    total_pages = len(pdf.pages)
    last_page = total_pages - 1
    text = pdf.pages[last_page].extract_text()
    # print(text)
    for page in pdf.pages:
        # Extraer todas las tablas de la página
        tables = page.extract_tables()
        
        # Iterar sobre las tablas extraídas
        for table in tables:
            # Omitir la primera fila (suponiendo que es la fila de encabezados)
            table_data = table[2:]  # Comenzar desde la segunda fila
            
            # Agregar las filas de la tabla (sin los encabezados) a la lista
            full_table.extend(table_data)
# print(full_table)

df = pd.DataFrame(full_table)
df = df.dropna(axis=1, how='all')
df.columns = ['GUIA', 'PRODUCTO', 'DESTINO', 'UDS', 'PESO', 'FTE FIJO', 'FTE VARIABLE', 'FTE TOTAL', 'TIPO'] 
df[6] = pd.to_numeric(df[6], errors='coerce')

sum_items = df.iloc[:,3].sum()
print(df)