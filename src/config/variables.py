"""
El objetivo de este arhivo es mantener todas las variables globales del programa.
"""

import os
import sys

# Datos personales:
email = "sebastian.pincheira@ug.uchile.cl"
telefono = "+56 9 8918 6914"

# Colores:
title = {
    "main": "Ocho Fuegos - Automatización de procesos corporativos",
    "info1": "Info1 - Información",
}

bg = {
    "window": "#000739",
    "?": "#DDDDDD",
    "output_button": "#001693",
    "exit_button": "#A00000",
    "window_text": "#000739",
}
bg_on_enter = {"?": "#FCFF45", "output_button": "#000D56", "exit_button": "#6B0000"}
fg = {
    "window": "#DDDDDD",
    "output_button": "#FFFFFF",
    "exit_button": "#FFFFFF",
    "window_text": "#DDDDDD",
}
activebackground = {"output_button": "#DDDDDD", "exit_button": "#DDDDDD"}
activeforeground = fg
font = {"?": 8, "output_button": 40, "exit_button": 40}


# Diccionarios de traducción:

# Diccionario para ventas:
embarquesDict = {  # Traducción de embarques
    "DepartureWeek": "ETD WEEK",
    "ExporterName": "EXPORTADOR",
    "DispatchInstructiveCode": "INSTRUCTIVO",
    "ReceiverName": "CLIENTE",
    "ConsigneeName": "CONSIGNATARIO",
    "BillCode": "FACTURA PROFORMA",
    "BillDate": "FECHA FACTURA",
    "BillTypeAsString": "MODALIDAD DE VENTA",
    "IncotermCode": "INCOTERM",
    "PackingSiteName": "PACKING",
    "DispatchCode": "GUIA DESPACHO",
    "DispatchDate": "FECHA DESPACHO PLANTA",
    "GrowerName": "PRODUCTOR",
    "GrowerCSG": "CSG",
    "PackingDate": "FECHA EMBALAJE",
    "PalletCode": "FOLIO",
    "SpeciesName": "ESPECIE",
    "VarietyName": "VARIEDAD",
    "CaliberName": "CALIBRES",
    "PackageCode": "CODIGO EMBALAJE",
    "PackageNetWeight": "KG NET/CAJA",
    "PackageGrossWeight": "BRUTOS/CAJA",
    "Quantity": "CAJAS",
    "Pallets": "PALLETS",
    "NetWeight": "NETOS",
    "GrossWeight": "BRUTOS",
    "VesselTypeAsString": "TIPO DE EMBARQUE",
    "VesselName": "NAVE",
    "DeparturePortName": "PUERTO EMBARQUE",
    "ArrivalContinentAsString": "MERCADO",
    "ArrivalCountryName": "PAIS DESTINO",
    "ArrivalPortName": "PUERTO DESTINO",
    "BillBL": "AWB - BL",
    "VesselVoyageNumber": "VOYAGE NUMBER",
    "BillBooking": "BOOKING",
    "ContainerCode": "CONTENEDOR",
    "VesselCompanyName": "LINEA AEREA/NAVIERA",
    "ShipperName": "EMBARCADOR",
    "DepartureDate": "ETD",
    "ETA": "ETA",
    "BillDUS": "DUS",
    "ArrivalDate": "ETA REAL",
}

# color en diccionario de color (En parametros)
# "COD PUERTO EMBARQUE", "COD PUERTO DESTINO" (en parametros)


facturasDict = {
    "SiiReceptor_Name": "CONSIGNATARIO",
    "Bill_Code": "FACTURA PROFORMA",
    "LabeledVariety_Name": "VARIEDAD",
    "Package_Code": "CODIGO EMBALAJE",
    "Caliber_Name": "CALIBRES",
    "ExchangeRateToCLP": "TC Factura",
    "UnitFOB": "FACT PROFORMA $/CAJA",
}


# Diccionario para tarifas:
tarifaDict = {
    "Code": "INSTRUCTIVO",
    "SPS": "SPS",
    "FreightCost": "FLETE/kg",
}


# Keys de los dataframes de ventas (base embarques con facturas proformas):
key_columns = [
    "CONSIGNATARIO",
    "FACTURA PROFORMA",
    "VARIEDAD",
    "CODIGO EMBALAJE",
    "CALIBRES",
]

# Keys para unir los dataframes de venta (precios_contrato y embarques/control)
key_precios_contrato = [
    "CALIBRES",
    "KG NET/CAJA",
    "ETD WEEK",
    "CLIENTE",
]

# Diccionario para la columna "COLOR" de venta.
cherry_color = {
    "LD": "DARK",
    "LDD": "DARK",
    "XLD": "DARK",
    "XLDD": "DARK",
    "JD": "DARK",
    "JDD": "DARK",
    "2JD": "DARK",
    "2JDD": "DARK",
    "3JD": "DARK",
    "3JDD": "DARK",
    "4JD": "DARK",
    "4JDD": "DARK",
    "L": "LIGHT",
    "XL": "LIGHT",
    "J": "LIGHT",
    "2J": "LIGHT",
    "3J": "LIGHT",
    "4J": "LIGHT",
    "J-UP": "LIGHT",
}


# COD PUERTO EMBARQUE
COD_PUERTO_EMBARQUE = {
    "AEROP.A.M.BENITEZ": "997",
    "San Antonio  STI": "208",
    "Los Libertadores": "965",
    "Valparaiso": "208",
}

# LIQUIDACIONES
# Diccionario para el main table de liquidacion_reader.py y liquidacion_interpreter.py
main_dict_liq = {  # 12Islands
    "Observacion": "Observacion",  # New
    "日期 Date": "FECHA VENTA",  # New
    "板号 Pallet No.": "FOLIO",  # Old
    "果园 CSG": "CSG",  # Old
    "品种 Variety": "VARIEDAD",  # Old
    "大小 Size": "CALIBRES",  # Old
    "数量 Quantity": "CAJAS LIQUIDADAS",  # New
    "规格 Specification": "KG NET/CAJA",  # Old
    "价格 (人民币) Price RMB": "RMB/CJ",  # New
    "总数 (人民币) Total RMB": "TOTAL RMB",  # New
    "总数 (美金) Total USD": "TOTAL USD",  # New
    "每箱收益 FOB FOB Return": "RETORNO FOB/CJ",  # New
    "总收益 FOB Total Return": "RETORNO FOB",  # New
}

# Diccionario para el main table de liquidacion_interpreter.py, liquidacion_standard.
main_dict_liq_standard = {  # Standard -> 12Islands
    "观察": "Observacion",  # New
    "日期": "日期 Date",  # New
    "版号": "板号 Pallet No.",  # Old
    "CSG": "果园 CSG",  # Old
    "品种": "品种 Variety",  # Old
    "尺寸": "大小 Size",  # Old
    "到货数量": "数量 Quantity",  # New
    "重量": "规格 Specification",  # Old
    "单价": "价格 (人民币) Price RMB",  # New
    "金额": "总数 (人民币) Total RMB",  # New
    "美金": "总数 (美金) Total USD",  # New
}


# Transforma de inglés a chino en interpreter_JF
main_dict_liq_JF = {  # JF -> Standard
    "Nota": "观察",
    "Sales Box": "到货数量",
    "Variety": "品种",
    "Pallet Nr.": "版号",
    "Weight": "重量",
    "Size": "尺寸",
    "Date": "日期",
    "Brand": "CSG",
    "Price": "单价",
    "Total（RMB）": "金额",
}

# Columnas necesarias para el formato HFF de liquidacion
main_list_liq_HFF = [
    "观察",
    "到货数量",
    "品种",
    "版号",
    "重量",
    "尺寸",
    "日期",
    "销售数量",
    "单价",
    "金额",
    "美金",
]

main_list_liq_HFF_SEA = {
    "观察": "观察",
    "到货数量": "到货数量",
    "品种": "品种",
    "版号": "版号",
    "重量": "重量",
    "规格": "尺寸",
    "销售日期": "日期",
    "销售数量": "销售数量",
    "单价": "单价",
    "金额": "金额",
    "美金": "美金",
    # "每箱收益 FOB FOB Return",
}

# key para el main table de liquidacion_reader.py. Se usa en los que tienen columna CSG en control_final para el merge
key_liq = ["FOLIO", "CSG", "VARIEDAD", "CALIBRES", "KG NET/CAJA"]

# key para el main table de liquidacion_reader.py. Se usa en los que no tienen columna CSG
key_liq_incompleto = ["FOLIO", "VARIEDAD", "CALIBRES", "KG NET/CAJA"]

# Los siguientes son los formatos de liquidaciones que usan CSG. Cualquier otro formato no lo usa.
# El nombre del formato tiene que ser aquel que se encuentra en la columan ReceiverName de base embarques.
# Es utilizado en embarques.py
formatos_con_CSG = ["HARVEST-TIME IMP & EXP CO., LIMITED"]

# Ubicación del programa en el dispositivo del usuario
directory = os.path.dirname(os.path.realpath(sys.argv[0]))
