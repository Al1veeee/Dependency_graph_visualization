import os
import zlib
from graphviz import Digraph


def read_commit(repo_path, commit_hash):
    """
    Читает объект коммита из .git/objects, декомпрессирует его и извлекает данные.
    """
    obj_path = os.path.join(repo_path, ".git", "objects", commit_hash[:2], commit_hash[2:])
    try:
        with open(obj_path, "rb") as f:
            compressed_data = f.read()
            decompressed_data = zlib.decompress(compressed_data).decode('utf-8')
            return decompressed_data
    except Exception as e:
        print(f"Ошибка при чтении коммита {commit_hash}: {e}")
        return None


def parse_commit_data(commit_data):
    """
    Парсит данные коммита, чтобы получить хеш родительского коммита и сообщение.
    """
    lines = commit_data.splitlines()
    parents = []
    message = ""
    for line in lines:
        if line.startswith("parent "):
            parents.append(line.split()[1])
        elif line and not line.startswith("author") and not line.startswith("committer"):
            message += line.strip() + " "
    return parents, message.strip()


def sanitize_label(label):
    """
    Убирает из метки все символы, кроме букв и цифр, и ограничивает длину до 30 символов.
    """
    return ''.join(c for c in label if c.isalnum())[:30]


def get_commit_history(repo_path):
    """
    Находит все коммиты и их зависимости, начиная с веток в .git/refs/heads.
    """
    commits = {}
    refs_dir = os.path.join(repo_path, ".git", "refs", "heads")

    for branch in os.listdir(refs_dir):
        branch_path = os.path.join(refs_dir, branch)
        try:
            with open(branch_path, 'r') as f:
                commit_hash = f.read().strip()
                if commit_hash not in commits:
                    stack = [commit_hash]

                    while stack:
                        current_hash = stack.pop()
                        if current_hash in commits:
                            continue

                        commit_data = read_commit(repo_path, current_hash)
                        if commit_data:
                            parents, message = parse_commit_data(commit_data)
                            commits[current_hash] = {"parents": parents, "message": message}
                            stack.extend(parents)
        except Exception as e:
            print(f"Ошибка при обработке ветки {branch}: {e}")

    return commits


def build_dependency_graph(commits):
    """
    Строит граф зависимостей по таблице коммитов и их родителей, включая родственные связи.
    """
    graph = Digraph(comment='Commit Dependency Graph')

    for commit_hash, data in commits.items():
        # Сокращенный хэш и информация о сообщении коммита
        short_hash = commit_hash[:7]
        short_message = sanitize_label(data["message"]) if data["message"] else "NoMessage"
        commit_label = f"Commit: {short_hash}\nMessage: {short_message}"

        # Создаем узел для текущего коммита
        graph.node(commit_hash, label=commit_label, shape='box', style='filled', fillcolor='lightblue')

        # Связываем текущий коммит с его родителями
        for parent_hash in data["parents"]:
            graph.edge(parent_hash, commit_hash, label="parent->child", color="blue")

    # Добавляем обратные связи для наглядности (child -> parent)
    for commit_hash, data in commits.items():
        for parent_hash in data["parents"]:
            if parent_hash in commits:
                graph.edge(commit_hash, parent_hash, label="child->parent", color="green", style="dashed")

    return graph


def save_graph(graph, output_path):
    """
    Сохраняет граф в формате PNG.
    """
    output_base = os.path.splitext(output_path)[0]
    graph.format = "png"
    graph.attr(rankdir='TB')
    try:
        graph.render(output_base, cleanup=True)
        print(f"Граф зависимостей сохранён в {output_base}.png")
    except Exception as e:
        print(f"Ошибка при сохранении графа: {e}")


def main():
    # Настройки
    repo_path = "C:/Users/User/Desktop/konf2/my_repo"
    output_path = "C:/Users/User/Desktop/output.png"

    print(f"Работаю с репозиторием: {repo_path}")

    # Получаем все коммиты и их зависимости
    commits = get_commit_history(repo_path)

    # Строим граф
    graph = build_dependency_graph(commits)

    # Сохраняем граф
    save_graph(graph, output_path)


if __name__ == "__main__":
    main()
