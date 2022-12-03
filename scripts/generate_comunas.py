import requests
import json
url_regiones = "https://testservices.wschilexpress.com/georeference/api/v1.0/regions"

url = "https://testservices.wschilexpress.com/georeference/api/v1.0/coverage-areas?RegionCode={}&type=0"
header = {
            'Content-Type':'application/json',
            'Cache-Control':'no-cache',
            'Ocp-Apim-Subscription-Key':'902f6e7fd36f4549b5145bb50e1f866a'
        }
print("Generando XML...")
with open("comunas.xml","w") as f:
    f.write("<?xml version='1.0' encoding='utf-8'?>\n<odoo>")
    region_codes = []
    y = requests.get(url_regiones, headers=header)
    response = json.loads(y.text)
    for item in response["regions"]:
        x = requests.get(url.format(item["regionId"]), headers=header)
        response = json.loads(x.text)
        record_text  ="""
<record id="{}" model="res.comuna">
    <field name="name">{}</field>
    <field name="region">{}</field>
    <field name="comuna_id">{}</field>
</record>
        """
        for item in response["coverageAreas"]:
            #print(record_text.format(item["countyCode"],item["countyName"], item["regionCode"]))
            f.write(record_text.format(item["countyCode"],item["countyName"], item["regionCode"],item["countyCode"]))
        f.write("</odoo>")