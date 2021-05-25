from lib import scrap_by_keyword
from datetime import date


def main():
    scrap_by_keyword('公主', date.today())


if __name__ == "__main__":
    main()
