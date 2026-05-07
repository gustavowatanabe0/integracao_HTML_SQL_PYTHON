from flask import Flask, render_template, redirect, url_for, request
import mysql.connector

app = Flask(__name__)

db_config = {
    'host':'localhost',
    'user':'root',
    'password':'escola',
    'database':'cadastro'
}

@app.route('/')
def index():
    try:
        conectar = mysql.connector.connect(**db_config)
        cursor = conectar.cursor(dictionary=True)

        cursor.execute("SELECT ID,NOME,TAMANHO,CATEGORIA,QUANTIDADE from produto")
        lista_produtos = cursor.fetchall()

        cursor.close()
        conectar.close()
        return render_template('index.html', produtos=lista_produtos)
    
    except mysql.connector.Error as err:
        return f"Erro ao carregar a tabela: {err}"
    
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    id = request.form['id']
    nome = request.form['nome']
    tamanho = request.form['tamanho']
    categoria = request.form['categoria']
    quantidade = request.form['quantidade']

    try:
        conectar = mysql.connector.connect(**db_config)
        cursor = conectar.cursor()
        query = "INSERT INTO produto(ID,NOME,TAMANHO,CATEGORIA,QUANTIDADE) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(query,(id,nome,tamanho,categoria,quantidade))

        conectar.commit()
        cursor.close()
        conectar.close()

        return f"<h3>Produto {nome} salvo com sucesso!</h3> <a href='/'>Voltar</a>"

    except mysql.connector.Error as err:
        return f"Erro ao gravar no banco: {err}"