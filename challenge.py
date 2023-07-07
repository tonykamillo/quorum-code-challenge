import csv, os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DS_DIR = os.path.join(BASE_DIR, "data")
DS_INPUT_DIR = os.path.join(DS_DIR, "input")
DS_OUTPUT_DIR = os.path.join(DS_DIR, "output")


def load_csv(filename):
    """Load csv file from data/input/ folder"""
    items = []
    with open(os.path.join(DS_INPUT_DIR, filename), newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        items = [row for row in reader]
    return items
