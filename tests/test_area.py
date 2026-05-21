from pytest import approx
from common.r3 import R3
from shadow.polyedr import Polyedr, Facet


def r3approx(self, other):
    return self.x == approx(other.x) and self.y == approx(other.y) and \
        self.z == approx(other.z)


setattr(R3, 'approx', r3approx)


class TestSpecialArea:
    """Тесты для задачи: сумма площадей граней с ≤2 'хорошими' вершинами"""

    # 1. Проверка условия "хорошей" точки
    def test_good_point_inside(self):
        assert Polyedr.is_good_point(R3(0.0, 0.0, -1.5)) is True
        assert Polyedr.is_good_point(R3(0.0, 0.0, -4.5)) is True

    def test_good_point_outside(self):
        assert Polyedr.is_good_point(R3(0.0, 0.0, 0.0)) is False
        assert Polyedr.is_good_point(R3(0.0, 0.0, -3.0)) is False

    # 2. Проверка корректности расчёта площади грани
    def test_facet_area_unit_square(self):
        v = [R3(0, 0, 0), R3(1, 0, 0), R3(1, 1, 0), R3(0, 1, 0)]
        f = Facet(v, v)  # raw_vertexes совпадают с обычными для теста
        assert Polyedr.facet_area(f) == approx(1.0, abs=1e-6)

    # 3. Интеграционные тесты на реальных файлах (проверка итогового ответа)
    # В данных тестах указана погрешность вичислений 2%
    def test_box(self):
        p = Polyedr("data/box.geom")
        assert p.calculate_special_area() == approx(5.0, rel=0.02)

    def test_ccc(self):
        p = Polyedr("data/ccc.geom")
        assert p.calculate_special_area() == approx(50.0, rel=0.02)

    def test_cube(self):
        p = Polyedr("data/cube.geom")
        assert p.calculate_special_area() == approx(6.0, rel=0.02)

    def test_king(self):
        p = Polyedr("data/king.geom")
        assert p.calculate_special_area() == approx(0.89, rel=0.02)

    def test_cow(self):
        p = Polyedr("data/cow.geom")
        assert p.calculate_special_area() == approx(92.4, rel=0.02)
