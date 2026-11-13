import unittest
from src.core.logic import clasificar_riesgo, promedio

class TestLogic(unittest.TestCase):
    def test_riesgo_alto_por_incidente(self):
        self.assertEqual(clasificar_riesgo(30, 45.0, 1), "ALTO")
    def test_promedio(self):
        self.assertEqual(promedio([10,20,30]), 20)

if __name__ == "__main__": unittest.main()
