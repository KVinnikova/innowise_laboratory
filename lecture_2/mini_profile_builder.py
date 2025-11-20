from itertools import islice

'''Determining the stage of life by age'''
def generate_profile(age):
    if 0 <= age <= 12:
        return 'Child'
    elif 13 <= age <= 19:
        return 'Teenager'
    elif age >= 20:
        return 'Adult'

# Greeting the user and getting basic information
print("Welcome to the profile builder!")
user_name = input("Enter your full name: ")
birth_year_str = input("Enter your birth year: ")
birth_year = int(birth_year_str)
current_year = 2025
current_age = current_year - birth_year
hobbies = list()
hobby = ''

while hobby.lower() != 'stop':
    hobby = input("Enter a favorite hobby or type 'stop' to finish: ")
    if hobby.lower() != 'stop':
        hobbies.append(hobby)

life_stage = generate_profile(current_age)

# Creating and displaying the final profile
user_profile = {
    'Name': user_name,
    'Age': current_age,
    'Life stage': life_stage,
    'Favorite Hobbies': hobbies
}

print(f"---\nProfile Summary:")
for key, value in islice(user_profile.items(), 3):
    print(f"{key}: {value}")

if len(hobbies) == 0:
    print("You didn't mention any hobbies.")
else:
    print(f"Favorite Hobbies ({len(hobbies)}):")
    for hobby in hobbies:
        print(f"- {hobby}")
print('---')

