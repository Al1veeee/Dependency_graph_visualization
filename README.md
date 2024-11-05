## **Цель задание:**

Разработать инструмент командной строки для визуализации графа
зависимостей, включая транзитивные зависимости. Сторонние средства для
получения зависимостей использовать нельзя.


Зависимости определяются для git-репозитория. Для описания графа
зависимостей используется представление Graphviz. Визуализатор должен
выводить результат в виде сообщения об успешном выполнении и сохранять граф
в файле формата png.


Построить граф зависимостей для коммитов, в узлах которого находятся
связи с файлами и папками, представленными уникальными узлами. Граф
необходимо строить только для тех коммитов, где фигурирует файл с заданным
хеш-значением.


Ключами командной строки задаются:

  
   - Путь к программе для визуализации графов.
   - Путь к анализируемому репозиторию.
   - Путь к файлу с изображением графа зависимостей.
   - Файл с заданным хеш-значением в репозитории.


Все функции визуализатора зависимостей должны быть покрыты тестами.


## **Описание проекта:**

Проект предназначен для анализа Git-репозитория и визуализации зависимостей файлов с помощью графиков. Он позволяет отслеживать изменения в файлах и видеть, какие коммиты затрагивают определённые файлы.


## **Описание функциональности:**
### **Основные функции:**


   1. **Получение истории коммитов:** Инструмент извлекает список коммитов, связанных с файлом, имеющим заданное хеш-значение.
   2. **Определение зависимостей:** Для каждого коммита, найденного на предыдущем шаге, инструмент собирает список файлов и папок, которые были изменены.
   3. **Построение графа зависимостей:** Инструмент создает граф, в котором:


      - Узлы представляют собой коммиты и уникальные файлы/папки.
      - Ребра показывают связи между коммитами и измененными файлами.
     
      
   4. **Сохранение графа:** Граф сохраняется в виде PNG-файла.
   5. **Вывод сообщений:** Инструмент выводит сообщения об успешном выполнении операций.


### **Параметры командной строки:**

Инструмент принимает следующие параметры командной строки:

   - ```--graphviz_path```: Путь к программе для визуализации графов (например, Graphviz).
   - ```--repo_path```: Путь к анализируемому git-репозиторию.
   - ```--output_path```: Путь к файлу, в который будет сохранен граф зависимостей (формат PNG).
   - ```--file_hash```: Имя файла с заданным хеш-значением для анализа зависимостей.

## **Сценарий использования ```auto_commit.py```**

**Запуск программы:** 
```
python auto_commit.py
```


1. **Запуск программы:** Пользователь запускает программу, которая начинает отслеживать изменения в указанном файле example.txt, находящемся в Git-репозитории по заданному пути.

2. **Изменение файла:** При каждом изменении файла (например, при сохранении изменений в текстовом редакторе) программа автоматически добавляет изменения в Git и коммитит их с сообщением "Автоматический коммит изменений в {file_path}".

3. **Командный интерфейс:** Пользователь может вводить команды в терминале:


   - Команда ```clear``` очищает историю коммитов, оставляя только текущий коммит.
   - Команда ```exit``` завершает работу программы.
4. **Завершение работы:** При выходе из программы все потоки останавливаются корректно, и наблюдение за изменениями завершается.


![Гифка с Gifius ru](https://github.com/user-attachments/assets/43afecd0-48fa-4333-ab6c-8498d0b02979)

## **Пример работы ```dependency_visualizer.py```**

### **Описание**
Этот скрипт предназначен для визуализации зависимостей в Git-репозиториях. Он анализирует историю коммитов указанного файла и создает граф, отображающий изменения, внесенные в файл в разных коммитах.


### **Установка**

Перед использованием убедитесь, что у вас установлены следующие зависимости:

   - Python 3.x
   - Git
   - Graphviz

**Чтобы запустить скрипт, используйте команду:** 
```
python ваш_скрипт.py --graphviz_path <путь_к_Graphviz> --repo_path <путь_к_репозиторию> --output_path <путь_к_выходному_файлу> --file_hash <имя_файла>
```
**Пример:**
```
python dependency_visualizer.py --graphviz_path "C:\Program Files\Graphviz\bin" --repo_path "C:\Users\User\Desktop\konf2\my_repo" --output_path "output_graph.png" --file_hash "example.txt"
```

**Содержимое** ```output_graph.png```:

![image](https://github.com/user-attachments/assets/7918ba6e-1fe7-47b8-a428-1714f46bf3f4)


## **Тесты визуализатора зависимостей** ```test_dependency_visualizer.py```

### **Описание**
Эта документация описывает тесты, написанные для проверки функциональности визуализатора зависимостей в Git-репозиториях. Тесты написаны с использованием библиотеки unittest и проверяют ключевые функции, такие как получение истории коммитов, изменения файлов, построение графа зависимостей и сохранение графа.

### Тестовые методы
1. ```test_get_commit_history```


Тестирует функцию ```get_commit_history```.

**Описание:**
   - Получает историю коммитов для указанного файла.
   - Проверяет, что результат является списком.
   - Убеждается, что список коммитов не пустой.


**Ожидаемое поведение:**
   - Тест должен пройти, если история коммитов успешно получена и содержит хотя бы один коммит. В противном случае выводится сообщение об ошибке.

---
2. ```test_get_file_changes```
Тестирует функцию ```get_file_changes```.

**Описание:**
   - Получает историю коммитов для указанного файла.
   - Извлекает хеш первого коммита.
   - Получает изменения для этого коммита.
   - Проверяет, что результат является списком и не содержит отрицательных значений по длине.


**Ожидаемое поведение:**
   - Тест должен пройти, если изменения были успешно получены и представляют собой либо пустой список, либо список с изменениями.

---
3. ```test_build_dependency_graph```
Тестирует функцию build_dependency_graph.

**Описание:**
   - Строит граф зависимостей для указанного файла.
   - Проверяет, что граф не равен None.
   - Проверяет, что объект графа является экземпляром Digraph.


**Ожидаемое поведение:**
   - Тест должен пройти, если граф был успешно построен и является корректным объектом.
---
4. ```test_save_graph```
Тестирует функцию ```save_graph```.

**Описание:**
   - Строит граф зависимостей для указанного файла.
   - Сохраняет граф в указанный путь.
   - Проверяет, что файл с графом был успешно создан.


**Ожидаемое поведение:**
   - Тест должен пройти, если граф был успешно сохранен и файл существует по заданному пути.
---
### **Запуск тестов**
Для запуска тестов выполните следующую команду в терминале:
```
python -m unittest -v test_dependency_visualizer.py
```

![image](https://github.com/user-attachments/assets/2210b031-ea11-435f-a086-a18906673c08)


