# PARKOUT
PROJETO PP
# Car Jam - Embarque com Movimento

Projeto desenvolvido em Python com PyQt6: um mini-jogo de lógica e coordenação que simula o embarque de passageiros em autocarros, com movimentação animada dos veículos numa grelha visual.

## Descrição

No "Car Jam", cada autocarro possui uma cor, capacidade limitada e movimenta-se numa grelha. O objetivo é embarcar corretamente todos os passageiros, respeitando as cores dos autocarros, através de uma interface visual intuitiva e animada.

- Os autocarros partem do lado direito da grelha e movem-se automaticamente para a esquerda até à área de embarque.
- Ao chegarem à área de embarque, tentam embarcar um passageiro da mesma cor (caso exista na fila).
- Após o embarque (ou tentativa), os autocarros retornam à posição de origem (lado direito).
- O jogo termina quando todos os passageiros forem embarcados, ou se o jogo ficar travado (nenhum autocarro disponível pode embarcar o passageiro do início da fila).

## Demonstração

￼

## Como jogar

1. **Clique num autocarro** para iniciar o movimento desse veículo para a esquerda.
2. Quando o autocarro chega à área de embarque (primeira coluna), ele tenta embarcar o passageiro na frente da fila, desde que:
   - O passageiro seja da mesma cor do autocarro.
   - O autocarro ainda tenha lugares disponíveis.
3. Após o embarque (ou tentativa), o autocarro retorna animadamente ao ponto de partida (última coluna).
4. Repita o processo para embarcar todos os passageiros.
5. Se não for possível embarcar mais passageiros e o primeiro da fila não pode ser embarcado por nenhum autocarro, será apresentado um aviso de jogo travado.

## Regras

- Só é possível embarcar um passageiro se a cor do autocarro coincidir com a do passageiro e houver lugares livres.
- Os autocarros só podem transportar até à sua capacidade máxima (4 passageiros).
- O jogo termina quando todos os passageiros forem embarcados (vitória) ou se ficar travado (nenhuma solução possível).

## Requisitos

- Python 3.8 ou superior
- PyQt6

## Instalação

1. **Clona o repositório:**
    ```sh
    git clone https://github.com/teu-usuario/teu-repo-car-jam.git
    cd teu-repo-car-jam
    ```

2. **Instala as dependências:**
    ```sh
    pip install PyQt6
    ```

## Como executar

Basta correr o ficheiro principal:


python Parkout.py
