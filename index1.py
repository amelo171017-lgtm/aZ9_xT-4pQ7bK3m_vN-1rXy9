import itertools
import pandas as pd
import random
import string

def gerar_codigo(prefixo, indice):
    """Gera um código com prefixo do grupo e sufixo aleatório"""
    sufixo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
    return f"{prefixo}{indice:03d}{sufixo}"

def gerar_combinacoes(subjects, tlinks, alinks, output_file="combinacoes.xlsx"):

    todas = []
    for r in range(1, len(subjects) + 1):
        todas.extend((r, c) for c in itertools.combinations(range(len(subjects)), r))

    linhas = []
    contadores = {r: 1 for r in range(1, len(subjects) + 1)}  # contador por grupo

    for r, combinacao in todas:
        prefixo = f"S{r}"
        idx = contadores[r]
        contadores[r] += 1

        linha = {"code": gerar_codigo(prefixo, idx)}  # código diferenciado por grupo

        # preencher as colunas
        for posicao, idx_sub in enumerate(combinacao, start=1):
            linha[f"subject{posicao}"] = subjects[idx_sub]
            linha[f"tlink{posicao}"] = tlinks[idx_sub]
            linha[f"alink{posicao}"] = alinks[idx_sub]

        # garantir que todas as colunas existam até subject6
        for posicao in range(len(combinacao) + 1, 7):
            linha[f"subject{posicao}"] = ""
            linha[f"tlink{posicao}"] = ""
            linha[f"alink{posicao}"] = ""

        linhas.append(linha)

    # cria DataFrame e exporta para Excel
    df = pd.DataFrame(linhas)
    df.to_excel(output_file, index=False)
    print(f"Arquivo gerado: {output_file}")


if __name__ == "__main__":
    # exemplo de uso
    subjects = ["natureza", "humanas", "matematica", "linguagens", "educacao_fisica", "redacao"]
    tlinks = [
        "https://drive.google.com/file/d/1ROxyE66_B0OQlSwFby1SIulsUE_aExNg/view?usp=drive_link",
        "https://drive.google.com/file/d/1dLud0D6AGrW81MGpRxgb9_lkreDxLviq/view?usp=drive_link",
        "https://drive.google.com/file/d/1K-D7ey1ko8vKfUTPLGDi1tA0FnbOymux/view?usp=drive_link",
        "https://drive.google.com/file/d/1EV4du_axzMUEx3y9LXzxLD4k7OU7oyPz/view?usp=drive_link",
        "https://drive.google.com/file/d/1KZ8LqRquj09ecaPIfxewihxxnY6txfzn/view?usp=drive_link",
        "https://drive.google.com/file/d/14VY-mdDCJOpqB6p1dZQjgVYwm04TLwLr/view?usp=drive_link"
    ]
    alinks = [
        "https://drive.google.com/file/d/1GqLlSMjLFW_ESFn0TbY9KCf77ceoCQY8/view?usp=drive_link",
        "https://drive.google.com/file/d/1mwhrTpprcm2HrTBXzKHzWiBhNqKopmY_/view?usp=drive_link",
        "https://drive.google.com/file/d/1TBEc50gkwNG7vuPkLga7iM7A5DqaugdI/view?usp=drive_link",
        "https://drive.google.com/file/d/1wRI5bDwDTAgR9tyDpCKKcH3PjsyT1uBi/view?usp=drive_link",
        "https://drive.google.com/file/d/170YnHsPmkXgtt_3Mt4w7W1IK30dDFz0H/view?usp=drive_link",
        ""
    ]

    gerar_combinacoes(subjects, tlinks, alinks, "1.xlsx")
