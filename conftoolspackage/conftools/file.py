import csv


def load(path):
    """
    Load a csv file onto a two dimensional array
    """
    ans = []
    with open(path, "r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            ans.append(row)

    return ans


def save(path, array, utf=False):
    """
    Save a two dimensional array onto a csv file
    """
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        for row in array:
            writer.writerow(row)
