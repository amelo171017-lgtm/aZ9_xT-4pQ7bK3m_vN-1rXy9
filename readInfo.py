import pandas as pd
import sys
import os

def verificar_senha():
    senha_correta = "10170370"
    senha_digitada = input("Digite a senha: ")
    
    if senha_digitada == senha_correta:
        print("Acesso autorizado. Iniciando sistema...")
        return True
    else:
        print("Acesso negado.")
        return False

def ler_excel():
    try:
        df = pd.read_excel('1.xlsx')
        print("Arquivo carregado com sucesso!")
        print(f"Colunas encontradas: {list(df.columns)}")
        print("\n" + "="*80)
        print("DADOS COMPLETOS:")
        print("="*80)
        print(df.to_string(index=False))
        print("="*80)
        print(f"Total de registros: {len(df)}")
        print(f"Total de campos: {len(df.columns)}")
        print("="*80)
        return df
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        return None

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def criar_interface_terminal(df):
    categorias_unicas = set()
    for col in df.columns:
        if col.startswith('subject'):
            valores = df[col].dropna().unique()
            categorias_unicas.update(valores)
    
    categorias_lista = sorted(list(categorias_unicas))
    categorias_selecionadas = {categoria: False for categoria in categorias_lista}
    posicao_atual = 0
    
    while True:
        limpar_tela()
        
        print("=" * 60)
        print("        SELEÇÃO DE CATEGORIAS")
        print("=" * 60)
        print()
        print("Navegação: SETAS ↑↓ | Seleção: ESPAÇO | Busca: ENTER | Sair: ESC")
        print()
        print("-" * 60)
        
        for i, categoria in enumerate(categorias_lista):
            cursor = " > " if i == posicao_atual else "   "
            checkbox = "[X]" if categorias_selecionadas[categoria] else "[ ]"
            print(f"{cursor}{checkbox} {categoria}")
        
        print("-" * 60)
        print()
        
        try:
            import msvcrt
            tecla = msvcrt.getch()
            
            if tecla == b'\xe0':
                tecla2 = msvcrt.getch()
                
                if tecla2 == b'H':
                    posicao_atual = (posicao_atual - 1) % len(categorias_lista)
                elif tecla2 == b'P':
                    posicao_atual = (posicao_atual + 1) % len(categorias_lista)
                    
            elif tecla == b' ':
                categoria_atual = categorias_lista[posicao_atual]
                categorias_selecionadas[categoria_atual] = not categorias_selecionadas[categoria_atual]
                
            elif tecla == b'\r':
                obter_codigos(df, categorias_selecionadas)
                input("\nPressione ENTER para continuar...")
                
            elif tecla == b'\x1b':
                print("\nEncerrando...")
                break
                
        except ImportError:
            print("Sistema não suporta entrada direta de teclas.")
            break

def obter_codigos(df, categorias_selecionadas):
    limpar_tela()
    
    print("=" * 60)
    print("              RESULTADOS DA BUSCA")
    print("=" * 60)
    print()
    
    categorias_ativas = [categoria for categoria, selecionada in categorias_selecionadas.items() if selecionada]
    
    if not categorias_ativas:
        print("❌ Nenhuma categoria selecionada!")
        return
    
    print(f"✅ Categorias selecionadas: {len(categorias_ativas)}")
    for categoria in categorias_ativas:
        print(f"   • {categoria}")
    
    print()
    print("-" * 60)
    
    codigos_encontrados = []
    
    for idx, row in df.iterrows():
        categorias_presentes = set()
        
        for col in df.columns:
            if col.startswith('subject') and pd.notna(row[col]):
                categorias_presentes.add(row[col])
        
        if set(categorias_ativas) == categorias_presentes:
            codigos_encontrados.append(row['code'])
    
    if len(codigos_encontrados) > 0:
        print(f"📊 Total de códigos encontrados: {len(codigos_encontrados)}")
        print()
        print("🔑 Códigos correspondentes:")
        print()
        
        for codigo in codigos_encontrados:
            print(f"   • {codigo}")
        
        print()
    else:
        print("❌ Nenhum código encontrado para as categorias selecionadas!")
        print()
        print("💡 Dica: Tente selecionar menos categorias para ampliar os resultados.")
    
    print("=" * 60)

def main():
    print("=== Sistema de Consulta ===")
    
    if not verificar_senha():
        print("Programa encerrado.")
        return
    
    df = ler_excel()
    if df is None:
        print("Não foi possível carregar o arquivo.")
        return
    
    criar_interface_terminal(df)

if __name__ == "__main__":
    main()
