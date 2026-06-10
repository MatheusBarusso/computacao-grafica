# Trabalho 7 - Rasterização

Estender o Trabalho 5 para permitir uso de algoritmo de Bresenham e Xiaolin Wu para desenhar as arestas dos objetos gráficos 2D. A escolha do algoritmo deve ser um parâmetro de inicialização do programa.

# Instruções de Inicialização:
### Para usar Bresenham execute com: 
``` 
python3 main.py teste.obj bresenham
```

### Para usar Xiaolin Wu execute com: 
``` 
python3 main.py teste.obj wu
```



# Alterações realizadas:
- Função ```drawn_line_bresenham(...)``` já presente no código anteriormente e não foi alterada.
- Função ```drawn_line_xiaolin_wu(surface, x0, y0, x1, y1, color=())``` adicionada, responsável por rasterizar as retas utilizando antialiasing. Além disso foram adicionadas as seguintes funções auxiliares para o funcionamento da rasterização:
    - ```plot_aa(surface, x, y, color, brightness)```, que desenha um pixel com intensidade especificada;
    - ```ipart(x)```, que trunca um número, isso é, retornando apenas sua parte inteira. Utilizado para descobrir qual pixel está logo abaixo da reta;
    - ```roundi(x)```, que arredonda para o número inteiro mais próximo do inserido. Utilizado para encontrar os pixels dos extremos da reta;
    - ```fpart(x)```,  que retorna apenas a parte fracionária do seu argumento. Utilizado para informar o quão perto a reta está do próximo pixel.
    - ```rfpart(x)```, que retorna o complemento da parte fracionária, isso é, quanto "falta" para que ela seja um inteiro.
- Inclusão de parâmetro de renderização na função ```render_mesh(screen, mesh, width, height, font, line_algorithm)```, com ```line_algorithm``` sendo o argumento de inicizaliação do programa que define o método de rasterização. Dependendo do argumento utilizado a função ```draw_line_xiaolin_wu(...)``` ou ```drawn_line_bresenham(...)``` poderá ser chamada.
- Checagem de quantidade de parâmetros de inicialização em ```if len(sys.argv) < 3:```, pronto para receber um arquivo ```.obj``` e o método de rasterização.

    