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


def count_votes(legislators, bills, vote_results, vote2bill):
    """Process vote results"""
    for vote in vote_results:
        _, legislator_id, vote_id, vote_type = vote.values()
        legislator = legislators[legislator_id]
        bill = bills[vote2bill[vote_id]]

        if "primary_sponsor" not in bill:
            bill["primary_sponsor"] = legislators.get(bill["sponsor_id"], {}).get(
                "name", "Unknown"
            )
            bill.pop("sponsor_id")

        if int(vote_type) == 1:
            legislator["num_supported_bills"] += 1
            bill["supporter_count"] = bill.get("supporter_count", 0) + 1

        elif int(vote_type) == 2:
            legislator["num_opposed_bills"] += 1
            bill["opposer_count"] = bill.get("opposer_count", 0) + 1

    return legislators.values(), bills.values()


def add_legislator_fields(leg):
    """Adds accounting fields for legislator in order to avoid empty values for both num_supported_bills and num_opposed_bills fields"""
    leg["num_supported_bills"] = 0
    leg["num_opposed_bills"] = 0

    return leg


def main():
    # Loading csv datasets
    bills = load_csv("bills.csv")
    legislators = load_csv("legislators.csv")
    vote_results = load_csv("vote_results.csv")
    votes = load_csv("votes.csv")

    # Transforming some datasets into dictionary to constant time O(1) access.
    # It gonna allows to make only one iteration over vote_results making the account in linear time O(n)
    vote2bill = {bill_vote["id"]: bill_vote["bill_id"] for bill_vote in votes}
    legislators_dict = {leg["id"]: add_legislator_fields(leg) for leg in legislators}
    bills_dict = {bill["id"]: bill for bill in bills}

    # Accounting votes for both legislators and bills
    legislator_results, bill_results = count_votes(
        legislators_dict, bills_dict, vote_results, vote2bill
    )

    # Saving accounts files
    dump_csv("legislators-support-oppose-count.csv", list(legislator_results))
    dump_csv("bills.csv", list(bill_results))


if __name__ == "__main__":
    main()
