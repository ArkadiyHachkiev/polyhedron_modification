from math import pi
from common.r3 import R3


class Edge:
    """ Ребро полиэдра """
    # Параметры конструктора: начало и конец ребра (точки в R3)

    def __init__(self, beg, fin):
        self.beg, self.fin = beg, fin


class Facet:
    """ Грань полиэдра """
    # Параметры конструктора: список вершин

    def __init__(self, vertexes, raw_vertexes=None):
        self.vertexes = vertexes
        if raw_vertexes:
            self.raw_vertexes = raw_vertexes


class Polyedr:
    """ Полиэдр """
    # Параметры конструктора: файл, задающий полиэдр

    def __init__(self, file):

        # списки вершин, рёбер и граней полиэдра
        self.vertexes, self.raw_vertexes = [], []
        self.edges, self.facets = [], []

        # список строк файла
        with open(file) as f:
            for i, line in enumerate(f):
                if i == 0:
                    # обрабатываем первую строку; buf - вспомогательный массив
                    buf = line.split()
                    # коэффициент гомотетии
                    c = float(buf.pop(0))
                    # углы Эйлера, определяющие вращение
                    alpha, beta, gamma = (float(x) * pi / 180.0 for x in buf)
                elif i == 1:
                    # во второй строке число вершин, граней и рёбер полиэдра
                    nv, nf, ne = (int(x) for x in line.split())
                elif i < nv + 2:
                    # задание всех вершин полиэдра
                    x, y, z = (float(x) for x in line.split())
                    self.raw_vertexes.append(R3(x, y, z))
                    self.vertexes.append(R3(x, y, z).rz(
                        alpha).ry(beta).rz(gamma) * c)
                else:
                    # вспомогательный массив
                    buf = line.split()
                    # количество вершин очередной грани
                    size = int(buf.pop(0))
                    # массив вершин этой грани
                    vertexes = [self.vertexes[int(n) - 1] for n in buf]
                    raw_vertexes = [self.raw_vertexes[int(n) - 1] for n in buf]
                    # задание рёбер грани
                    for n in range(size):
                        self.edges.append(Edge(vertexes[n - 1], vertexes[n]))
                    # задание самой грани
                    self.facets.append(Facet(vertexes, raw_vertexes))

    # Метод проверки: является ли точка хорошей
    @staticmethod
    def is_good_point(p):
        return 1.0 < abs(p.z + 3.0) < 2.0

    # Подсчёт площади грани
    @staticmethod
    def facet_area(facet):
        n = len(facet.raw_vertexes)
        if n < 3:
            return 0.0
        v0 = facet.raw_vertexes[0]
        area_vec = R3(0.0, 0.0, 0.0)
        for i in range(1, n - 1):
            v1 = facet.raw_vertexes[i]
            v2 = facet.raw_vertexes[i + 1]
            cross_prod = (v1 - v0).cross(v2 - v0)
            area_vec = area_vec + cross_prod
        area = 0.5 * (area_vec.dot(area_vec)) ** 0.5
        return area

    # Подсчёт количества граней, удовлетворяющих условию
    def calculate_special_area(self):
        total_area = 0.0
        for facet in self.facets:
            good_count = 0
            for v in facet.raw_vertexes:
                if Polyedr.is_good_point(v):
                    good_count += 1
            if good_count <= 2:
                total_area += Polyedr.facet_area(facet)
        return total_area

    # Метод изображения полиэдра
    def draw(self, tk):
        tk.clean()
        for e in self.edges:
            tk.draw_line(e.beg, e.fin)
        result = self.calculate_special_area()
        print(f"Сумма площадей целевых граней: {result}")
