import unittest
import os
import subprocess
from graphviz import Digraph  # Импортируем класс Digraph
from dependency_visualizer import get_commit_history, get_file_changes, build_dependency_graph, save_graph

class TestDependencyVisualizer(unittest.TestCase):
    def setUp(self):
        self.graphviz_path = "C:\\Program Files\\Graphviz\\bin"  # Укажите правильный путь
        self.repo_path = "C:\\Users\\User\\Desktop\\konf2\\my_repo"
        self.graph_output_path = "C:\\Users\\User\\Desktop\\konf2\\output_graph.png"
        self.file_hash = "example.txt"  # Укажите файл для тестирования

        # Добавляем Graphviz в PATH
        os.environ["PATH"] += os.pathsep + self.graphviz_path

    def test_get_commit_history(self):
        commits = get_commit_history(self.repo_path, self.file_hash)
        self.assertIsInstance(commits, list)
        self.assertGreater(len(commits), 0, "Коммиты не найдены для указанного файла.")

    def test_get_file_changes(self):
        commits = get_commit_history(self.repo_path, self.file_hash)
        if commits:
            # Извлекаем только хеш первого коммита
            commit_hash = commits[0][0]
            changes = get_file_changes(self.repo_path, commit_hash)  # Используем только хеш коммита
            self.assertIsInstance(changes, list)
            self.assertTrue(len(changes) >= 0, "Изменения должны быть пустым списком или содержать элементы.")

    def test_build_dependency_graph(self):
        graph = build_dependency_graph(self.repo_path, self.file_hash)
        self.assertIsNotNone(graph, "Граф не должен быть None.")
        self.assertIsInstance(graph, Digraph, "Граф должен быть экземпляром Digraph.")

    def test_save_graph(self):
        graph = build_dependency_graph(self.repo_path, self.file_hash)
        save_graph(graph, self.graph_output_path)
        output_path_with_extension = f"{os.path.splitext(self.graph_output_path)[0]}.png"
        self.assertTrue(os.path.exists(output_path_with_extension), "Граф не был сохранён.")

if __name__ == '__main__':
    unittest.main()
