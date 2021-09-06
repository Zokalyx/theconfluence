import xlsxwriter
import json
import csv
import pyautogui


TEST_MODE = False
RACE_CUTOFF = 4
MAX_SCORER = 100
TYPE_OFFSET = 5
TOTAL_RACES = 8
MIN_WEEK = 1
RESULTS_STR = "results.txt"
SCOREBOARD_STR = "scoreboard"
BACKUP_STR = "backup"
COMPETITORS_STR = "competitors.csv"
RANDOM_STR = "random.csv"


def main():
    """
    Menu for managing marble races
    """
    global TEST_MODE

    competitors = Competitors("../../data/basic/probyuser.csv")
    scoreboard = Scoreboard(SCOREBOARD_STR + ".json", competitors.get_flair_dict())

    print("\n--- The Confluence Marble Racing Menu ---\n")
    print(f"{scoreboard.races} race(s) so far")
    print(f"Test mode is {'ON' if TEST_MODE else 'OFF'}")
    print_instructions()

    print()
    option = input("Type here: ")
    while option != "quit":

        # Get random
        if option == "random":
            create_random(RANDOM_STR, read_int("Amount: "))
            print(f"Random list saved as '{RANDOM_STR}'!")

        # Get list
        elif option == "list":
            competitors.save_list(COMPETITORS_STR, scoreboard.races)
            print(f"List saved as '{COMPETITORS_STR}'!")

        # Add race
        elif option == "add":
            scoreboard.add_race(RESULTS_STR, read_int("First marble to place as DNF (0 if none): "))
            scoreboard.save_all(SCOREBOARD_STR)
            print(f"Race added! ({scoreboard.races} total)")
            print(f"Updated scoreboard saved as '{SCOREBOARD_STR}'")

        # Remove race
        elif option == "remove":
            scoreboard.remove_race()
            scoreboard.save_all(SCOREBOARD_STR)
            print(f"Race removed! ({scoreboard.races} total)")
            print(f"Updated scoreboard saved as '{SCOREBOARD_STR}'")

        # Save
        elif option == "save":
            scoreboard.save_all(SCOREBOARD_STR)
            print(f"Scoreboard saved as '{SCOREBOARD_STR}'")

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

        # Autoclick
        elif option == "click":
            print(f"Starting to click in {TYPE_OFFSET} second(s)! ({MAX_SCORER} times)")
            autoclick()

        # Debug
        elif option == "debug":
            print("Nothing to debug")

        # Toggle test
        elif option == "test":
            TEST_MODE = not TEST_MODE
            print(f"Test mode is now {'ON' if TEST_MODE else 'OFF'}")

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
        self.dnf_marbles: list[int] = []

        with open(filename, "r") as f:
            file_data = json.load(f)
        
        self.data: dict[str, list[dict[str, int]]] = file_data["marbles"]
        self.dnf_marbles = file_data["dnf-marbles"]
        
        self.races = len(self.dnf_marbles)


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
            sorting_key = lambda x: x[0].lower()
        elif option == "last race":
            sorting_key = lambda x: x[1][-1]["individual"]

        # Create a list out of data to be sorted
        listed = list(self.data.items())

        try:
            sorted_list = list(sorted(
                listed,
                key=sorting_key,
                # We only want descending order when sorting by points
                reverse=(option == "points" or option == "last race")   
            ))

        # Username not found when sorting by flair
        except KeyError as e:
            if not TEST_MODE:
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


    def get_filtered_positions(self) -> dict[str, int]:
        """
        Returns a dict containing the current position of each user
        only considering those that are still part of the competition
        """

        sorted_list = list(self.get_sorted_by("points"))

        filtered_dict = {}
        i = 1
        for username in sorted_list:
            try:
                flair = self.competitors[username]
            except KeyError:
                continue
            
            if flair == 0:
                continue

            filtered_dict[username] = i
            i += 1

        return filtered_dict


    def clear_all(self) -> None:
        self.data = {}
        self.dnf_marbles = []
        self.races = 0


    def remove_race(self) -> None:
        """
        Removes the last race data from all users
        """

        # Don't do anything if already at 0
        if self.races == 0:
            return

        self.races -= 1

        self.dnf_marbles.pop()

        # Delete everything if there are no races left
        if self.races == 0:
            self.data = {}
        else:
            for username, user in self.data.items():
                user.pop()


    def add_race(self, filename: str, dnf_marble: int) -> None:
        """
        Reads a file containing the results of the last race and
        updates the competitors' data accordingly
        """

        self.races += 1

        self.dnf_marbles.append(dnf_marble)

        # Read the file
        with open(filename, "r") as f:
            results = [ username.strip() for username in f.readlines() ]

        # Handle each user
        for position, username in enumerate(results):
            score = get_score(position + 1, dnf_marble)

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
            json.dump(
                { "marbles": self.data, "dnf-marbles": self.dnf_marbles },
                f,
                indent=4
            )

    
    def save_xlsx(self, filename: str) -> None:
        """
        Saves the data to a .xlsx file
        """

        workbook = xlsxwriter.Workbook(filename)

        # Auxiliary
        positions = self.get_filtered_positions()
        sheets = ("points", "username", "flair", "last race")
        looper = (
            (f"Sorted by {option}", self.get_sorted_by(option)) for option in sheets
        )

        # Create two copies, one sorted by position and the other by flair
        for worksheet, dataset in looper:
            sheet = workbook.add_worksheet(worksheet)

            # Format presets
            bold = workbook.add_format({
                "bold": True,
                "bg_color": "00FFFF",
                "align": "center",
                "border": 1,
                "align": "center"
            })
            normal = workbook.add_format({
                "pattern": 1,
                "bg_color": "FFFFFF",
                "border": 1,
                "align": "center"
            })
            redded = workbook.add_format({
                "pattern": 1,
                "bg_color": "EA9999",
                "border": 1,
                "align": "center"
            })
            greyed = workbook.add_format({
                "pattern": 1,
                "bg_color": "CCCCCC",
                "border": 1,
                "align": "center"
            })

            # Column widths
            sheet.set_column(1, 1, 25)
            sheet.set_column(2, 3 + TOTAL_RACES, 15)

            # Titles row
            sheet.write(0, 0, "Flair", bold)
            sheet.write(0, 1, "Username", bold)
            sheet.write(0, 2, "Position", bold)
            sheet.write(0, 3, "Total Points", bold)
            for i in range(TOTAL_RACES):
                sheet.write(0, 4 + i, f"Race {i+1}", bold)

            # Loop through users
            row = 1
            for username, user in dataset.items():
                # Try to get flair (there might be a typo)
                try:
                    flair = self.competitors[username]
                except KeyError:
                    # Keep going when test mode is on
                    if TEST_MODE:
                        flair = "-"
                    # Else, don't write anything
                    else:
                        print(f"ERROR: Username not found: '{username}'")
                        print("Not writing any data...")
                        continue

                # Skip people who left
                if flair == 0:
                    continue

                # Flair
                sheet.write(row, 0, flair, normal)

                # Username
                sheet.write(row, 1, username, normal)

                # Position
                position = positions[username]
                sheet.write(row, 2, f"{position}{self.get_end(position)}", normal)

                # Total Points
                sheet.write(row, 3, user[-1]["total"], normal)

                # Loop through race data
                col = 4
                for race in user:
                    # Only write data if participatedd
                    if (pos := race["position"]) != 0:
                        # Check if DNF
                        dnf_marble = self.dnf_marbles[col-4]
                        if dnf_marble > 0 and pos >= dnf_marble:
                            point_text = "DNF"
                            formatting = redded
                        else:
                            point_text = f"{pos}{self.get_end(pos)}"
                            formatting = normal
                        
                        sheet.write(
                            row,
                            col,
                            f"{point_text} (+{race['individual']})",
                            formatting
                        )

                    # Else grey it out
                    else:
                        sheet.write(row, col, "-", greyed)
                    col += 1

                row += 1
                
        workbook.close()

    
    def save_all(self, filename: str) -> None:
        xlsxfilename = filename + ".xlsx"
        jsonfilename = filename + ".json"

        self.save_xlsx(xlsxfilename)
        self.save_json(jsonfilename)


    def get_end(self, number: int) -> str:
        """
        Returns "st" for 1, "nd" for 2, "rd" for 3 and "th" othewise
        """

        last_digit = number % 10

        if last_digit == 1:
            return "st"
        elif last_digit == 2:
            return "nd"
        elif last_digit == 3:
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


    def save_list(self, filename: str, race: int) -> None:
        """
        Saves the list of eligible members to a file
        """

        if race <= RACE_CUTOFF:
            min_weeks = MIN_WEEK
        else:
            min_weeks = MIN_WEEK + (race - RACE_CUTOFF)

        eligible = self.get_elegible(min_weeks)

        with open(filename, "w") as f:
            f.writelines("\n".join(eligible))


def get_score(position: int, dnf_marble: int) -> int:
    """
    Scoring function
    """

    # Did not finish
    if dnf_marble > 0 and position >= dnf_marble:
        return 0

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
        ans.append(str(ith_digit))

    return reversed(ans)


def autotype() -> None:
    """
    Auto types the scores of each position, in descending order
    Auto scrolls while doing so (otherwise, it glitches Marbles On Stream)
    """

    pyautogui.sleep(TYPE_OFFSET)

    for i in range(MAX_SCORER):
        pyautogui.write(get_keystrokes(get_score(i+1)))
        pyautogui.write(["down"])
        pyautogui.scroll(-160)
        

def autoclick() -> None:
    """
    Auto clicks for adding Marbles On Stream scores
    """

    pyautogui.sleep(TYPE_OFFSET)

    for i in range(MAX_SCORER):
        pyautogui.click()


def create_random(filename: str, amount: int):
    """
    Creates and saves a list of nameless marbles
    """

    with open(filename, "w") as f:
        for i in range(amount):
            f.write("Marble " + str(i + 1) + "\n")


def read_int(message: str) -> None:
    """
    Fail-proof read integer from input
    """

    inp = input(message)
    while True:
        try:
            number = int(inp)
            break
        except ValueError:
            inp = input(message)
    
    return number


def print_instructions() -> None:
    """
    Prints menu instructions
    """

    print("Insert one of the following options")
    print("random: Creates a list of nameless marbles to test races")
    print(f"list: Save list of competitors that stayed at least {MIN_WEEK} full week(s)")
    print(f"add: Read from '{RESULTS_STR}' and add race")
    print("remove: Remove a race from the scoreboard")
    print("save: Save all data")
    print("clear: Clear all the data and create backup")
    print("type: Autofill scoring system in Marbles On Stream")
    print("click: Autoclick for the Marbles On Stream configuration")
    print("debug: Execute some debugging code")
    print(f"test: Toggle test mode (currently {'ON' if TEST_MODE else 'OFF'}")
    print("help: Show the menu options")
    print("quit: Exit the program")


if __name__ == "__main__":
    main()
