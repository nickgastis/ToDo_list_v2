import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, TodoList, Task

white = "\033[1;37"
red = "\033[1;31;"
yellow = "\033[4;33;49m"
green = "\033[1;32;"
magenta = "\033[1;35;"
cyan = "\033[1;36;49m"

engine = create_engine('sqlite:///todo.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

current_user = None


def login(username):
    global current_user
    user = session.query(User).filter_by(username=username).first()
    if user:
        print(f'Welcome back {user.username}!\n')
    else:
        user = User(username=username)
        session.add(user)
        session.commit()
        print(f'Welcome {user.username}!\n')
    current_user = user


def get_user_by_id(id):
    global current_user
    user = session.query(User).filter_by(id=id).first()
    if user:
        current_user = user
        return current_user
    else:
        return None


def get_all_users():
    return session.query(User).all()


def create_todo_list(name, user_id):
    todo_list = TodoList(name=name, user_id=user_id)
    session.add(todo_list)
    session.commit()
    return todo_list


def get_todo_lists_for_user(user_id):
    print(f"\nHere are {current_user.username}'s ToDo-Lists:\n")
    return session.query(TodoList).filter_by(user_id=user_id).all()



def delete_todo_list(todo_list_id):
    todo_list = session.query(TodoList).filter_by(id=todo_list_id).first()
    if todo_list:
        # delete tasks in list
        session.query(Task).filter_by(todo_list_id=todo_list_id).delete()
        session.delete(todo_list)
        session.commit()
        print(f'Todo list {todo_list.name} deleted')
    else:
        print('Todo list not found')


def create_task(description, todo_list_id):
    todo_list = session.query(TodoList).filter_by(id=todo_list_id).first()
    if todo_list:
        task = Task(description=description, todo_list_id=todo_list_id)
        session.add(task)
        session.commit()
        print(f'Task "{task.description}" added to todo list "{todo_list.name}"')
    else:
        print('Todo list not found')

def get_tasks_for_user(user_id):
    if not current_user:
        print('No current user set')
        return
    todo_lists = get_todo_lists_for_user(user_id)
    if not todo_lists:
        print('No todo lists found')
        return
    for todo_list in todo_lists:
        print(f'Todo list: {todo_list.name}')
        tasks = session.query(Task).filter_by(todo_list_id=todo_list.id).all()
        if tasks:
            for task in tasks:
                print(f'{task.id} | {task.description}')
        else:
            print('No tasks found')
        





def run_todo_list_app():
    os.system('clear') 
    print(f'Todo List App\n')
    while True:
        if current_user:
            print(f'Logged in as {current_user.username}\n')
            print('1. Get user by ID')
            print('2. Get all users')
            print('3. Create todo list')
            print('4. Get all todo lists for the current user')
            print('5. Delete todo list')
            print('6. Create task')
            print('7. Get tasks for the current user')
            print('0. Exit\n')
        else:
            print('1. Login')
            print('0. Exit')

        choice = input('Enter choice: ')

        if choice == '1':
            users = get_all_users()
            print("")
            for user in users:
                print(f'{user.id} | {user.username}')
            print("")
            if not current_user:
                username = input('Enter username: ')
                print("")
                login(username)
            else:
                
                id = input('Enter user ID: ')
                user = get_user_by_id(id)
                if user:
                    print(f'User: {user.username}\n')
                else:
                    print('User not found')
        elif choice == '0':
            break
                
        elif choice == '2':
            users = get_all_users()
            print("")
            for user in users:
                print(f'{user.id} | {user.username}')
            print("")
            input('Press Enter to continue...')
            print("")
        elif choice == '3':
            name = input('Enter todo list name: ')
            print("")
            user_id = current_user.id if current_user else input('Enter user ID: ')
            create_todo_list(name, user_id)
            print('Todo list created\n')
            
        elif choice == '4':
            if not current_user:
                print('No current user set')
            else:
                todo_lists = get_todo_lists_for_user(current_user.id)
                for todo_list in todo_lists:
                    print(f'{todo_list.id} | {todo_list.name}')
                print("")
            input('Press Enter to continue...')
            print("")
        elif choice == '5':
            if not current_user:
                print('No current user set')
            else:
                todo_lists = get_todo_lists_for_user(current_user.id)
                for todo_list in todo_lists:
                    print(f'{todo_list.id} | {todo_list.name}')
                print("")
                todo_list_id = input('Enter todo list ID to delete: ')
                print("")
                delete_todo_list(todo_list_id)
            input('\nPress Enter to continue...')
            print("")
        elif choice == '6':
            if not current_user:
                print('No current user set')
            else:
                todo_lists = get_todo_lists_for_user(current_user.id)
                if not todo_lists:
                    print('No Todo lists found')
                    run_todo_list_app()

                else:
                    for todo_list in todo_lists:
                        print(f'{todo_list.id} | {todo_list.name}')
                todo_list_id = input('\nEnter the ID of the Todo list to add the task to: ')

                todo_list = session.query(TodoList).filter_by(id=todo_list_id).first()
                if not todo_list:
                    print('Todo list not found')
                else:
                    description = input('\nEnter task description: ')
                    task = Task(description=description, todo_list_id=todo_list.id)
                    session.add(task)
                    session.commit()
                    print(f'\nTask "{description}" created and added to Todo list "{todo_list.name}"\n')
        elif choice =='7':
            if not current_user:
                print('No current user set')
            else:
                todo_lists = get_todo_lists_for_user(current_user.id)
                if not todo_lists:
                    print('No Todo lists found')
                    run_todo_list_app()
                else:
                    for todo_list in todo_lists:
                        print(f'{todo_list.id} | {todo_list.name}')
                    todo_list_id = input('Enter the ID of the Todo list to get tasks for: ')
                    tasks = session.query(Task).filter_by(todo_list_id=todo_list_id).all()
                    if not tasks:
                        print('No tasks found for the selected Todo list')
                    else:
                        for task in tasks:
                            print(f'{task.id} | {task.description}')

                



        # elif choice == '0':
        #         break


        # else:
        #     print('Invalid choice')
        #     input('Press Enter to continue...\n')


if __name__ == '__main__':
    run_todo_list_app()
