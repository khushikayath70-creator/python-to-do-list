from pathlib import Path

def to_do_list():
    path = Path(__file__).parent / "to_dolist.txt"

    while True:
        try:
            print("\n====TO DO APP====")
            print("1. Add Task")
            print("2. View Task")
            print("3. Mark Task Completed")
            print("4. Delete Task")
            print("5. Exit")

            choice = int(input("Enter your choice:- "))

            #Add Task
            if choice == 1:
                task = input("Enter your task:- ")

                with open(path, "a") as fs:
                    fs.write(f"{task} - pending\n")
                
                print("Task Added Successfully!")

            #View Task
            if choice == 2:
                try:
                    with open(path, "r") as fs:
                        tasks = fs.readlines()

                        if len(tasks) == 0:
                            print("task not found")
                        else:
                            print("\nYour task: ")

                            for i, task in enumerate(tasks, start=1):
                                print(f"{i}. {task.strip()}")

                except FileNotFoundError:
                    print("File Not Found")

            # 3. Mark task completed
            if choice == 3:
                try:
                    with open(path, "r") as fs:
                        tasks = fs.readlines()

                        if len(tasks) == 0:
                            print("task not found")
                        else:
                            print("\nYour task: ")

                            for i, task in enumerate(tasks, start=1):
                                print(f"{i}. {task.strip()}")

                            task_no = int(inpu("Enter task number to completed:- "))

                            if task_no < 1 or task_no > len(tasks):
                                print("Invalid Task number.")

                            else:
                                old_task = tasks[task_no - 1].strip()

                                task_name = old_task.split(" - ")[0]

                                tasks[task_no - 1] = f"{task_name} - completed\n"

                                with open(path, "w") as fs:
                                    fs.writelines(tasks)

                                print("task marked as completed")

                except FileNotFoundError:
                    print("File not found")

                except ValueError:
                    print("Please Enter a valid number: ")

            #Delete task
            if choice == 4:
                try:
                    with open(path, "r") as fs:
                        fs.readlines()

                    if len(tasks) == 0:
                        print("No task found")

                    else:
                        print("\nYour Tasks: ")

                        for i, tasks in enumerate(tasks, start = 1):
                            print(f"{i}. {task.strip()}")

                            task_no = int(input("Enter Task number to delete: "))

                            if task_no < 1 or task_no > len(tasks):
                                print("Invalid task number.")
                            else:
                                deleted_task = tasks.pop(task_no- 1)

                                with open(path, "w") as fs:
                                    fs.writelines(tasks)

                                print(f"Deleted task: {deleted_task.split()}")

                except FileNotFoundError:
                    print("Task file does not exist")

                except ValueError:
                    print("Please enter a valid task number")

            if choice == 5:
                print("Exit")
                break
            else:
                print("Invalid choice")

        except ValueError:
            print("Please enter a valid choice number")

to_do_list()