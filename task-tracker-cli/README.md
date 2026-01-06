# 📝 Task Tracker CLI

A simple **Command Line Interface (CLI)** application built with **Python** to help you track and manage your tasks.

This project allows users to add, update, delete, and organize tasks directly from the terminal while practicing:
- Python fundamentals
- File handling with JSON
- Command-line arguments
- Git & GitHub workflow
- Clean CLI design

---

## 🚀 Features

- Add new tasks
- Update existing tasks
- Delete tasks
- Mark tasks as **in progress** or **done**
- List all tasks
- Filter tasks by status (`todo`, `in-progress`, `done`)
- Built-in `help` command for guidance
- Persistent storage using a JSON file

---

## 📂 Project Structure

```
task-tracker-cli/

|
│
├── task_cli.py        # Main CLI application
├── tasks.json         # Task storage (ignored by Git)
├── .gitignore         # Git ignore rules
└── README.md          # Project documentation
```

---

##  Requirements

- Python **3.8+**
- No external libraries required (uses only Python standard library)

---

## ▶️ Getting Started

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/task-tracker-cli.git
cd task-tracker-cli
```

### 2️⃣ Run the application

```bash
python3 task_cli.py help
```

---

## 📌 Usage

### ➕ Add a task
```bash
python3 task_cli.py add "Buy groceries"
```

### ✏️ Update a task
```bash
python3 task_cli.py update 1 "Buy groceries and cook dinner"
```

### 🗑 Delete a task
```bash
python3 task_cli.py delete 1
```

### ⏳ Mark task as in progress
```bash
python3 task_cli.py mark-in-progress 2
```

### ✅ Mark task as done
```bash
python3 task_cli.py mark-done 2
```

### 📋 List all tasks
```bash
python3 task_cli.py list
```

### 🔍 List tasks by status
```bash
python3 task_cli.py list todo
python3 task_cli.py list in-progress
python3 task_cli.py list done
```

### 🆘 Help
```bash
python3 task_cli.py help
```

---

## 🧾 Task Properties

Each task is stored with the following fields:

- `id` — Unique task identifier
- `description` — Task description
- `status` — `todo`, `in-progress`, or `done`
- `createdAt` — Timestamp when the task was created
- `updatedAt` — Timestamp when the task was last updated

---

## 🧠 What I Learned

- Building a real-world CLI application
- Handling command-line arguments with `sys.argv`
- Reading and writing JSON files in Python
- Managing merge conflicts in Git
- Using Git branches for feature development
- Writing clean, user-friendly CLI output

---

## 🔒 Notes

- `tasks.json` is generated automatically when the app runs.
- This file is ignored by Git to avoid committing runtime data.

---

## 📌 Future Improvements

- Make the CLI globally executable (`task-cli`)
- Add colored output for better UX
- Add due dates and priorities
- Add unit tests

---

## 👤 Author

**Lucky Nkwor**  
Learning Python, CLI development, and Git by building real projects 🚀
