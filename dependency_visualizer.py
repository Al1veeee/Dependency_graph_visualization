import argparse
import subprocess
from graphviz import Digraph
import os

def get_commit_history(repo_path, file_hash):
    """
    Возвращает список коммитов, в которых встречается файл с заданным хешем.
    """
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "log", "--pretty=format:%H", "--all", "--", file_hash],
            check=True, capture_output=True, text=True
        )
        commits = result.stdout.splitlines()
        return commits
    except subprocess.CalledProcessError as e:
        print(f"Ошибка получения истории коммитов: {e}")
        return []

def get_file_dependencies(repo_path, commit_hash):
    """
    Возвращает список файлов и папок, изменённых в коммите.
    """
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "diff-tree", "--no-commit-id", "--name-only", "-r", commit_hash],
            check=True, capture_output=True, text=True
        )
        dependencies = result.stdout.splitlines()
        return dependencies
    except subprocess.CalledProcessError as e:
        print(f"Ошибка получения зависимостей для коммита {commit_hash}: {e}")
        return []

def build_dependency_graph(repo_path, file_hash):
    """
    Создаёт граф зависимостей для коммитов с указанным файлом по хешу.
    """
    commits = get_commit_history(repo_path, file_hash)
    graph = Digraph(comment='Dependency Graph')

    # Проверка, добавлены ли узлы и зависимости для графа
    if not commits:
        print(f"Файл '{file_hash}' не найден в истории коммитов.")
        return graph

    for commit in commits:
        dependencies = get_file_dependencies(repo_path, commit)
        for dependency in dependencies:
            # Создаём узел для коммита и зависимого файла
            graph.node(commit, label=commit[:7])  # узел для коммита
            graph.node(dependency, label=dependency)  # узел для файла
            graph.edge(commit, dependency)  # связь между коммитом и файлом

    return graph

def save_graph(graph, output_path):
    """
    Сохраняет граф в PNG-файл.
    """
    # Удаляем расширение, если оно присутствует
    output_base = os.path.splitext(output_path)[0]  # Получаем базовое имя без расширения
    output_file_path = f"{output_base}.png"  # Добавляем .png

    # Устанавливаем формат и сохраняем граф
    graph.format = "png"
    graph.attr(rankdir='TB', charset='UTF-8')  # Устанавливаем направление и кодировку
    graph.render(output_base, cleanup=True)  # cleanup удаляет промежуточный файл .dot
    print(f"Граф зависимостей сохранён в {output_file_path}")

def main():
    parser = argparse.ArgumentParser(description="Визуализатор зависимостей для Git-репозитория")
    parser.add_argument("--graphviz_path", required=True, help="Путь к программе для визуализации графов")
    parser.add_argument("--repo_path", required=True, help="Путь к анализируемому репозиторию")
    parser.add_argument("--output_path", required=True, help="Путь к файлу с изображением графа зависимостей")
    parser.add_argument("--file_hash", required=True, help="Имя файла, для которого нужно найти зависимости")
    args = parser.parse_args()

    # Добавляем Graphviz в PATH
    os.environ["PATH"] += os.pathsep + args.graphviz_path
    graph = build_dependency_graph(args.repo_path, args.file_hash)
    save_graph(graph, args.output_path)

if __name__ == "__main__":
    main()
