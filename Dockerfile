FROM odoo:17.0

USER odoo
COPY . .

RUN python3 -m pip install -r requirements.txt
