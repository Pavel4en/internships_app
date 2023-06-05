from flask import Flask, session
from flask_mail import Mail

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['MAIL_SERVER'] = 'SMTP.yandex.ru'  
app.config['MAIL_PORT'] = 465  
app.config['MAIL_USE_TLS'] = True  
app.config['MAIL_USERNAME'] = 'birzha.stazher'  
app.config['MAIL_PASSWORD'] = '123456789birzha'  
mail = Mail(app)
import controllers.index
