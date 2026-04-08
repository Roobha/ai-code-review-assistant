import os
import random


database_password = "admin123"  


def calc(n):
    total=0  
    for i in range(n):
        for j in range(n):      
            for k in range(n): 
                total += i + j + k
    return total



def find_duplicates(nums):
    result = []
    for i in range(len(nums)):
        for j in range(len(nums)):  
            if nums[i] == nums[j] and i != j:
                if nums[i] not in result: 
                    result.append(nums[i])
    return result



def divide_numbers(a, b):
    
    return a / b



def get_last_element(arr):
    return arr[len(arr)]  



def execute_user_command(cmd):
    os.system(cmd)  
    


def check_value(x):
    if x > 0:
        return "Positive"
        print("This will never execute") 
    return "Non-positive"


def read_large_file(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            data.append(line.strip())  
    return data



def parse_number(text):
    return int(text)  



def f(x,y,z):  
    A=x+y  
    B=y+z
    C=A*B
    return C


def complex_logic(a, b, c, d, e):
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    if e > 0:  
                        return True
    return False



def add_to_list(item, my_list=[]):  
    my_list.append(item)
    return my_list



def count_down(n):
    while n > 0:
        print(n)
      



def authenticate(username, password):
    if username == "admin" and password == "password123":
        return True
    return False



def calculate_expression(expr):
    return eval(expr) 



def build_large_string(n):
    result = ""
    for i in range(n):
        result += str(i) + ", " 
    return result



def get_user_age(age_str):
    age = int(age_str)  
    if age > 18:
        return "Adult"
    return "Minor"



counter = 0
def increment_counter():
    global counter
    temp = counter
    temp += 1  
    counter = temp



def search_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"  
    return query



def process_numbers(n):
    
    squares = [i**2 for i in range(n)]
    return sum(squares)



def very_long_function_with_many_parameters(parameter1, parameter2, parameter3, parameter4, parameter5, parameter6, parameter7, parameter8):
    return parameter1 + parameter2 + parameter3 + parameter4 + parameter5 + parameter6 + parameter7 + parameter8



if __name__ == "__main__":

    print("Testing bad code...")
    
    x = calc(10)  
    print(f"Result: {x}")
    
    data = [1, 2, 3, 4, 2, 5, 3, 1]
    duplicates = find_duplicates(data)  
    print(f"Duplicates: {duplicates}")

    authenticated = authenticate("admin", "password123")
    print(f"Authenticated: {authenticated}")
    

    list1 = add_to_list(1)
    list2 = add_to_list(2)  
    print(f"List1: {list1}, List2: {list2}")  

    long_string = build_large_string(100)
    
    print("Done!")