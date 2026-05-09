# Trabalho 3 OpenGL - Snake-Game

Com base no projeto Snake-Game disponível em https://github.com/Rohit-B-Kadam/Snake-Game

1) Alterar o código-fonte de forma que a snake cruze de forma horizontal e vertical as fronteiras da viewport; por exemplo, quando ultrapassar o limite da fronteira à esquerda, a snake deve cruzar para o lado direito e vice-versa. O mesmo deve acontecer no sentido cima-baixo e vice-versa.

2) Inserir, a cada início de jogo, pelo menos 6 blocos médios ou grandes (quadrados ou retângulos) aleatórios no espaço a ser percorrido pela snake. Caso a snake colida com os blocos, o estado deve ser GAME OVER.  

---

# Instruções de Compilação e Inicialização:
### Forneça permissão para o script
``` chmod +x compile.sh ```

### Execute com: 
``` ./compile ```

---

# Alterações realizadas:

## ``` GameHeader.h ```
- ``` NUM_OBSTACLES ``` definindo a quantidade de obstáculos a serem criados.
- Matrizes ``` pos_x[] ``` e ``` pos_y[] ``` irão guardar informações para a posição dos blocos de obstáculo criados.
- Criação da Função ``` createObstacles() ```: Gera semente aleatória e cria ``` NUM_OBSTACLES ``` posições de blocos que caibam dentro do viewport.
- Inserção da função ``` createObstacles() ``` dentro de ``` initGame() ``` para que blocos sejam criados no início do jogo.
- Criação da Função ``` searchObstacle() ``` que checa se o próximo movimento irá colidir com algum dos obstáculos por meio de ``` checkEqualNode() ```.
- Criação da Função ``` drawObstacle() ``` que desenha ``` NUM_OBSTACLES ``` gerados na tela, com tamanho de 30x30.

## ``` snake.c ```
- Alteração na lógica de checagem de colisão em ``` moveSnake() ```:
    - Checa colisão usando ``` search() ``` para colisão com o próprio corpo e ``` searchObstacle() ``` para colisão com obstáculos criados.
    - Quando próxima movimentação chega nos extremos do ViewPort direciona o próximo movimento para o canto contrário. ``` Se Próximo_X > 640 -> Próximo_X = 0 ```, ```Se Próximo_X < 0 -> Próximo_X = 640```. O mesmo vale para Y, com limites de 0 e 480.
- Chamada de função ``` drawObstacles()``` na função ```mydisplay()```, pois toda vez que essa última é chamada a tela é limpa com ``` glClear() ```.
    