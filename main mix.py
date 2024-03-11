# All the imports
import csv
from collections import Counter
import datetime
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
import pandas as pd
import os
from PIL import Image, ImageFont, ImageDraw

# Get most recent csv
current_script_folder = os.path.dirname((os.path.abspath(__file__)))
project_folder = current_script_folder
csv_files = [f for f in os.listdir(project_folder) if
             f.endswith(".csv") and os.path.isfile(os.path.join(project_folder, f))]
if csv_files:
    most_recent_file = max(csv_files, key=lambda f: os.path.getmtime(os.path.join(project_folder, f)))


# Define the Semicolon Dialect
class SemiColonDialect(csv.excel):
    delimiter = ";"


def shall_we_go_on():
    global running
    print("-----------------------------------------------------------\n")
    print("Do you want to do anything else?\n"
          "0. No\n"
          "1. Yes\n")
    running = int(input())
    if running == 0:
        exit(99)


# Read CSV file line by line
with open(most_recent_file, 'r') as file:
    lines = file.readlines()

# Process each line and create a list of dictionaries
data = []
for line in lines:
    values = line.strip().split(';')
    data.append({f'Column_{i}': value for i, value in enumerate(values)})

# Create a DataFrame from the list of dictionaries
df_aff = pd.DataFrame(data)

# Optionally, transpose and abridge the DataFrame if needed
df_aff = df_aff.transpose()
df_aff.columns = df_aff.iloc[0]
df_aff = df_aff.drop(df_aff.index[0])
# # Convert csv data into dataframe, transpose, and abridge it
# df_aff = pandas.read_csv(most_recent_file, sep=";", header=None)
# df_aff = df_aff.transpose()
# df_aff.columns = df_aff.iloc[0]
# df_aff = df_aff.drop(df_aff.index[0])

# variables (check for necessity)
running = 1
task = 0
subtask = 0
leading_letter = "A"
query = ""
found_characters = []
found_characters_map = ""
character_names = []
aff_dict = {}
column_labels = df_aff.columns.tolist()
list_aff = df_aff.columns.tolist()
complete_char_list = aff_dict.values()
was_added_to = []
updated_affiliations = []

filename_main = "MCP.csv"
filename_copy = "MCP_{}.csv"
datetime_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
original_file = os.path.join(project_folder, filename_main)
copy_file = os.path.join(project_folder, "MCP_{}.csv".format(datetime_str))


# Define functions
###WORK CONTINUES HERE
def write_and_copy_csv():
    os.rename(original_file, copy_file)


for col in df_aff.columns:
    if col not in aff_dict:
        aff_dict[col] = []

for col in df_aff.columns:
    for cell in df_aff[col].dropna().values:
        if cell not in aff_dict[col]:
            aff_dict[col].append(cell)

# Convert data frame into a dictionary and get variables from it
aff_dict = {key: sorted(values) for key, values in sorted(aff_dict.items())}
affiliations = sorted(aff_dict.keys())
complete_char_list = aff_dict.values()
characters_by_aff = []
for affiliation in affiliations:
    characters_by_aff.append(aff_dict[affiliation])

while running == 1:
    # Choose the task that should be performed
    task = input("What would you like to do?\n"
                 "1. See all affiliations.\n"  # Broken
                 "2. See one affiliation.\n"
                 "3. See a character's affiliations.\n"  ##Broken
                 "4. Add a new affiliation.\n"
                 "5. Add a new character.\n"
                 "6. Add a character to an affiliation.\n"
                 "7. Remove a character from an affiliation.\n"
                 "8. Create a picture of an affiliation\n"
                 "9. See the gaps in your collection\n"
                 "10. Rank affiliations by missing characters\n"
                 "11. Add a character to your collection\n")
    if not task.isdigit():
        print("Please input a valid choice.\n")
        continue
    if not 0 < int(task) < 12:
        print("Please input a valid choice.\n")
        continue
    task = int(task)

    # Task 1: See all affiliations
    if task == 1:
        df_aff = df_aff.fillna("")
        print(df_aff.to_string(index=False))
        shall_we_go_on()
        continue

    # Task 2: See one affiliation
    elif task == 2:
        print("Choose an affiliation:")
        for i, header in enumerate(df_aff, start=1):
            print(f"{i}. {header}")
            max_header = max(enumerate(df_aff, start=1))
            max_header = int(max_header[0])
        # Choose affiliation to show
        subtask = input()

        # Error code
        if not subtask.isdigit():
            print("Please input a valid choice.\n")
            continue
        try:
            subtask = int(subtask)
            selected = list_aff[subtask - 1]
        except IndexError:
            print("Please input a valid choice.\n")
            continue
        # Drop all the empty cells
        non_empty_rows = df_aff.dropna(subset=selected)
        # Show yourself
        print(selected)
        print(f"{non_empty_rows[selected].to_string(index=False)}")
        shall_we_go_on()
        continue

    # Task 3: See a character's affiliations
    elif task == 3:
        leading_letter = input("Which character are you looking for? Please enter the exact first letter.").upper()
        # Put all characters in the results list
        if not leading_letter.isalpha():
            print("Please input a valid choice.\n")
            continue
        results = []
        for value in aff_dict.values():
            for entry in value:
                if entry.startswith(leading_letter) and entry not in results:
                    results.append(entry)
                    results = sorted(results)
        print("Please choose a character:")
        for index, entry in enumerate(results, 1):
            print(f"{index}. {entry}")
        # Choose a character
        subtask = input()
        # Error code
        if not subtask.isdigit():
            print("Please input a valid choice.\n")
            continue
        try:
            subtask = int(subtask)
            selected = list_aff[subtask - 1]
        except IndexError:
            print("Please input a valid choice.\n")
            continue
        query = results[int(subtask) - 1]
        aff_dict_keys = aff_dict.keys()
        # Find the affiliation
        matching_keys = [key for key in aff_dict_keys if query in aff_dict[key]]
        print(matching_keys)
        print(f"{query} is affiliated with the following affiliations:")
        for key in matching_keys:
            print(key)
        shall_we_go_on()
        continue

    # Task 4: Add a new affiliation
    elif task == 4:
        print("Current affiliations:")
        for i, header in enumerate(df_aff, start=1):
            print(f"{i}. {header}")
        new_affiliation = input("Enter the name of the new affiliation:")
        aff_dict_keys = aff_dict.keys()
        if new_affiliation not in aff_dict_keys:
            aff_dict[new_affiliation] = []
        print(aff_dict_keys)
        datetime_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.rename(original_file, copy_file)
        with open(copy_file, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            existing_data = list(csv_reader)
        existing_data.append([new_affiliation])
        with open(filename_main, "w") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(existing_data)
            csv_file.close()
        # os.rename("C:\PythonProjects\MCP Affiliations\MCP_{}.csv".format(datetime_str), "C:\PythonProjects\MCP Affiliations\MCP.csv")
        shall_we_go_on()
        continue

    # Task 5: Add a new character
    elif task == 5:
        new_character = input("Enter the name of the new character:")
        if new_character in complete_char_list:
            print("Character already included")
            exit(55)
        more_aff = 1
        print("Which affiliations does the character belong to?")

        while more_aff == 1:
            for i, header in enumerate(df_aff, start=1):
                print(f"{i}. {header}")
            subtask = input()
            # Error code
            if not subtask.isdigit():
                print("Please input a valid choice.\n")
                continue
            try:
                subtask = int(subtask)
                add_to = list_aff[subtask - 1]
            except IndexError:
                print("Please input a valid choice.\n")
                continue

            was_added_to = was_added_to + [add_to]
            existing_characters = aff_dict[add_to]
            aff_dict[add_to].append(new_character)
            updated_affiliations.append((add_to, aff_dict[add_to]))
            more_aff = int(input("Align with more affiliations?\n"
                                 "0. No\n"
                                 "1. Yes\n"))
            write_and_copy_csv()
            with open(copy_file, "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                existing_data = list(csv_reader)
            with open(filename_main, "w") as csv_file:
                csv_writer = csv.writer(csv_file, dialect=SemiColonDialect)
                for key, values in aff_dict.items():
                    csv_writer.writerow([key] + values)
                csv_file.close()
            for i in was_added_to:
                print(f"{i} updated in CSV.")
            continue
        if more_aff == 0:
            shall_we_go_on()
            continue

    # Task 6: Add a character to an affiliation
    elif task == 6:
        print("Choose an affiliation:")
        for i, header in enumerate(df_aff, start=1):
            print(f"{i}. {header}")
        subtask = input()
        # Error code
        if not subtask.isdigit():
            print("Please input a valid choice.\n")
            continue
        try:
            subtask = int(subtask)
            selected = list_aff[subtask - 1]
        except IndexError:
            print("Please input a valid choice.\n")
            continue

        all_characters = set(char for chars in aff_dict.values() for char in chars)
        characters_not_in_selected = all_characters - set(aff_dict[selected])
        print("Choose a character to add:")
        for i, char in enumerate(characters_not_in_selected):
            if char != "":
                print(f"{i}. {char}")
        viable_list = list(characters_not_in_selected)
        subtask = int(input())
        aff_dict[selected].append(viable_list[subtask])
        datetime_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        write_and_copy_csv()
        with open(copy_file, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            existing_data = list(csv_reader)
        with open(filename_main, "w") as csv_file:
            csv_writer = csv.writer(csv_file, dialect=SemiColonDialect)
            for key, values in aff_dict.items():
                csv_writer.writerow([key] + values)
            csv_file.close()
        print(f"{selected} updated in CSV.")
        shall_we_go_on()
        continue

    elif task == 7:
        print("Choose an affiliation:")
        for i, header in enumerate(df_aff, start=1):
            print(f"{i}. {header}")
        subtask = input()
        # Error code
        if not subtask.isdigit():
            print("Please input a valid choice.\n")
            continue
        try:
            subtask = int(subtask)
            add_to = list_aff[subtask - 1]
        except IndexError:
            print("Please input a valid choice.\n")
            continue

        print("Choose a character to remove:")
        for i, char in enumerate(aff_dict[selected]):
            if char != "":
                print(f"{i}. {char}")

        subtask = input()
        # Error code
        if not subtask.isdigit():
            print("Please input a valid choice.\n")
            continue
        try:
            subtask = int(subtask)
            selected = list_aff[subtask - 1]
        except IndexError:
            print("Please input a valid choice.\n")
            continue

        aff_dict[selected].pop(subtask)
        print(aff_dict[selected])
        write_and_copy_csv()
        with open(copy_file, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            existing_data = list(csv_reader)
        with open(filename_main, "w") as csv_file:
            csv_writer = csv.writer(csv_file, dialect=SemiColonDialect)
            for key, values in aff_dict.items():
                csv_writer.writerow([key] + values)
            csv_file.close()
        print(f"{selected} updated in CSV.")
        shall_we_go_on()
        continue

    elif task == 8:
        print("Choose an affiliation:")
        for i, header in enumerate(df_aff, start=1):
            print(f"{i}. {header}")
        subtask = input()
        # Error code
        if not subtask.isdigit():
            print("Please input a valid choice.\n")
            continue
        try:
            subtask = int(subtask)
            selected = list_aff[subtask - 1]
        except IndexError:
            print("Please input a valid choice.\n")
            continue
        non_empty_rows = df_aff.dropna(subset=selected)
        output_list = []

        bg_color = (255, 255, 0)  # yellow
        size = (400, 800)
        bg_im = Image.open("C:/PythonProjects/MCP Affiliations/Download.jpg")

        if bg_im.size != size:
            bg_im = bg_im.resize(size)
        im = Image.new("RGB", size)
        im.paste(bg_im)
        font_path = "C:/PythonProjects/MCP Affiliations/AvengeanceHeroicAvengerNormal-Bz7d.ttf"
        font = ImageFont.truetype(font_path, 18)
        # Image Centre
        draw = ImageDraw.Draw(im)
        draw.text((150, 20), f"{selected}\n", font=font, fill=(0, 0, 0))
        for character in non_empty_rows[selected]:
            output_list.append(character.strip())

        output_list = "\n".join(output_list)
        draw.text((30, 80), output_list, font=font, fill=(0, 0, 0))

        draw = ImageDraw.Draw(im)

        im.save(f"{selected}.png")
        ###I may still want centre aligned, wraparound, and automatic font size
        shall_we_go_on()
        continue
    # See collection gaps
    elif task == 9:
        ownership_file = os.path.join(project_folder, "Ownership.csv")
        df_own = pd.read_csv(ownership_file, sep=";", header=None)
        df_own.columns = df_own.iloc[0]
        ownership_list = list(df_own.columns)

        unique_file = os.path.join(project_folder, "MCP_NoLead.csv")
        # df_unique = pd.read_csv(unique_file,sep=";",header=None)

        with open(unique_file, 'r') as file:
            lines = file.readlines()

        # Process each line and create a list of dictionaries
        missing_characters = []
        for line in lines:
            values = line.strip().split(';')
            missing_characters.append({f'Column_{i}': value for i, value in enumerate(values)})

        # Create a DataFrame from the list of dictionaries
        df_unique = pd.DataFrame(missing_characters)

        # Optionally, transpose and abridge the DataFrame if needed
        df_unique = df_unique.transpose()
        df_unique.columns = df_unique.iloc[0]
        df_unique = df_unique.drop(df_unique.index[0])

        missing_characters = df_unique.stack().unique().tolist()

        new_missing_characters = [character for character in missing_characters if character not in ownership_list]
        missing_characters = sorted(new_missing_characters)

        print("\n".join(map(str, missing_characters)))
        exit(9)
    # Rank affiliations by missing models

    elif task == 10:
        ownership_file = os.path.join(project_folder, "Ownership.csv")
        df_own = pd.read_csv(ownership_file, sep=";", header=None)
        df_own.columns = df_own.iloc[0]
        ownership_list = list(df_own.columns)

        unique_file = os.path.join(project_folder, "MCP_NoLead.csv")
        missing_characters = pd.read_csv(unique_file, sep=";", header=None)
        missing_characters = missing_characters.transpose()
        missing_characters.columns = missing_characters.iloc[0]
        # missing_characters = missing_characters.fillna("")
        missing_characters = missing_characters.drop(missing_characters.index[0])

        miss_by_aff = {}

        for col in missing_characters.columns:
            if col not in miss_by_aff:
                miss_by_aff[col] = []

        for col in missing_characters.columns:
            for cell in missing_characters[col].dropna().values:
                if cell not in miss_by_aff[col]:
                    miss_by_aff[col].append(cell)

        for key, values in miss_by_aff.items():
            miss_by_aff[key] = [value for value in values if value not in ownership_list]


        def count_values_in_dict(dictionary):
            counts = []
            for key, values in dictionary.items():
                if not values:
                    counts.append((key, -99))
                else:
                    counts.append((key, len(values)))

            sorted_counts = sorted(counts, key=lambda x: x[1])

            for key, count in sorted_counts:
                print(f"{key}: {'Complete' if count == -99 else count}")
                if count != -99:
                    print("\t", end="")
                    print(", ".join(dictionary[key]))


        def most_common_value(dictionary, n=1):
            # Flatten the values into a single list
            all_values = [value for values in dictionary.values() for value in values]

            # Count the occurrences of each value
            value_counts = Counter(all_values)

            # Find the value with the highest count
            most_common_values = value_counts.most_common()

            return most_common_values


        # Example usage:
        top_values = most_common_value(miss_by_aff, n=1)
        count_values_in_dict(miss_by_aff)

        print("\nCharacters with most affiliations:\n")
        for rank, (value, count) in enumerate(top_values, start=1):
            print(f"{rank}. '{value}' with {count} occurrences.")


        def calculate_buying_index_affiliation(character, affiliation_counts):
            # Calculate the average value for the affiliations
            if len(affiliation_counts) == 0:
                return 0
            average_affiliation_value = sum(affiliation_counts.values()) / len(affiliation_counts)

            # Calculate the buying index
            buying_index = average_affiliation_value - len(affiliation_counts)

            return buying_index


        buying_indices_aff = {}

        for character, affiliations in miss_by_aff.items():
            # Calculate the counts of affiliations for the character
            affiliation_counts = Counter(affiliations)

            # Calculate the buying index for the affiliation
            buying_index = calculate_buying_index_affiliation(character, affiliation_counts)

            # Store the buying index in the dictionary
            buying_indices_aff[character] = buying_index

        # Sort characters based on buying index in ascending order
        sorted_characters = sorted(buying_indices_aff.items(), key=lambda x: x[1])

        # Display the sorted characters with buying indices
        print("\nAffiliation Buying Index:")
        for rank, (character, buying_index) in enumerate(sorted_characters, start=1):
            print(f"{rank}. '{character}' with Buying Index: {buying_index}")
            # for value in miss_by_aff:
            #     if value == "":
            #         del value
            # print (miss_by_aff)
            # print (miss_by_aff)


        def calculate_buying_index(character, affiliations):
            # Check if there are no affiliations for the character
            if not affiliations:
                return 0  # or any default value you want to assign

            # Calculate the counts of affiliations for the character
            affiliation_counts = Counter(affiliations)

            # Calculate the average value for the affiliations
            average_affiliation_value = sum(affiliation_counts.values()) / len(affiliation_counts)

            # Calculate the buying index
            buying_index = average_affiliation_value - len(affiliation_counts)

            return buying_index


        buying_indices_char = {}

        for affiliation, characters in miss_by_aff.items():
            for character in characters:
                buying_index = calculate_buying_index(character, characters)

                # Store the buying index in the dictionary
                if character not in buying_indices_char:
                    buying_indices_char[character] = []
                buying_indices_char[character].append(buying_index)

            # Calculate the average buying index for each character
        average_buying_indices = {character: sum(indices) / len(indices) if indices else 0 for character, indices in
                                  buying_indices_char.items()}

        # Sort characters based on average buying index in ascending order
        sorted_characters = sorted(average_buying_indices.items(), key=lambda x: x[1], reverse=True)

        # Display the sorted characters with average buying indices
        print("\nCharacters with Buying Index:")
        for rank, (character, avg_buying_index) in enumerate(sorted_characters, start=1):
            print(f"{rank}. '{character}' with Average Buying Index: {avg_buying_index}")
        exit(4)
        ###use this

    elif task == 11:
        ownership_file = os.path.join(project_folder, "Ownership.csv")
        df_own = pd.read_csv(ownership_file, sep=";", header=None)
        df_own.columns = df_own.iloc[0]
        ownership_list = list(df_own.columns)
        ownership_list = [str(item) for item in ownership_list]
        unique_file = os.path.join(project_folder, "MCP_NoLead.csv")
        # df_unique = pd.read_csv(unique_file,sep=";",header=None)

        with open(unique_file, 'r') as file:
            lines = file.readlines()

        # Process each line and create a list of dictionaries
        missing_characters = []
        for line in lines:
            values = line.strip().split(';')
            missing_characters.append({f'Column_{i}': value for i, value in enumerate(values)})

        # Create a DataFrame from the list of dictionaries
        df_unique = pd.DataFrame(missing_characters)

        # Optionally, transpose and abridge the DataFrame if needed
        df_unique = df_unique.transpose()
        df_unique.columns = df_unique.iloc[0]
        df_unique = df_unique.drop(df_unique.index[0])

        missing_characters = df_unique.stack().unique().tolist()

        new_missing_characters = [character for character in missing_characters if character not in ownership_list]
        missing_characters = sorted(new_missing_characters)
        for i, character in enumerate(missing_characters):
            print(f"{i}. {character}")
        character_to_add_nr = int(input("Enter the character's number."))
        character_to_add_name = missing_characters[character_to_add_nr]
        print (character_to_add_name)
        ownership_list.append(character_to_add_name)
        with open(ownership_file, 'w') as file:
            file.write(';'.join(ownership_list))
        shall_we_go_on()
