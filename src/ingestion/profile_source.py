from pathlib import Path
import pandas as pd


RAW_DATA_PATH = Path("data/raw")


def profile_csv(file_path):
    print("\n" + "=" * 80)
    print(f"FILE: {file_path.name}")
    print("=" * 80)

    df = pd.read_csv(file_path)

    print(f"Rows       : {len(df):,}")
    print(f"Columns    : {len(df.columns)}")
    print(f"Duplicates : {df.duplicated().sum():,}")

    print("\nCOLUMN PROFILE")
    print("-" * 80)

    profile = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "null_count": df.isnull().sum(),
        "null_pct": (df.isnull().mean() * 100).round(2),
        "unique_count": df.nunique()
    })

    print(profile.to_string())


def main():
    csv_files = sorted(RAW_DATA_PATH.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in {RAW_DATA_PATH}"
        )

    print(f"Found {len(csv_files)} source files.")

    for file_path in csv_files:
        profile_csv(file_path)


if __name__ == "__main__":
    main()
