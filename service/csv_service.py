import csv
import random
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

    @staticmethod
    def async_read_csv(file_path: str) -> List[Dict[str, str]]:
        return CSVService.read_csv(file_path)

    @staticmethod
    def search_terms(file_path: str) -> List[str]:
        """Synchronous version of async_search_terms for use in pytest parametrize"""
        search_data = CSVService.read_csv(file_path)
        return [row['search_term'].strip() for row in search_data if row.get('search_term', '').strip()]

    @staticmethod
    def get_random_search_term(file_path: str) -> str:
        """Get a random search term from the CSV file"""
        search_data = CSVService.read_csv(file_path)
        return random.choice(search_data)['search_term'].strip()
