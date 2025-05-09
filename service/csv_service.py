import csv
from typing import List, Dict
from pathlib import Path

class CSVService:
    @staticmethod
    def read_csv(file_path: str) -> List[Dict[str, str]]:
        DATA_PATH = Path(__file__).parent.parent / "data"
        file_path = str(DATA_PATH / file_path)
        if not Path(file_path).exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader]

    @staticmethod
    def write_csv(file_path: str, data: List[Dict[str, str]], fieldnames: List[str]):
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
