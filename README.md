# Bincom Python Basic Developer Test

## Files

- `main.py` - Python solution for the assessment.
- `python_class_test.html` - HTML dataset supplied in the assessment.
- `requirements.txt` - Python dependencies (PostgreSQL driver and `.env` loader).
- `.env.example` - Example PostgreSQL connection settings.
- `database.sql` - PostgreSQL table definition.
- `.gitignore` - Prevents secrets and generated files from being committed.

## Python version

Python 3.8+ is recommended.

## Install dependencies

```bash
python -m pip install -r requirements.txt
```

## PostgreSQL setup

Create a PostgreSQL database, for example:

```sql
CREATE DATABASE bincom;
```

Copy `.env.example` to `.env` and fill in your connection details. The program loads `.env` automatically, creates the `color_frequencies` table if needed, and inserts or updates each color's frequency (running it again does not create duplicates).

Do not commit a real `.env` file or database password.

## Run

```bash
python main.py
```

The program reads the colors directly from `python_class_test.html`.

## Notes on the statistical questions

Color names are categorical values. Therefore, a mathematical mean, median, and variance are not intrinsically defined for the color labels themselves.

For the purpose of the assessment:

1. Mean: the program reports the mean frequency of the distinct colors and explains why a mean color itself is not mathematically defined.
2. Most worn color: based directly on frequency.
3. Median: the program uses alphabetical ordering as an explicit assumption and returns the middle color.
4. Variance: population variance of the distinct color frequencies.
5. Probability of red: RED observations divided by all observations.

The source data contains `BLEW` and `ARSH`. They are preserved exactly rather than silently correcting or deleting source data. `BLEW` appears to be a likely typo for `BLUE`, but changing source data without documentation would alter the analysis.

## Additional binary sequence question

The supplied page contains an additional sequence question. The implementation marks the third character of every `111` sequence as `1`, matching the provided sample interpretation.

## Expected key results from the supplied data

- Total observations: 95
- BLUE: 30
- WHITE: 16
- GREEN: 10
- ORANGE: 9
- RED: 9
- Mean frequency: 7.92
- Population variance of frequency counts: 63.24
- Probability of RED: 9/95 = 9.47%
- Sum of first 50 Fibonacci numbers (starting at 0): 20,365,011,073
