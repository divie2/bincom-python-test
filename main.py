import os
import re
import random
import statistics
from collections import Counter

try:
    import psycopg2
except ImportError:
    psycopg2 = None

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


HTML_FILE = "python_class_test.html"


def extract_colors(filename):
    """Extract all colors from the HTML table."""
    with open(filename, "r", encoding="utf-8") as file:
        html = file.read()

    table_cells = re.findall(
        r"<td>([^<]+)</td>",
        html,
        flags=re.IGNORECASE
    )

    colors = []

    # Each table row contains DAY followed by COLOURS.
    for index in range(1, len(table_cells), 2):
        color_text = table_cells[index]
        day_colors = [
            color.strip().upper()
            for color in color_text.split(",")
        ]
        colors.extend(day_colors)

    return colors


def get_color_frequencies(colors):
    return Counter(colors)


def get_most_common_color(color_counts):
    return color_counts.most_common(1)[0]


def get_mean_frequency(color_counts):
    """Mean of the frequencies of the distinct colors."""
    frequencies = list(color_counts.values())
    return statistics.mean(frequencies)


def get_median_color(colors):
    """
    Color is categorical data, so a mathematical median is not
    intrinsically defined. For this assessment, return the middle
    item after alphabetical sorting, and document the assumption.
    """
    sorted_colors = sorted(colors)
    return sorted_colors[len(sorted_colors) // 2]


def get_frequency_variance(color_counts):
    """Population variance of the distinct color frequencies."""
    frequencies = list(color_counts.values())
    return statistics.pvariance(frequencies)


def get_red_probability(colors):
    if not colors:
        return 0.0
    return colors.count("RED") / len(colors)


def save_to_postgresql(color_counts):
    """
    Save frequencies to PostgreSQL.

    Connection details are read from environment variables (or a .env file):
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD.
    """
    if psycopg2 is None:
        print("PostgreSQL skipped: install dependencies first.")
        return

    required = ["DB_NAME", "DB_USER", "DB_PASSWORD"]
    missing = [name for name in required if not os.getenv(name)]

    if missing:
        print(
            "PostgreSQL skipped. Missing environment variables: "
            + ", ".join(missing)
        )
        return

    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
    except psycopg2.Error as error:
        print("PostgreSQL skipped. Could not connect to the database:")
        print(str(error).strip())
        return

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS color_frequencies (
                        id SERIAL PRIMARY KEY,
                        color VARCHAR(50) UNIQUE NOT NULL,
                        frequency INTEGER NOT NULL
                    )
                """)

                for color, frequency in color_counts.items():
                    cursor.execute("""
                        INSERT INTO color_frequencies (color, frequency)
                        VALUES (%s, %s)
                        ON CONFLICT (color)
                        DO UPDATE SET frequency = EXCLUDED.frequency
                    """, (color, frequency))
    finally:
        connection.close()

    print(f"Saved {len(color_counts)} colors to the color_frequencies table.")


def recursive_search(numbers, target, index=0):
    """Recursively search for target and return its index, or -1."""
    if index >= len(numbers):
        return -1

    if numbers[index] == target:
        return index

    return recursive_search(numbers, target, index + 1)


def generate_binary_number():
    """Generate a random 4-digit binary number and convert it to base 10."""
    binary_number = "".join(random.choice("01") for _ in range(4))
    decimal_number = int(binary_number, 2)
    return binary_number, decimal_number


def fibonacci_sum(n):
    """Return the sum of the first n Fibonacci numbers (starting at 0)."""
    first, second = 0, 1
    total = 0

    for _ in range(n):
        total += first
        first, second = second, first + second

    return total


def three_ones_output(binary_string):
    """
    Mark the third 1 whenever three consecutive 1s are found.

    This interpretation matches the sample output:
    each position that completes a '111' sequence is marked as 1.
    """
    result = ["0"] * len(binary_string)

    for i in range(len(binary_string) - 2):
        if binary_string[i:i + 3] == "111":
            result[i + 2] = "1"

    return "".join(result)


def display_results(colors, color_counts):
    print("\n" + "=" * 55)
    print("BINCOM PYTHON BASIC DEVELOPER TEST")
    print("=" * 55)

    print(f"\nTotal color observations: {len(colors)}")
    print(f"Distinct colors: {len(color_counts)}")

    print("\nCOLOR FREQUENCIES")
    print("-" * 30)

    for color, frequency in color_counts.most_common():
        print(f"{color:<10} {frequency}")

    print("\n1. MEAN COLOR")
    print(
        "Mean is not directly applicable to categorical color data."
    )
    print(
        f"Mean frequency of distinct colors: "
        f"{get_mean_frequency(color_counts):.2f}"
    )

    most_common_color, frequency = get_most_common_color(color_counts)

    print("\n2. MOST WORN COLOR")
    print(f"{most_common_color}: {frequency} times")

    print("\n3. MEDIAN COLOR")
    print(
        "Using alphabetical ordering as the required categorical "
        f"ordering assumption: {get_median_color(colors)}"
    )

    print("\n4. VARIANCE")
    print(
        "Population variance of the distinct color frequencies: "
        f"{get_frequency_variance(color_counts):.2f}"
    )

    red_probability = get_red_probability(colors)

    print("\n5. PROBABILITY OF RED")
    print(f"{red_probability:.4f}")
    print(f"{red_probability * 100:.2f}%")

    print("\n7. RECURSIVE SEARCH")
    numbers = [2, 5, 8, 12, 17, 21, 30]
    print(f"Example list: {numbers}")

    user_input = input("Enter a number to search for: ").strip()

    try:
        target = int(user_input)
        result = recursive_search(numbers, target)

        if result == -1:
            print("Number not found.")
        else:
            print(f"Number found at index {result}.")
    except ValueError:
        print("Invalid input. Please enter a whole number.")

    print("\n8. RANDOM 4-DIGIT BINARY NUMBER")
    binary_number, decimal_number = generate_binary_number()
    print(f"Binary: {binary_number}")
    print(f"Base 10: {decimal_number}")

    print("\n9. SUM OF FIRST 50 FIBONACCI NUMBERS")
    print(fibonacci_sum(50))

    print("\nADDITIONAL BINARY SEQUENCE QUESTION")
    sample_input = "0101101011101011011101101000111"
    sample_output = three_ones_output(sample_input)
    print(f"Input:  {sample_input}")
    print(f"Output: {sample_output}")


def main():
    if load_dotenv is not None:
        load_dotenv()

    if not os.path.exists(HTML_FILE):
        raise FileNotFoundError(
            f"Could not find '{HTML_FILE}'. "
            "Make sure the HTML file is in the same directory."
        )

    colors = extract_colors(HTML_FILE)
    color_counts = get_color_frequencies(colors)

    display_results(colors, color_counts)

    print("\n6. SAVE COLORS AND FREQUENCIES TO POSTGRESQL")
    save_to_postgresql(color_counts)


if __name__ == "__main__":
    main()
