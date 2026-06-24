# Trabalho 8 - Weiler-Artheton Clipping Algorithm

Implementar o algoritmo Weiler–Atherton Clipping em Pyhton. Use o Colab com plotagem do recorte (similar ao algoritmos disponíveis do Cohen Sutherland e Sutherland-Hodgman)

# Instrução de Inicialização:
### Pré-Requisitos: 
``` 
pip install matplotlib numpy shapely
```

### Em um terminal, execute: 
``` 
python3 main.py
```

### Para utilizar diferentes polígonos e seções de clipping alterar respectivamente:
```subject_polygon = []``` e ```clip_poligon = []```


# Implementação:
- Biblioteca ```matplotlib``` e ```matplotlib.patches``` utilizadas na plotagem 2D interativa (Zoom, movimentação,...) quando executado no terminal. Permite visualização antes e depois (inclusive no colab).
- Biblioteca ```shapely``` utilizada para processar a travessia de nós do algoritmo de Weiler-Artheton. Isso foi escolhido pois o pipeline do algoritmo é o seguinte:
    - Duas listas duplamente encadeadas são criadas, uma para o polígono sujeiro e outra para o polígono de recorte;
    - Todas as interseções são calculadas e novos nós são inseridos em ambas as listas;
    - Cada interseção é rotulada como "Entrando" ou "Saindo" da área de recorte;
    - Passa de nó por nó, alternando de lista quando encontra uma interseção.
- Implementar a travessia das listas encadeadas em python pode facilmente criar erro de precisão flutuante. Se um vértice tocar exatamente a linha do outro polígono (chamado casos de borda) o programa entra em loops infinitos.
- Função Geomátrica auxiliar ```line_intersection(p1, p2, p3, p4)``` baseada em determinanda. Ela encontra a interseção entre dois segmentos por meio de interpolação linear, definida pela função $t = \frac{(x_1 - x_3)(y_3 - y_4) - (y_1-y_3)(x_3-x_4)}{(x_1 - x_2)(y_3 - y_4) - (y_1-y_2)(x_3-x_4)}$.
- Função auxiliar ```is_point_inside(pt, poly)``` utiliza Ray Casting para determinar se o ponto fornecido está dentro do polígono fornecido.
- Função principal de recorte ```weiler_atherton_clip(subject_poly, clip_poly)```. Simula as fases do pipeline do algoritmo de WA por meio de operação booleana de interção: $P_{resultado} = P_{sujeito} \cap P_{clip}$.
- Função de visualização ```plot_clipping(subject, clip, clipped_polygons)```. Renderiza a área do polígono original (verde), o polígono da janela de recorte (azul) e destaca em vermelho a malha poligonal resultante da operção de clipping.

    