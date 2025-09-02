from flask import Flask, render_template, request, jsonify, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Carregar dados do Excel
def carregar_dados():
    try:
        df = pd.read_excel('1.xlsx')
        return df
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/verificar_senha', methods=['POST'])
def verificar_senha():
    senha_digitada = request.json.get('senha')
    senha_correta = "10170370"
    
    if senha_digitada == senha_correta:
        session['autenticado'] = True
        return jsonify({'sucesso': True, 'mensagem': 'Acesso autorizado. Iniciando sistema...'})
    else:
        return jsonify({'sucesso': False, 'mensagem': 'Acesso negado.'})

@app.route('/carregar_dados')
def carregar_dados_route():
    if not session.get('autenticado'):
        return jsonify({'erro': 'Não autorizado'}), 401
    
    df = carregar_dados()
    if df is None:
        return jsonify({'erro': 'Não foi possível carregar o arquivo'}), 500
    
    # Obter categorias únicas
    categorias_unicas = set()
    for col in df.columns:
        if col.startswith('subject'):
            valores = df[col].dropna().unique()
            categorias_unicas.update(valores)
    
    categorias_lista = sorted(list(categorias_unicas))
    
    # Converter DataFrame para formato JSON, substituindo NaN por null
    import json
    dados_json = json.loads(df.to_json(orient='records', date_format='iso'))
    
    return jsonify({
        'colunas': list(df.columns),
        'categorias': categorias_lista,
        'dados': dados_json,
        'total_registros': len(df),
        'total_campos': len(df.columns)
    })

@app.route('/buscar_codigos', methods=['POST'])
def buscar_codigos():
    if not session.get('autenticado'):
        return jsonify({'erro': 'Não autorizado'}), 401
    
    categorias_selecionadas = request.json.get('categorias', [])
    
    if not categorias_selecionadas:
        return jsonify({'erro': 'Nenhuma categoria selecionada'}), 400
    
    df = carregar_dados()
    if df is None:
        return jsonify({'erro': 'Não foi possível carregar o arquivo'}), 500
    
    codigos_encontrados = []
    
    for idx, row in df.iterrows():
        categorias_presentes = set()
        
        for col in df.columns:
            if col.startswith('subject') and pd.notna(row[col]):
                categorias_presentes.add(row[col])
        
        if set(categorias_selecionadas) == categorias_presentes:
            codigos_encontrados.append(row['code'])
    
    return jsonify({
        'codigos': codigos_encontrados,
        'total_encontrados': len(codigos_encontrados),
        'categorias_buscadas': categorias_selecionadas
    })

@app.route('/logout')
def logout():
    session.pop('autenticado', None)
    return jsonify({'sucesso': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
