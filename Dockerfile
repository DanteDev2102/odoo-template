FROM odoo:17.0

USER root
COPY . .

RUN chmod +x /entrypoint.sh


RUN python3 -m pip install -r requirements.txt
