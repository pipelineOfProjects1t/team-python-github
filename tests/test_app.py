import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import main


class AppTestCase(unittest.TestCase):
    def test_save_and_load_records(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            main.DATA_FILE = Path(temp_dir) / main.DATA_FILE.name
            main.save_records([main.SAMPLE_RECORD])
            self.assertEqual(main.load_records(), [main.SAMPLE_RECORD])

    def test_count_by_field(self):
        records = [dict(main.SAMPLE_RECORD), dict(main.SAMPLE_RECORD)]
        result = main.count_by_field(records, main.GROUP_FIELD)
        key = str(main.SAMPLE_RECORD[main.GROUP_FIELD])
        self.assertEqual(result[key], 2)

    def test_delete_record_by_index(self):
        records = [dict(main.SAMPLE_RECORD)]
        removed = main.delete_record_by_index(records, 1)
        self.assertEqual(removed, main.SAMPLE_RECORD)
        self.assertEqual(records, [])

    def test_numeric_stat_if_project_has_numeric_field(self):
        if main.NUMERIC_FIELD:
            records = [dict(main.SAMPLE_RECORD), dict(main.SAMPLE_RECORD)]
            if main.NUMERIC_MODE == "sum":
                value = main.calculate_sum(records, main.NUMERIC_FIELD)
                self.assertGreater(value, 0)
            else:
                value = main.calculate_average(records, main.NUMERIC_FIELD)
                self.assertGreater(value, 0)


if __name__ == "__main__":
    unittest.main()
