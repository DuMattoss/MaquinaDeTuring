import json
import sys

def carregar_maquina(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        dados = json.load(f)

    maquina = {
        "estado_inicial": None,
        "finais": [],
        "branco": None,
        "transicoes": {}
    }

  
    if "transitions_count" in dados:
        maquina["estado_inicial"] = dados["initial"]
        maquina["finais"] = [dados["final_0"]]
        maquina["branco"] = dados["white"]

        for i in range(dados["transitions_count"]):
            de = dados[f"transition_{i}_from"]
            para = dados[f"transition_{i}_to"]
            ler = dados[f"transition_{i}_read"]
            escrever = dados[f"transition_{i}_write"]
            direcao = dados[f"transition_{i}_dir"]
            maquina["transicoes"][str((de, ler))] = [para, escrever, direcao]

    # Caso estilo "igualdade.json"
    else:
        maquina["estado_inicial"] = dados["initial"]
        maquina["finais"] = [int(dados["final"])]
        maquina["branco"] = dados["white"]

        transicoes_lista = dados["transitions"]
        if isinstance(transicoes_lista, str):  # é uma string JSON
            transicoes_lista = json.loads(transicoes_lista)

        for t in transicoes_lista:
            de = t["from"]
            para = t["to"]
            ler = t["read"]
            escrever = t["write"]
            direcao = t["dir"]
            maquina["transicoes"][str((de, ler))] = [para, escrever, direcao]

    return maquina


def carregar_fita(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        return list(f.read().strip())

def salvar_fita(output_file, fita):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("".join(fita))

def simular(maquina, fita):
    estado = maquina["estado_inicial"]
    br = maquina["branco"]
    pos = 0
    transicoes = maquina["transicoes"]

    # garante espaço infinito à direita
    fita = fita + [br] * 1000  

    while True:
        simbolo = fita[pos]

        chave = (estado, simbolo)
        if str(chave) not in transicoes:
            # nenhuma transição válida
            return False, fita  

        prox_estado, escreve, move = transicoes[str(chave)]
        fita[pos] = escreve
        estado = prox_estado

        if move == "R":
            pos += 1
        elif move == "L":
            pos -= 1
            if pos < 0:  # expande à esquerda
                fita.insert(0, br)
                pos = 0

        if estado in maquina["finais"]:
            return True, fita

def main():
    if len(sys.argv) != 3:
        print("Uso: python turing.py <arquivo.json> <arquivo.in>")
        sys.exit(1)

    json_file = sys.argv[1]
    input_file = sys.argv[2]
    output_file = input_file.replace(".in", ".out")

    maquina = carregar_maquina(json_file)
    fita = carregar_fita(input_file)

    aceita, fita_final = simular(maquina, fita)

    salvar_fita(output_file, fita_final)

    print("1" if aceita else "0")

if __name__ == "__main__":
    main()
