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


def dump_csv(filename, data):
    """Creates csv file into data/output/ folder"""
    with open(os.path.join(DS_OUTPUT_DIR, filename), "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        for item in data:
            writer.writerow(item)


def main():
    # Loading csv datasets
    bills = load_csv("bills.csv")
    legislators = load_csv("legislators.csv")
    vote_results = load_csv("vote_results.csv")
    votes = load_csv("votes.csv")

    vote2bill = {bill_vote["id"]: bill_vote["bill_id"] for bill_vote in votes}

    print(bills)
    print(legislators)
    print(vote_results)
    print(votes)
    print(vote2bill)


if __name__ == "__main__":
    main()
