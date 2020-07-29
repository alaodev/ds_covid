from flask import Flask
from flask_mysqldb import MySQL
from flask_googlecharts import GoogleCharts

app = Flask(__name__)
app.config.from_object('conf')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'covid'

mysql = MySQL(app)

charts = GoogleCharts()
charts.init_app(app)

from app.controllers import rotas