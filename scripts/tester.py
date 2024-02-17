import os




input = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Liquidaciones\120. Liquidation-品牌-8F  柜号 CXRU-1413703.xlsx"

print(os.path.isdir(input) or input.lower().endswith(".pdf") or input.lower().endswith(".xlsx") or input.lower().endswith(".xls"))