import xlsxwriter
import json
import csv
import pyautogui


MAX_SCORER = 100
TYPE_OFFSET = 5
TOTAL_RACES = 8
MIN_WEEK = 1
RESULTS_STR = "results.txt"
SCOREBOARD_STR = "scoreboard"
BACKUP_STR = "backup"
COMPETITORS_STR = "competitors.csv"


def main():
    """
    Writes an .xlsx file containing the points and positions
    of all competitors in the marble racing tournament.
    Provides a menu system for it.
    """

    competitors = Competitors("../../data/basic/probyuser.csv")
    scoreboard = Scoreboard(SCOREBOARD_STR + ".json", competitors.get_flair_dict())

    print("\n--- The Confluence Marble Racing Menu ---\n")
    print(f"{scoreboard.races} race(s) so far")
    print_instructions()

    print()
    option = input("Type here: ")
    while option != "quit":

        # Get list
        if option == "list":
            competitors.save_list(MIN_WEEK, COMPETITORS_STR)
            print(f"List saved as '{COMPETITORS_STR}'!")

        # Add race
        elif option == "add":
            scoreboard.add_race(RESULTS_STR)
            scoreboard.save_all(SCOREBOARD_STR)
            print(f"Race added! ({scoreboard.races} total)")
            print(f"Updated scoreboard saved as '{SCOREBOARD_STR}'")

        # Remove race
        elif option == "remove":
            scoreboard.remove_race()
            scoreboard.save_all(SCOREBOARD_STR)
            print(f"Race removed! ({scoreboard.races} total)")
            print(f"Updated scoreboard saved as '{SCOREBOARD_STR}'")

        # Clear all
        elif option == "clear":
            scoreboard.save_all(BACKUP_STR)
            scoreboard.clear_all()
            scoreboard.save_all(SCOREBOARD_STR)
            print("Data cleared!")
            print(f"Created a backup as '{BACKUP_STR}' and saved" +
                f" the empty scoreboard as '{SCOREBOARD_STR}'"
            )

        # Autotype
        elif option == "type":
            print(f"Starting to type in {TYPE_OFFSET} second(s)! ({MAX_SCORER} numbers)")
            autotype()

        # Debug
        elif option == "debug":
            print(get_keystrokes(123))

        # Help
        elif option == "help":
            print_instructions()

        # Command not recognized
        else:
            print("Command not recognized")
            print_instructions()

        print()
        option = input("Type here: ")


class Scoreboard():
    """Contains the data of all competitors"""


    def __init__(self, filename: str, competitors: dict[str, int]):
        """
        Reads a .json file and creates a dictionary containing all
        the data corresponding to each competitor, each entry having
        a position, an individual score and a total score
        """

        self.competitors = competitors

        with open(filename, "r") as f:
            self.data: dict[str, list[dict[str, int]]] = json.load(f)
        
        # Count how many entries are in the first user
        keys = list(self.data)
        if len(keys) > 0:
            self.races = len(self.data[keys[0]])
        else:
            self.races = 0


    def __getitem__(self, username: str) -> list[int]:
        """
        Returns the positions of a specific user as a list
        """

        return self.data[username]

    
    def get_dict(self) -> dict[str, list[dict[str, int]]]:
        """
        Returns the data contained in the object
        """

        return self.data

    
    def get_sorted_by(self, option: str) -> dict[str, list[dict[str, int]]]:
        """
        Returns the data sorted by the selected option
        """

        # Select sorting method
        if option == "points":
            sorting_key = lambda x: x[1][-1]["total"]
        elif option == "flair":
            sorting_key = lambda x: self.competitors[x[0]]
        elif option == "username":
            sorting_key = lambda x: x[0]

        # Create a list out of data to be sorted
        listed = list(self.data.items())

        try:
            sorted_list = list(sorted(
                listed,
                key=sorting_key,
                # We only want descending order when sorting by points
                reverse=(option == "points")   
            ))

        # Username not found when sorting by flair
        except KeyError as e:
            print(f"ERROR: Username not found: {e}")
            print("Defaulting to unsorted...")
            return self.data

        # Convert to dict
        return { username: user for username, user in sorted_list }


    def get_positions(self) -> dict[str, int]:
        """
        Returns a dict containing the current position of each user
        """

        sorted_list = list(self.get_sorted_by("points"))

        return { username: index + 1 for index, username in enumerate(sorted_list) }


    def clear_all(self) -> None:
        self.data = {}
        self.races = 0


    def remove_race(self) -> None:
        """
        Removes the last race data from all users
        """

        # Don't do anything if already at 0
        if self.races == 0:
            return

        self.races -= 1

        # Delete everything if there are no races left
        if self.races == 0:
            self.data = {}
        else:
            for username, user in self.data.items():
                user.pop()


    def add_race(self, filename: str) -> None:
        """
        Reads a file containing the results of the last race and
        updates the competitors' data accordingly
        """

        self.races += 1

        # Read the file
        with open(filename, "r") as f:
            results = [ username.strip() for username in f.readlines() ]

        # Handle each user
        for position, username in enumerate(results):
            score = get_score(position + 1)

            # Already existing user
            if username in self.data:
                user = self.data[username]
                user.append({
                    "position": position + 1,
                    "individual": score,
                    "total": user[-1]["total"] + score
                })

            # New user
            else:
                user = []
                # Fill with zeros up to last race
                for i in range(self.races - 1):
                    user.append({
                        "position": 0,
                        "individual": 0,
                        "total": 0
                    })
                # Last race
                user.append({
                    "position": position + 1,
                    "individual": score,
                    "total": score
                })
                self.data[username] = user


        # Handle users that abandoned
        for username, user in self.data.items():
            if len(user) < self.races:
                user.append({
                    "position": 0,
                    "individual": 0,
                    "total": user[-1]["total"]
                })


    def save_json(self, filename: str) -> None:
        """
        Saves the data to a .json file
        """

        with open(filename, "w") as f:
            json.dump(self.data, f, indent=4)

    
    def save_xlsx(self, filename: str) -> None:
        """
        Saves the data to a .xlsx file
        """

        workbook = xlsxwriter.Workbook(filename)

        # Auxiliary
        positions = self.get_positions()
        sheets = ("points", "username", "flair")
        looper = (
            (f"Sorted by {option}", self.get_sorted_by(option)) for option in sheets
        )

        # Create two copies, one sorted by position and the other by flair
        for worksheet, dataset in looper:
            sheet = workbook.add_worksheet(worksheet)

            # Format presets
            center = workbook.add_format({"align": "center"})
            bold = workbook.add_format({"bold": True, "align": "center"})
            grey = workbook.add_format({"pattern": 1, "bg_color": "CCCCCC"})

            # Formatting
            sheet.set_column(0, self.races + 3, 10, center)
            sheet.set_column(1, 1, 20)
            sheet.set_column(2, 3, 15)

            # Titles row
            sheet.set_row(0, 18, bold)
            sheet.write(0, 0, "Flair")
            sheet.write(0, 1, "Username")
            sheet.write(0, 2, "Position")
            sheet.write(0, 3, "Total Points")
            for i in range(TOTAL_RACES):
                sheet.write(0, 4 + i, f"Race {i+1}")

            # Loop through users
            row = 1
            for username, user in dataset.items():
                # Flair
                try:
                    sheet.write(row, 0, self.competitors[username])
                # Username not found, most likely a typo
                except KeyError:
                    print(f"ERROR: Username not found: '{username}'")
                    print("Writing 'N/A'...")
                    sheet.write(row, 0, "N/A")

                # Username
                sheet.write(row, 1, username)

                # Position
                position = positions[username]
                sheet.write(row, 2, f"{position}{self.get_end(position)}")

                # Total Points
                sheet.write(row, 3, user[-1]["total"])

                # Loop through race data
                col = 4
                for race in user:
                    # Only write data if participated
                    if (pos := race["position"]) != 0:
                        sheet.write(row, col, f"{pos}{self.get_end(pos)} (+{race['individual']})")
                    # Else grey it out
                    else:
                        sheet.write(row, col, "", grey)
                    col += 1

                row += 1
                
        workbook.close()

    
    def save_all(self, filename: str) -> None:
        xlsxfilename = filename + ".xlsx"
        jsonfilename = filename + ".json"

        self.save_xlsx(xlsxfilename)
        self.save_json(jsonfilename)


    def get_score(self, position: int) -> int:
        """
        Returns the score corresponding to
        a given position in a race
        """

        # Did not participate
        if position == 0:
            return 0

        # Nice.
        if position == 69:
            return 6

        if position <= 1:
            return 30
        elif position <= 3:
            return 25
        elif position <= 10:
            return 20
        elif position <= 20:
            return 15
        elif position <= 50:
            return 10
        elif position <= 100:
            return 5
        else:
            return 0


    def get_end(self, number: int) -> str:
        """
        Returns "st" for 1, "nd" for 2, "rd" for 3 and "th" othewise
        """

        if number == 1:
            return "st"
        elif number == 2:
            return "nd"
        elif number == 3:
            return "rd"
        else:
            return "th"


class Competitors():
    """
    Class containing the logic behind eligible competitors
    """

    def __init__(self, filename: str):
        """
        Loads data from csv file and stores it in a dict
        """

        self.data: dict[str, list[int]] = {}

        with open(filename, "r", newline="") as f:
            reader = csv.reader(f)
            # { username: [flairs] }
            for row in reader:
                username = row[0]
                flairs = [ int(flair) for flair in row[1:] ]
                self.data[username] = flairs


    def get_flair_dict(self) -> int:
        """
        Returns all current flairs as a dict
        """

        return { username: flairs[-1] for username, flairs in self.data.items() }

    
    def get_elegible(self, min_weeks: int) -> list[str]:
        """
        Returns a dictionary with all members who have at least
        min_weeks stayed in The Confluence. Also, they have to be
        current members
        """

        eligible = [
            username for username, flairs in self.data.items()
            if flairs[-1] != 0 and flairs.count(0) < len(flairs) - min_weeks
        ]

        return eligible


    def save_list(self, min_weeks: int, filename: str) -> None:
        """
        Saves the list of eligible members to a file
        """

        eligible = self.get_elegible(min_weeks)

        with open(filename, "w") as f:
            f.writelines("\n".join(eligible))


def get_score(position: int) -> int:
    """
    Scoring function
    """

    if position >= 1 and position <= MAX_SCORER:
        return MAX_SCORER + 1 - position
    else:
        return 0


def get_keystrokes(number: int) -> list[str]:
    """
    Converts a number into a sequence of keystrokes
    """

    ans = []
    length = len(str(number))

    for i in range(length):
        ith_digit = number//pow(10, i) % 10
        print(ith_digit)
        ans.append(str(ith_digit))

    return reversed(ans)


def autotype() -> None:
    """
    Auto types the scores of each position, in descending order
    """

    pyautogui.sleep(TYPE_OFFSET)

    for i in range(MAX_SCORER):
        pyautogui.write(get_keystrokes(get_score(i+1)))
        pyautogui.write(["enter"])


def print_instructions() -> None:
    """
    Prints menu instructions
    """

    print("Insert one of the following options")
    print(f"list: Save list of competitors that stayed at least {MIN_WEEK} full week(s)")
    print(f"add: Read from '{RESULTS_STR}' and add race")
    print("remove: Remove a race from the scoreboard")
    print("clear: Clear all the data and create backup")
    print("type: Autofill scoring system in Marbles On Stream")
    print("debug: Execute some debugging code")
    print("help: Show the menu options")
    print("quit: Exit the program")


if __name__ == "__main__":
    main()
