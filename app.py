from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)


class Task:
    def __init__(self, name, description, priority):
        self.name = name
        self.description = description
        self.priority = priority


class ToDoList:
    def __init__(self, filename="tasks.csv"):
        self.tasks = []
        self.filename = filename
        self.load_from_csv()

    def add_task(self, name, description, priority):
        if priority not in ["High", "Medium", "Low"]:
            return False
        task = Task(name, description, priority)
        self.tasks.append(task)
        self.save_to_csv()
        return True

    def remove_task(self, name):
        for task in self.tasks:
            if task.name.lower() == name.lower():
                self.tasks.remove(task)
                self.save_to_csv()
                return True
        return False

    def get_tasks(self):
        return self.tasks

    def save_to_csv(self):
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Description', 'Priority'])
            for task in self.tasks:
                writer.writerow([task.name, task.description, task.priority])

    def load_from_csv(self):
        if not os.path.exists(self.filename):
            return
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            for row in reader:
                if len(row) == 3:
                    self.tasks.append(Task(row[0], row[1], row[2]))


todo_list = ToDoList()


@app.route('/')
def index():
    return render_template('index.html', tasks=todo_list.get_tasks())


@app.route('/add', methods=['POST'])
def add_task():
    name = request.form.get('name')
    description = request.form.get('description')
    priority = request.form.get('priority')
    if todo_list.add_task(name, description, priority):
        return redirect(url_for('index'))
    else:
        return "Invalid priority!", 400


@app.route('/remove/<name>')
def remove_task(name):
    todo_list.remove_task(name)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
