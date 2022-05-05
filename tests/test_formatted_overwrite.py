import io

import numpy as np
import pytest

from ecl_data_io._formatted.read import FormattedEclArray
import ecl_data_io._formatted.write as ecl_formatted_write


def test_overwrite_entries():
    data = {
        "KEYWORD1": np.array([1, 2, 3, 4, 5, 6]),
        "KEYWORD2": np.array([1.0, 2.0, 3.0]),
        "KEYWORD3": np.array(["test1   ", "test2   ", "test3   "])
    }
    buf = io.StringIO()
    ecl_formatted_write.formatted_write(buf, data)
    buf.seek(0)
    out_records = list(FormattedEclArray.parse(buf))

    edit_index = 1
    ecl_array_to_edit = out_records[edit_index]
    new_values = np.array([0.0, 0.0, 0.0])
    edited_data = [(ecl_array_to_edit.read_keyword(), new_values, ecl_array_to_edit.start)]

    ecl_formatted_write.formatted_overwrite(buf, edited_data)
    buf.seek(0)
    changed_out_records = list(FormattedEclArray.parse(buf))
    assert np.array_equal(changed_out_records[edit_index].read_array(), new_values)
