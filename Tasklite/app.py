from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import DateTime
from colorama import Fore, Style, Back
import getpass
import re
from passlib.hash import bcrypt


#base class for creating models/tables
Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50))
    password = Column(String(255))
    email = Column(String(100), unique=True)
    
    #Relationships
    task = relationship("tasks", cascade="all, delete-orphan", back_populates='user')
    category = relationship("categories", back_populates='user')
    
    #method to hash the password
    def set_password(self, password):
        self.password = bcrypt.hash(password)
    
    #method to verify the password
    def verify_password(self, password):
        return bcrypt.check(password, self.password)
    
    
    
class Tasks(Base):
    __tablename__ = 'tasks'
    
    task_id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(25))
    description = Column(String(255))
    priority = Column(Integer)
    status = Column(String(10))
    create_at = Column(DateTime)
    updated_at = Column(DateTime)
    due_date = Column(DateTime)
    
    #Relationship
    user = relationship("users", back_populates='task')
    
class Category(Base):
    __tablename__ = 'categories'
    
    category_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(25))
    create_at = Column(DateTime)
    
    #Relationships
    user = relationship("users", back_populates='task')
    #create the SQLite engine
engine = create_engine('sqlite:///task.db')
    
    #function start

def login(): 
    username = input('Enter username: ')
    password = getpass('Enter password: ')
    
    #create a session to interact with the database
    with Session() as sesh:
        #retieve the user from the database
        user = sesh.query(Users).filter_by(username=username).first()
        
        #check if the user exists and if the password matches
        if user:
            if user.verify_password(password):
                print(f"{Fore.GREEN} Login successful {Style.RESET_ALL}")
                return user 
            else:
                print(f"{Fore.RED} Incorrect password try again {Style.RESET_ALL}")
                password = input('Enter password: ')
        else:
            print(f"{Fore.RED}{Style.BRIGHT} Username not found {Style.RESET_ALL}")
            register()
            
def register():
    print(f"{Fore.YELLOW}{Style.BRIGHT} Register a new account...{Style.RESET_ALL}")
    username = input('Enter username: ')
    password = input('Enter password: ')
    email = input('Enter email: ')
    
    #Create a session to interact with the database
    with Session() as sesh:
        #check if the username already exists
        existing_user = sesh.query(Users).filter_by((Users.username == username) | (Users.email == email)).first()
        if existing_user:
            print(f"{Fore.RED}{Style.BRIGHT} Username or email already exists {Style.RESET_ALL}")
        else:
            new_user = Users(username-username, email=email)
            new_user.set_password(password) #hash the password
            
            #add the new user to the session and commit to the database
            sesh.add(new_user)
            sesh.commit()
            print(f"{Fore.GREEN} {Style.BRIGHT}Registration successful! you can log in;.{Style.RESET_ALL}")

def add_task(user):
    title = input 
            
        
        
    
    
    #end function 
    
    #end function
    
    
    
#start the cli
#ensures that the function listed down can only run on this particulat file only
if __name__ == '__main__':
    
    #create a session inorder to interact   with the database
    Session = sessionmaker(bing=engine)
    
    #start by asking the user to login or register
    print(f"{Fore.CYAN} Welcome to TaskLite - Task Management CLI Application! {Style.RESET_ALL}")
    
    
    while True:
        auth_choice = input("Do you have an account? (y/n): ").lower()
        if auth_choice == 'y' or 'yes':
            user = login()
            if user: #proceed only if the user sucessfully logs in
                break 
        elif auth_choice == 'n' or 'no':
            register()
        else:
            print(f"{Fore.RED} Invalid input.Please enter yes or no.")
    
    help = f"""{Fore.CYAN}
    
    
    
    commands:
    1. Add a task to the database
    2. List all tasks
    3. Mark a task as completed
    4. Delete a task from the database
    5. Add a new category
    6. List all categories
    7. Exit the application
    
    """
    while True:
        print(help)
        userInput = input('Select an option: ')
        if userInput == '1':
            #add a task
            add_task()
        elif userInput == '2':
            #list all tasks
            pass
        elif userInput == '3':
            #mark a task as completed
            pass
        elif userInput == '4':
            #delete a task
            pass
        elif userInput == '5':
            #add a new category
            pass
        elif userInput == '6':
            #list all categories
            pass
        elif userInput == '7':
            #exit the application
            break
    
    