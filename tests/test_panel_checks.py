import unittest
from pyqte.panel_checks import check_panel_data

class TestPanelChecks(unittest.TestCase):

    def setUp(self):
        # Configurações iniciais antes de cada teste
        self.data = {
            'id': [1, 1, 2, 2],
            'year': [1978, 1979, 1978, 1979],
            'value': [10, 20, 15, 25]
        }  # Exemplo de um conjunto de dados em painel

    def test_check_panel_data(self):
        # Testa se a função check_panel_data identifica corretamente os dados do painel
        result = check_panel_data(self.data, idname='id', tname='year')
        self.assertTrue(result)
        # Adicione mais asserções para validar o resultado esperado

if __name__ == '__main__':
    unittest.main()
