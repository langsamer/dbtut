import calendar
from csv import reader
from pathlib import Path
import random
from datetime import date, timedelta

schulfaecher = [
    "Mathematik",
    "Physik",
    "Chemie",
    "Biologie",
    "Erdkunde",
    "Sozialkunde",
    "Geschichte",
    "Deutsch",
    "Englisch",
    "Französisch",
    "Latein",
    "Spanisch",
    "Sport",
    "Musik",
    "Religion",
    "Kunst",
]


def read_names(csvpath: str | Path) -> dict:
    names = {"m": [], "f": []}
    with open(csvpath) as csvfile:
        r = reader(csvfile)
        for gender, name in r:
            names[gender].append(name)
    return names


def name_pool(names):
    for name in names:
        yield name


def generate_age(minimum: int = 6, maximum: int = 10) -> int:
    return random.randint(minimum, maximum)


def days_in_year(year: int = date.today().year) -> int:
    return 365 + calendar.isleap(year)


def generate_birthday(age: int) -> date:
    today = date.today()
    minimum_bday = today.replace(year=today.year - age - 1) + timedelta(days=1)
    maximum_bday = today.replace(year=today.year - age)
    bday = date.fromordinal(
        random.randint(minimum_bday.toordinal(), maximum_bday.toordinal())
    )
    return bday


def grade2age(grade: int) -> int:
    """Alter für eine Klassenstufe.

    Annahme: Regeleinschulung mit 6 Jahren.
    Um etwas Varianz zuzulassen, kann auch +-1 Jahr hinzugezählt werden."""
    return grade + 5


class PersonenGenerator:
    def __init__(self, all_names):
        self.names_f = name_pool(all_names["f"])
        self.names_m = name_pool(all_names["m"])

    def random_person(self, is_student=True) -> dict:
        gender = random.choice(("m", "f"))
        if gender == "f":
            name = next(self.names_f)
        else:
            name = next(self.names_m)
        if is_student:
            age = grade2age(random.randint(1, 4))
        else:
            age = random.randint(25, 60)
        birthday = generate_birthday(age)

        return {"gender": gender, "birthday": birthday, "name": name}


if __name__ == "__main__":
    names = read_names("names.csv")

    # for name in names["boy"]:
    #     age = generate_age()
    #     bday = generate_birthday(age)
    #     print(f"{name} is {age} years old, he was born on {bday:%Y-%m-%d}")

    # d1 = date(1967, 5, 5)
    # d2 = date.today()
    # td = d2 - d1
    # print(f"{td=}")

    pg = PersonenGenerator(all_names=read_names("names.csv"))
    for i in range(100):
        is_student = random.choice([True, False])
        print(f"{i}: {pg.random_person(is_student)} {is_student=}")
