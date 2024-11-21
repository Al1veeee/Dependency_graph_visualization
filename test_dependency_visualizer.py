import unittest
import os
from graphviz import Digraph  # Импортируем класс Digraph
from dependency_visualizer import get_commit_history, build_dependency_graph, save_graph

class TestDependencyVisualizer(unittest.TestCase):
    def setUp(self):
        # Путь к репозиторию Git для тестирования
        self.repo_path = "C:\\Users\\User\\Desktop\\konf2\\my_repo"
        # Путь для сохранения результирующего графа
        self.graph_output_path = "C:\\Users\\User\\Desktop\\konf2\\output_graph.png"

        # Проверяем, что репозиторий существует
        if not os.path.exists(self.repo_path):
            self.skipTest(f"Репозиторий по пути {self.repo_path} не найден.")

    def test_get_commit_history(self):
        """
        Тестирует функцию get_commit_history для получения истории коммитов.
        """
        commits = get_commit_history(self.repo_path)
        self.assertIsInstance(commits, dict, "Результат должен быть словарем.")
        self.assertGreater(len(commits), 0, "Коммиты не найдены в репозитории.")

        # Проверяем структуру первого коммита
        first_commit = next(iter(commits.values()))
        self.assertIn("parents", first_commit, "У коммита должна быть информация о родителях.")
        self.assertIn("message", first_commit, "У коммита должно быть сообщение.")

    def test_build_dependency_graph(self):
        """
        Тестирует функцию build_dependency_graph для создания графа зависимостей.
        """
        commits = get_commit_history(self.repo_path)
        graph = build_dependency_graph(commits)

        self.assertIsNotNone(graph, "Граф не должен быть None.")
        self.assertIsInstance(graph, Digraph, "Граф должен быть экземпляром Digraph.")

        # Проверяем, что хотя бы один узел добавлен в граф
        self.assertGreater(len(graph.body), 0, "Граф должен содержать узлы и связи.")

    def test_save_graph(self):
        """
        Тестирует функцию save_graph для сохранения графа в файл.
        """
        commits = get_commit_history(self.repo_path)
        graph = build_dependency_graph(commits)
        save_graph(graph, self.graph_output_path)

        # Проверяем, что файл был сохранен
        output_path_with_extension = f"{os.path.splitext(self.graph_output_path)[0]}.png"
        self.assertTrue(os.path.exists(output_path_with_extension), "Граф не был сохранён.")

    def test_graph_structure(self):
        """
        Дополнительный тест для проверки структуры графа.
        """
        commits = {
            "abc1234": {"parents": ["def5678"], "message": "Initial commit"},
            "def5678": {"parents": [], "message": "Root commit"}
        }
        graph = build_dependency_graph(commits)

        # Проверяем, что узлы добавлены
        self.assertIn("abc1234", graph.source, "Узел abc1234 должен быть в графе.")
        self.assertIn("def5678", graph.source, "Узел def5678 должен быть в графе.")

        # Проверяем наличие связи parent->child
        self.assertIn("def5678 -> abc1234", graph.source, "Должна быть связь def5678 -> abc1234.")

if __name__ == '__main__':
    unittest.main()
