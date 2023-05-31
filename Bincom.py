import random
from collections import Counter
from statistics import variance

import psycopg2


monday=["GREEN", "YELLOW", "GREEN", "BROWN", "BLUE", "PINK", "BLUE", "YELLOW", "ORANGE", "CREAM", "ORANGE", "RED", "WHITE", "BLUE", "WHITE", "BLUE", "BLUE", "BLUE", "GREEN"]
tuesday=["ARSH", "BROWN", "GREEN", "BROWN", "BLUE", "BLUE", "BLUE", "PINK", "PINK", "ORANGE", "ORANGE", "RED", "WHITE", "BLUE", "WHITE", "WHITE", "BLUE", "BLUE", "BLUE"]
wednesday=["GREEN", "YELLOW", "GREEN", "BROWN", "BLUE", "PINK", "RED", "YELLOW", "ORANGE", "RED", "ORANGE", "RED", "BLUE", "BLUE", "WHITE", "BLUE", "BLUE", "WHITE", "WHITE"]
thursday=["BLUE", "BLUE", "GREEN", "WHITE", "BLUE", "BROWN", "PINK", "YELLOW", "ORANGE", "CREAM", "ORANGE", "RED", "WHITE", "BLUE", "WHITE", "BLUE", "BLUE", "BLUE", "GREEN"]
friday=["GREEN", "WHITE", "GREEN", "BROWN", "BLUE", "BLUE", "BLACK", "WHITE", "ORANGE", "RED", "RED", "RED", "WHITE", "BLUE", "WHITE", "BLUE", "BLUE", "BLUE", "WHITE"]


color_sequence = monday + tuesday + wednesday + thursday + friday


# Define a dictionary mapping color names to RGB values
color_rgb = {
    "GREEN": (0, 128, 0),
    "YELLOW": (255, 255, 0),
    "BROWN": (165, 42, 42),
    "BLUE": (0, 0, 255),
    "PINK": (255, 192, 203),
    "ORANGE": (255, 165, 0),
    "CREAM": (255, 253, 208),
    "RED": (255, 0, 0),
    "WHITE": (255, 255, 255),
    "ARSH": (178, 190, 181),
    "BLACK": (0, 0, 0)
}

# Convert color names to RGB values
rgb_sequence = [color_rgb[color] for color in color_sequence]


# 1. Which color of shirt is the mean color?


# Calculate the average RGB values
mean_rgb = tuple(int(sum(channel) / len(rgb_sequence)) for channel in zip(*rgb_sequence))

# Find the closest color name to the mean RGB values
mean_color = min(color_rgb, key=lambda color: sum(abs(c - m) for c, m in zip(color_rgb[color], mean_rgb)))

print(f"Mean color of shirt is:{mean_color}")


# 2.Which color is mostly worn throughout the week?

mode = max(color_sequence, key=color_sequence.count)

print(f"Most worn color throughout the week is {mode}")



# 3.Which color is the median?

median_color = color_sequence[(len(color_sequence)//2)]

print(f"Median color is {median_color}")



# 5.BONUS if a colour is chosen at random, what is the probability that the color is red?

# Count the occurrences of red in the list
red_count = color_sequence.count("RED")

# Calculate the probability
probability_red = red_count / len(color_sequence)

print(f"Probability of choosing red: {probability_red}")


# Calculate the percentage probability
percent_probability = probability_red * 100

print(f"Percent Probability of choosing red:{percent_probability} %")




# 6. Save the colours and their frequencies in postgresql database

# these are the db params i used locally
conn = psycopg2.connect(
    host="localhost",
    database="bincom",
    user="postgres",
    password="postgres"
)



cursor = conn.cursor()

# SQL statement to create the table
create_table_query = """
    CREATE TABLE bincom_color_data (
        id SERIAL PRIMARY KEY,
        color VARCHAR(255),
        frequency VARCHAR(255)
    )
"""

# Checks for the existence of the bincom_color_data table
cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'bincom_color_data')")
exists = cursor.fetchone()[0]


# Execute the create table query if table is not in existence
if not exists:
    cursor.execute(create_table_query)


color_counts = Counter(color_sequence)

for color, frequency in color_counts.items():
    query = f"INSERT INTO bincom_color_data (color, frequency) VALUES ('{color}', {frequency})"
    cursor.execute(query)


conn.commit()


select_query = "SELECT * FROM bincom_color_data"

cursor.execute(select_query)

rows = cursor.fetchall()

for row in rows:
    print(row)


cursor.close()
conn.close()




# 7.BONUS write a recursive searching algorithm to search for a number entered by user in a list of numbers.

def recursive_search(number, lst, start_index=0):
    # Base case: If the start_index exceeds the list length, the number is not found
    if start_index >= len(lst):
        return False

    # Base case: If the current element matches the number, return True
    if lst[start_index] == number:
        return True

    # Recursive case: Search the rest of the list starting from the next index
    return recursive_search(number, lst, start_index + 1)



numbers = [20, 13, 5, 8, 2, 10]
search_number = int(input("Enter a number to search for----> "))

if recursive_search(search_number, numbers):
    print(f" {search_number} is present in the list.")
else:
    print(f" {search_number} is not present in the list.")



# 8. Write a program that generates random 4 digits number of 0s and 1s and convert the generated number to base 10.


def generate_binary_to_decimal():

    binary_number = ""
    for _ in range(4):
        binary_number += str(random.randint(0, 1))

    # To base 10
    decimal_number = int(binary_number, 2)

    return binary_number, decimal_number


binary, decimal = generate_binary_to_decimal()

# Print the generated binary number and its base 10 equivalent
print("Generated Binary Number:", binary)
print("Decimal Equivalent:", decimal)




# 9. Write a program to sum the first 50 fibonacci sequence.

def fibonacci(n):
    fib_list = [0, 1]  

    for i in range(2, n):
        fib_list.append(fib_list[i - 1] + fib_list[i - 2])

    return sum(fib_list)

'''Calculate and print the first 10 Fibonacci numbers'''
fib_number = fibonacci(50)
print(f"The sum of the first 50 fibonacci numbers is {fib_number}")
