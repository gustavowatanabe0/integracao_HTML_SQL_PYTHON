# NEW: Incluída a importação do 'flash' no final da linha
from flask import Flask, render_template, redirect, url_for, request, flash
import mysql.connector

app = Flask(__name__)

# NEW: Chave secreta obrigatória para usar o recurso de mensagens Flash
app.secret_key = 'chave_secreta_e_segura_do_projeto'

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

        # NEW: Cria a mensagem de sucesso categorizada como 'success'
        flash(f"Produto '{nome}' salvo com sucesso!", "success")
        
        # NEW: Substituído o HTML estático pelo redirecionamento para a página principal
        return redirect(url_for('index'))

    except mysql.connector.Error as err:
        # NEW: Cria uma mensagem de erro caso o banco falhe
        flash(f"Erro ao gravar no banco: {err}", "danger")
        return redirect(url_for('index'))
    
@app.route('/excluir/<id>')
def excluir(id):
    try:
        conectar = mysql.connector.connect(**db_config)
        cursor = conectar.cursor()
        cursor.execute("DELETE FROM produto WHERE ID = %s", [id])

        conectar.commit()
        cursor.close()
        conectar.close()

        # NEW: Cria a mensagem de aviso para exclusões
        flash("Produto excluído com sucesso!", "warning")
        return redirect(url_for('index'))
    
    except mysql.connector.Error as err:
        flash(f"Erro ao excluir: {err}", "danger")
        return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(debug=True)
