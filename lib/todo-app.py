import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, TodoList, Task

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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
        print(f'Nice to meet you {user.username}!\n')
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

def delete_user(user_id, current_user):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        todo_lists = get_todo_lists_for_user(user.id)
        for todo_list in todo_lists:
            tasks = session.query(Task).filter_by(todo_list_id=todo_list.id).all()
            for task in tasks:
                session.delete(task)
            session.delete(todo_list)
        session.delete(user)
        session.commit()
        if current_user.id == user_id:
            current_user = None
        print(f"User \033[91m{user.username}\033[0m deleted\n")
    else:
        print(f"\n\033[91mNo user found with ID {user_id}\033[0m\n")



def create_todo_list(name, user_id):
    todo_list = TodoList(name=name, user_id=user_id)
    session.add(todo_list)
    session.commit()
    return todo_list


def get_todo_lists_for_user(user_id):
    print('\033[34m' + f"\nHere are {current_user.username}'s ToDo-Lists:\n" + '\033[0m')
    return session.query(TodoList).filter_by(user_id=user_id).all()



def delete_todo_list(todo_list_id):
    todo_list = session.query(TodoList).filter_by(id=todo_list_id).first()
    if todo_list:
        # delete tasks in list
        session.query(Task).filter_by(todo_list_id=todo_list_id).delete()
        session.delete(todo_list)
        session.commit()
        print(f"Todo list \033[91m{todo_list.name}\033[0m deleted")
    else:
        print('\033[91mTodo list not found\033[0m')


def create_task(description, todo_list_id):
    todo_list = session.query(TodoList).filter_by(id=todo_list_id).first()
    if todo_list:
        task = Task(description=description, todo_list_id=todo_list_id)
        session.add(task)
        session.commit()
        
    else:
        
        print('\033[91mTodo list not found\033[0m')

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
    print('\033[33m' + 'Welcome to the Todo List App! Please login.\n' + '\033[0m')
    while True:
        if current_user:
            print('\033[32m' + f'Logged in as {current_user.username}\n' + '\033[0m')
            print('1. Switch user')
            print('2. Get all users')
            print('3. Create todo list')
            print('4. Get all todo lists for the current user')
            print('5. Delete todo list')
            print('6. Create task')
            print('7. Get tasks for the current user')
            print('8. Delete user')
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
                    print('\n\033[91mUser not found\033[0m\n')
        elif choice == '0':
            clear_screen()
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
            if len(name) > 0:
                create_todo_list(name, user_id)
                print(f'Todo list \033[34m{name}\033[0m created\n')

            else:
                print("\033[91mName must be more than 1 character.\n\033[0m")
                

            
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
                    print('\033[91mTodo list not found\033[0m')
                else:
                    description = input('\nEnter task description: ')
                    if len(description) > 0:
                        task = Task(description=description, todo_list_id=todo_list.id)
                        session.add(task)
                        session.commit()
                        print(f'\nTask "\033[34m{task.description}\033[0m" added to todo list "\033[34m{todo_list.name}\033[0m"')
                    else:
                        print("\nDescription must be over 1 character.\n")
                
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
                    todo_list_id = input('\nEnter the ID of the Todo list to get tasks for: ')
                    selected_todo_list = session.query(TodoList).filter_by(id=todo_list_id).first()
                    print("")
                    tasks = session.query(Task).filter_by(todo_list_id=todo_list_id).all()
                    if not tasks:
                        print('\033[31mNo tasks found for the selected Todo list\033[0m')
                    else:
                        
                        print(f'\033[34mHere are the tasks in \'{selected_todo_list.name}\'\n\033[0m\n')
                        for task in tasks:
                            print(f'{task.id} | {task.description}')
                    input('\nPress Enter to continue...')
                    print("")
        elif choice == '8':
            if not current_user:
                print('No current user set')
            else:
                users = get_all_users()
                if not users:
                    print('No users found')
                else:
                    print("")
                    for user in users:
                        print(f'{user.id} | {user.username}')
                    print("")
                    user_id = input('Enter user ID to delete: ')
                    delete_user(user_id, current_user)
                    
                

                
if __name__ == '__main__':
    run_todo_list_app()
