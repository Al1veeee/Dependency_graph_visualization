import argparse
import subprocess
from graphviz import Digraph
import os

def get_commit_history(repo_path, file_hash):
    """
    Возвращает список коммитов с их хешем, датой и сообщением для заданного файла.
    """
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "log", "--pretty=format:%H|%ad|%s", "--date=iso", "--all", "--", file_hash],
            check=True, capture_output=True, text=True, encoding='utf-8'
        )
        commits = result.stdout.splitlines()
        return [tuple(commit.split('|')) for commit in commits]
    except subprocess.CalledProcessError as e:
        print(f"Ошибка получения истории коммитов: {e}")
        return []

def get_file_changes(repo_path, commit_hash):
    """
    Возвращает список файлов, измененных в заданном коммите.
    """
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "show", "--pretty=format:", "--name-only", commit_hash],
            check=True, capture_output=True, text=True, encoding='utf-8'
        )
        changes = result.stdout.splitlines()
        return changes
    except subprocess.CalledProcessError as e:
        print(f"Ошибка получения изменений для коммита {commit_hash}: {e}")
        return []

def get_detailed_diff(repo_path, commit_hash, file_name):
    """
    Возвращает разницу для конкретного файла в заданном коммите.
    """
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "diff", f"{commit_hash}^!", "--", file_name],
            check=True, capture_output=True, text=True, encoding='utf-8'
        )
        return result.stdout.strip().splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Ошибка получения различий для файла {file_name} в коммите {commit_hash}: {e}")
        return []

def build_dependency_graph(repo_path, file_hash):
    """
    Создаёт граф зависимостей для коммитов с указанным файлом.
    """
    commits = get_commit_history(repo_path, file_hash)
    graph = Digraph(comment='Dependency Graph')

    # Устанавливаем шрифт для узлов
    graph.attr(fontname='Verdana', fontsize='12', labelfontsize='14')

    if not commits:
        print(f"Файл '{file_hash}' не найден в истории коммитов.")
        return graph

    for commit_hash, commit_date, commit_message in commits:
        changes = get_file_changes(repo_path, commit_hash)

        for file_name in changes:
            # Получаем различия для каждого файла
            detailed_diff = get_detailed_diff(repo_path, commit_hash, file_name)

            # Создаем метку для узла коммита
            commit_label = f"{commit_hash[:7]}\n{commit_date}\n{commit_message}"  # Узел для коммита
            graph.node(commit_hash, label=commit_label.encode('utf-8').decode('utf-8'), shape='box')  # Узел для коммита

            # Форматируем изменения
            additions = []
            deletions = []

            for line in detailed_diff:
                if line.startswith('+') and not line.startswith('+++'):
                    additions.append(line)  # Добавленные строки
                elif line.startswith('-') and not line.startswith('---'):
                    deletions.append(line)  # Удаленные строки

            # Сжимаем вывод изменений
            addition_str = "\n".join(additions) if additions else "Нет добавленных строк"
            deletion_str = "\n".join(deletions) if deletions else "Нет удаленных строк"

            dependency_label = f"{file_name}\nДобавлено:\n{addition_str}\n\nУдалено:\n{deletion_str}"
            graph.node(file_name, label=dependency_label.encode('utf-8').decode('utf-8'), shape='ellipse')  # Узел для файла
            graph.edge(commit_hash, file_name)  # Связь между коммитом и файлом

    return graph

def save_graph(graph, output_path):
    """
    Сохраняет граф в PNG-файл.
    """
    output_base = os.path.splitext(output_path)[0]
    graph.format = "png"
    graph.attr(rankdir='TB')
    graph.render(output_base, cleanup=True)
    print(f"Граф зависимостей сохранён в {output_base}.png")

def main():
    parser = argparse.ArgumentParser(description="Визуализатор зависимостей для Git-репозитория")
    parser.add_argument("--graphviz_path", required=True, help="Путь к программе для визуализации графов")
    parser.add_argument("--repo_path", required=True, help="Путь к анализируемому репозиторию")
    parser.add_argument("--output_path", required=True, help="Путь к файлу с изображением графа зависимостей")
    parser.add_argument("--file_hash", required=True, help="Имя файла, для которого нужно найти зависимости")
    args = parser.parse_args()

    os.environ["PATH"] += os.pathsep + args.graphviz_path
    graph = build_dependency_graph(args.repo_path, args.file_hash)
    save_graph(graph, args.output_path)

if __name__ == "__main__":
    main()
