
import pandas as pd
import os
def pregunta_01():

    # Crear el directorio de salida si no existe
    os.makedirs('files/output', exist_ok=True)

    # Cargar el archivo de datos
    dataset = pd.read_csv('files/input/solicitudes_de_credito.csv', sep=';', index_col=0)

    # Eliminar filas con datos faltantes
    dataset = dataset.dropna()

    # columnas
    dataset['sexo'] = dataset['sexo'].str.lower()
    dataset['tipo_de_emprendimiento'] = dataset['tipo_de_emprendimiento'].str.lower()
    dataset['idea_negocio'] = dataset['idea_negocio'].str.lower()
    dataset['barrio'] = dataset['barrio'].str.lower()
    dataset['línea_credito'] = dataset['línea_credito'].str.lower()

    # limpiar columnas
    dataset['barrio'] = dataset['barrio'].str.replace('_', ' ').str.replace('-', ' ')
    dataset['idea_negocio'] = dataset['idea_negocio'].str.replace('_', ' ').str.replace('-', ' ')
    dataset['línea_credito'] = dataset['línea_credito'].str.replace('_', ' ').str.replace('-', ' ')

    # Limpiar el campo de monto 
    dataset['monto_del_credito'] = dataset['monto_del_credito'].str.replace('$', '', regex=False)
    dataset['monto_del_credito'] = dataset['monto_del_credito'].str.replace(',', '', regex=False)
    dataset['monto_del_credito'] = dataset['monto_del_credito'].str.replace('.00', '', regex=False)
    dataset['monto_del_credito'] = dataset['monto_del_credito'].str.strip()
    dataset['monto_del_credito'] = pd.to_numeric(dataset['monto_del_credito'])

    # Procesar las fechas
    dataset['fecha_aux'] = pd.to_datetime(dataset['fecha_de_beneficio'], 
                                          dayfirst=True, 
                                          format='%d/%m/%Y', 
                                          errors='coerce')

    fechas_invalidas = dataset['fecha_aux'].isna()
    if fechas_invalidas.any():
        dataset.loc[fechas_invalidas, 'fecha_aux'] = pd.to_datetime(
            dataset.loc[fechas_invalidas, 'fecha_de_beneficio'],
            format='%Y/%m/%d',
            errors='coerce'
        )

    dataset['fecha_de_beneficio'] = dataset['fecha_aux'].dt.strftime('%Y-%m-%d')
    dataset = dataset.drop('fecha_aux', axis=1)

    # Eliminar filas con fechas no válidas y duplicados
    dataset = dataset.dropna()
    dataset = dataset.drop_duplicates()

    
    dataset.to_csv('files/output/solicitudes_de_credito.csv', sep=';')

    return dataset
print(pregunta_01())
