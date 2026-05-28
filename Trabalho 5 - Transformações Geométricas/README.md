# Trabalho 5 - Transformações Geométricas

Estender o Trabalho 2 para permitir transformações geométricas de translação, escala, cisalhamento, reflexão e rotação no objeto gráfico 2D carregado e renderizado a partir de um arquivo no formato .obj.

A estrutura de dados winged-edge ou half-edge deve ser mantida para gerenciar a geometria e topologia do objeto. Também deve ser mantida a rotina de equação da reta para desenhar as arestas, bem como as 9 (nove) operações de busca sobre a estrutura de dados. 

# Instruções de Inicialização:
### Execute com: 
``` 
python3 main.py arquivo_objeto.obj 
```



# Alterações realizadas:
- Biblioteca ```math``` adicionada para utilzação de trigonometria e conversão de graus para radianos.
- Novas funções de transformações geométricas 2D:
    - Função ```translate_mesh(mesh, tx, ty)``` com base na fórmula da operação: $T(x,y) = (x + tx, y + ty) $. Movimento o objeto no plano 2D (Ao utilizar valores muito altos o objeto será deslocado para fora da viewport fixa). Para que o programa não tenha como centro da viewport o objeto e a transalação seja notada foram adicionados métodos para calcular os limites originais uma vez para que possam ser reutilizados nas renderizações em que o objeto "se movemente". 
    - Função ```scale_mesh(mesh, sx, sy)``` com base na fórmula da operação: $S(x,y) = (x\cdot s_x, y\cdot s_y)$. Altera a escala nos eixos do objeto "esticando" ou "comprimindo" ele. Coordenadas originais são armazenadas no início da renderização para que alterações sucessivas de escalas sejam possíveis sem deformações acumuladas.
    - Função ```rotate_mesh(mesh, angle_deg)``` com base nas fórmulas da operação: $x' = xcos(\theta) - ysin(\theta),~~y' = xsin(\theta) + ycos(\theta)$. Função rotaciona a malha em torno do seu centro.
    - Função ```shear_mesh(mesh, shx, shy)``` com base nas fórmulas da operação: $x' = x + sh_x \cdot y,~~y' = y + sh_y \cdot x$. Aplica deformação inclinando a geometria do objeto.
    - Função ```reflect_mesh(mesh, axis)```, realizando a reflexão ("espelhamento da malha") no eixo $x$ por meio de $(x,y) \rightarrow (x, -y)$ e no eixo $y$ por meio de $(x,y) \rightarrow (-x,y)$.
    - Função auxiliadora ```get_mesh_center(mesh)``` que tem como objetivo calcular o centro geométrico do objeto. É chamada nas funções ```scale_mesh()```, ```rotate_mesh()``` e ```reflect_mesh```.
- Novas opções no menu de interação com blocos de operação que chamam as funções condizentes com cada opção.

    