# Trabalho 2 - Estrutura de Dados Winged-edge ou Hal-edge

Escrever um programa em OpenGL ou outra biblioteca gráfica (usando apenas a primitiva de ponto e a equação da reta para desenhar a aresta) que, dado como entrada um objeto gráfico 2D no formato .obj, construa a estrutura de dados winged-edge ou half-edge e renderize a partir dessa estrutura. Se desejável, estenda o código line-equation-handling-obj. A escolha da linguagem de programação é livre (C, C++, Python, etc.).

O programa deve aceitar, como argumento de inicialização, um arquivo .obj. Além disso, o programa deve permitir realizar as consultas abaixo:
- Dada uma face, listar as faces adjacentes.
- Dada uma face, listar as arestas que compõem a face.
- Dada uma face, listar os vértices que compõem a face.
- Dada uma aresta, listar as faces adjacentes.
- Dada uma aresta, listar os vértices inicial e final.
- Dada uma aresta, listar as arestas adjacentes.
- Dado um vértice, listar quais faces compartilham o vértice.
- Dado um vértice, listar quais arestas compartilham o vértice.
- Dado um vértice, listar quais faces compartilham o vértice.


# Instruções de Inicialização:
### Execute com: 
``` 
python3 main.py arquivo_objeto.obj 
```

---


    