import sys
import pygame
import threading

#Alunos: Matheus Berbel Barusso 2326248 e Matheus Salvi 1815121


# estrutura half edge
class Vertex:
    def __init__(self, v_id, x, y):
        self.id = v_id
        self.x = x
        self.y = y
        self.he = None  # Uma meia-aresta que sai deste vértice

    def __repr__(self):
        return f"V{self.id}"

class Face:
    def __init__(self, f_id):
        self.id = f_id
        self.he = None  # Uma meia-aresta que compõe o limite da face

    def __repr__(self):
        return f"F{self.id}"

class HalfEdge:
    def __init__(self, he_id):
        self.id = he_id
        self.origem = None  # Vértice de origem
        self.gemeo = None    # Meia-aresta gêmea (sentido oposto, pode ser None nas bordas)
        self.face = None    # Face à qual pertence
        self.prox = None    # Próxima meia-aresta na face
        self.anter = None    # Meia-aresta anterior na face

    def __repr__(self):
        gemeo_id = self.gemeo.origem.id if self.gemeo else 'None'
        return f"HE{self.id}({self.origem.id}->{self.prox.origem.id} | gemeo_org:{gemeo_id})"

class Mesh:
    def __init__(self):
        self.vertices = {}
        self.faces = {}
        self.half_edges = []
    
    def get_vertex(self, v_id): return self.vertices.get(v_id)
    def get_face(self, f_id): return self.faces.get(f_id)
    
    def get_halfedge_by_vertices(self, v_start_id, v_end_id):
        for he in self.half_edges:
            if he.origem.id == v_start_id and he.prox.origem.id == v_end_id: # O destino de uma meia-aresta é sempre a origem da próxima meia-aresta da face
                return he
        return None

#parser do .obj e construct
def load_obj_to_halfedge(filepath):
    mesh = Mesh()
    v_count = 1
    f_count = 1
    
    edges_map = {} # (origem, destino) -> HalfEdge

    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if not parts: continue
            
            if parts[0] == 'v':
                x, y = float(parts[1]), float(parts[2])
                mesh.vertices[v_count] = Vertex(v_count, x, y)
                v_count += 1
                
            elif parts[0] == 'f':
                # obj os indices começam em 1
                v_indices = [int(p.split('/')[0]) for p in parts[1:]]
                face = Face(f_count)
                mesh.faces[f_count] = face
                
                face_edges = []
                n = len(v_indices)
                
                # Criar as meia-arestas para esta face
                for i in range(n):
                    v_start_id = v_indices[i]
                    v_end_id = v_indices[(i + 1) % n]
                    
                    he = HalfEdge(len(mesh.half_edges) + 1)
                    mesh.half_edges.append(he)
                    
                    he.origem = mesh.vertices[v_start_id]
                    he.face = face
                    
                    # O vertice aponta para a primeira HE que sai dele (se já não tiver)
                    if he.origem.he is None:
                        he.origem.he = he
                        
                    # A face aponta para a primeira HE que a compõe
                    if i == 0:
                        face.he = he
                        
                    face_edges.append(he)
                    edges_map[(v_start_id, v_end_id)] = he

                # Ligar prox, anter e buscar gemeos
                for i in range(n):
                    he = face_edges[i]
                    he.prox = face_edges[(i + 1) % n]
                    he.anter = face_edges[(i - 1) % n]
                    
                    # Checar se a gemea já foi criada por uma face adjacente
                    gemeo_key = (v_indices[(i + 1) % n], v_indices[i])
                    if gemeo_key in edges_map:
                        gemeo_he = edges_map[gemeo_key]
                        he.gemeo = gemeo_he
                        gemeo_he.gemeo = he
                        
                f_count += 1
                
    return mesh

# Rasterização ("usando apenas a primitiva de ponto e a equação da reta para desenhar a aresta")
def draw_line_bresenham(surface, x0, y0, x1, y1, color=(255, 255, 255)):
    #Desenha uma reta usando apenas a primitiva de ponto
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        surface.set_at((x0, y0), color) # Primitiva de ponto
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def render_mesh(screen, mesh, width, height, font):
    if not mesh.vertices: return
    
    # normalizar coordenadas
    min_x = min(v.x for v in mesh.vertices.values())
    max_x = max(v.x for v in mesh.vertices.values())
    min_y = min(v.y for v in mesh.vertices.values())
    max_y = max(v.y for v in mesh.vertices.values())
    
    def to_screen(x, y):
        pad = 50
        scale_x = (width - 2*pad) / (max_x - min_x) if max_x != min_x else 1
        scale_y = (height - 2*pad) / (max_y - min_y) if max_y != min_y else 1
        scale = min(scale_x, scale_y)
        
        sx = pad + (x - min_x) * scale
        sy = height - (pad + (y - min_y) * scale) # Inverter Y para tela
        return sx, sy

    # --- DESENHO DAS ARESTAS ---
    drawn_edges = set()
    for he in mesh.half_edges:
        v1 = he.origem
        v2 = he.prox.origem
        
        edge_id = tuple(sorted([v1.id, v2.id]))
        
        if edge_id not in drawn_edges:
            drawn_edges.add(edge_id)
            x0, y0 = to_screen(v1.x, v1.y)
            x1, y1 = to_screen(v2.x, v2.y)
            # Linhas cinzas para os textos destacarem mais
            draw_line_bresenham(screen, x0, y0, x1, y1, color=(150, 150, 150))

    # --- DESENHO DOS IDs DOS VÉRTICES ---
    for v in mesh.vertices.values():
        sx, sy = to_screen(v.x, v.y)
        text_surf = font.render(f"v{v.id}", True, (0, 255, 0)) # Verde
        screen.blit(text_surf, (sx + 5, sy - 15))

    # --- DESENHO DOS IDs DAS FACES ---
    for face in mesh.faces.values():
        if not face.he: continue
        
        # Calcular o Centroide da face (média das coordenadas)
        cx, cy = 0.0, 0.0
        count = 0
        curr_he = face.he
        start_he = face.he
        
        while True:
            cx += curr_he.origem.x
            cy += curr_he.origem.y
            count += 1
            curr_he = curr_he.prox
            if curr_he == start_he:
                break
                
        cx /= count
        cy /= count
        sx, sy = to_screen(cx, cy)
        
        text_surf = font.render(f"F{face.id}", True, (255, 100, 100)) # Vermelho/Salmão
        screen.blit(text_surf, (sx - 10, sy - 10))

# menu seleção
def query_menu(mesh):
    while True:
        print("\n" + "="*40)
        print(" SELECIONE UMA OPÇÃO")
        print("="*40)
        print("1. Face -> Faces adjacentes")
        print("2. Face -> Arestas que a compõem")
        print("3. Face -> Vértices que a compõem")
        print("4. Aresta -> Faces adjacentes")
        print("5. Aresta -> Vértices inicial e final")
        print("6. Aresta -> Arestas adjacentes")
        print("7. Vértice -> Faces que o compartilham")
        print("8. Vértice -> Arestas que o compartilham")
        print("0. Sair")
        
        try:
            op = int(input("Escolha a consulta: "))
        except: continue
        
        if op == 0:
            print("Pode fechar a janela gráfica agora.")
            break

        # FACE
        if op in [1, 2, 3]:
            f_id = int(input(f"ID da Face (1 a {len(mesh.faces)}): "))
            face = mesh.get_face(f_id)
            if not face:
                print("Face não encontrada.")
                continue
                
            start_he = face.he
            curr_he = start_he
            
            if op == 1:
                adj_faces = set()
                while True:
                    if curr_he.gemeo and curr_he.gemeo.face:
                        adj_faces.add(curr_he.gemeo.face.id)
                    curr_he = curr_he.prox
                    if curr_he == start_he: break
                print(f"Faces adjacentes à F{f_id}: {list(adj_faces)}")
                
            elif op == 2:
                edges = []
                while True:
                    edges.append(f"({curr_he.origem.id}-{curr_he.prox.origem.id})")
                    curr_he = curr_he.prox
                    if curr_he == start_he: break
                print(f"Arestas da F{f_id}: {', '.join(edges)}")
                
            elif op == 3:
                verts = []
                while True:
                    verts.append(curr_he.origem.id)
                    curr_he = curr_he.prox
                    if curr_he == start_he: break
                print(f"Vértices da F{f_id}: {verts}")

        # ARESTA
        elif op in [4, 5, 6]:
            v1 = int(input("ID do Vértice Inicial da aresta: "))
            v2 = int(input("ID do Vértice Final da aresta: "))
            
            # Buscar a meia-aresta correspondente
            he = mesh.get_halfedge_by_vertices(v1, v2)
            if not he:
                he = mesh.get_halfedge_by_vertices(v2, v1)
                
            if not he:
                print("Aresta não encontrada.")
                continue
                
            if op == 4:
                faces = [he.face.id]
                if he.gemeo and he.gemeo.face: 
                    faces.append(he.gemeo.face.id)
                print(f"Faces adjacentes à aresta: {faces}")
                
            elif op == 5:
                print(f"Vértice Inicial: {he.origem.id}, Vértice Final: {he.prox.origem.id}")
                
            elif op == 6:
                adj_edges = set()
                # Para evitar loops infinitos
                for test_he in mesh.half_edges:
                    v_start = test_he.origem.id
                    v_end = test_he.prox.origem.id
                    
                    # Se compartilha algum dos vértices com a aresta alvo (mas não é a própria aresta)
                    if (v_start in (he.origem.id, he.prox.origem.id) or v_end in (he.origem.id, he.prox.origem.id)):
                        edge_tuple = tuple(sorted([v_start, v_end]))
                        target_tuple = tuple(sorted([he.origem.id, he.prox.origem.id]))
                        if edge_tuple != target_tuple:
                            adj_edges.add(f"({edge_tuple[0]}-{edge_tuple[1]})")
                            
                print(f"Arestas adjacentes: {list(adj_edges)}")

        # VERTICE
        elif op in [7, 8]:
            v_id = int(input(f"ID do Vértice (1 a {len(mesh.vertices)}): "))
            vert = mesh.get_vertex(v_id)
            if not vert:
                print("Vértice não encontrado.")
                continue
                
            if op == 7:
                faces = set()
                for test_he in mesh.half_edges:
                    if test_he.origem.id == v_id or test_he.prox.origem.id == v_id:
                        faces.add(test_he.face.id)
                print(f"Faces que compartilham o V{v_id}: {list(faces)}")
                
            elif op == 8:
                edges = set()
                for test_he in mesh.half_edges:
                    if test_he.origem.id == v_id or test_he.prox.origem.id == v_id:
                        edge_tuple = tuple(sorted([test_he.origem.id, test_he.prox.origem.id]))
                        edges.add(f"({edge_tuple[0]}-{edge_tuple[1]})")
                print(f"Arestas que compartilham o V{v_id}: {list(edges)}")

# Main e loop gráfico
def main():
    if len(sys.argv) < 2:
        print("Uso: python render_halfedge.py <arquivo.obj>")
        sys.exit(1)
        
    obj_path = sys.argv[1]
    print("Carregando malha...")
    mesh = load_obj_to_halfedge(obj_path)
    
    # Thread p/ rodar janela gráfica e cli ao msm tempo
    cli_thread = threading.Thread(target=query_menu, args=(mesh,), daemon=True)
    cli_thread.start()

    # Iniciar Pygame para renderização e inicializar a fonte
    pygame.init()
    pygame.font.init()
    
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(f"Visualizador Half-Edge - {obj_path}")
    
    # Cria a fonte (Tamanho 24)
    font = pygame.font.SysFont(None, 24)
    
    running = True
    while running and cli_thread.is_alive():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        screen.fill((0, 0, 0)) # Fundo preto
        
        # Passa a fonte para a função de renderização
        render_mesh(screen, mesh, width, height, font)
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()