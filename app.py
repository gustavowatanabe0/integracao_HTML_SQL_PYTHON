#import do flask para criação do servidor
#render_template para criar uma "ponte" com html
#request para capturar dados digitados
from flask import Flask, render_template, request
import mysql.connector

#"Ajuda" o Flask a localizar o caminhos dos arquivos
app = Flask(__name__)

db_config = {
    'host':'localhost',
    'user':'root',
    'password':'escola',
    'database':'cadastro'
}

#Criando a rota para acessar o arquivo HTML
@app.route('/')
def index():
    return render_template('index.html')

#Criando a rota para acessar o formulário
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    cpf = request.form['cpf']
