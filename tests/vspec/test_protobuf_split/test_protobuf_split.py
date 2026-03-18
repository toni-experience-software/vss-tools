# Copyright (c) 2024 Contributors to COVESA
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License 2.0 which is available at
# https://www.mozilla.org/en-US/MPL/2.0/
#
# SPDX-License-Identifier: MPL-2.0

import filecmp
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEST_UNITS = HERE / ".." / "test_units.yaml"
TEST_QUANT = HERE / ".." / "test_quantities.yaml"


def test_protobuf_split_with_enums(tmp_path):
    """
    Test that --split --generate-enums produces one .proto file per branch
    with package-scoped short enum names.
    """
    vspec = HERE / "test.vspec"
    out_dir = tmp_path / "split_out"
    cmd = (
        f"vspec export protobuf -u {TEST_UNITS} -q {TEST_QUANT} "
        f"--vspec {vspec} --output {out_dir} --split --generate-enums"
    )
    subprocess.run(cmd.split(), check=True)

    expected_dir = HERE / "expected_split"
    for expected_file in expected_dir.iterdir():
        actual_file = out_dir / expected_file.name
        assert actual_file.exists(), f"Missing output file: {expected_file.name}"
        assert filecmp.cmp(actual_file, expected_file), (
            f"{expected_file.name} differs.\n"
            f"Got:\n{actual_file.read_text()}\n"
            f"Expected:\n{expected_file.read_text()}"
        )

    # Verify no extra files
    actual_files = sorted(f.name for f in out_dir.iterdir())
    expected_files = sorted(f.name for f in expected_dir.iterdir())
    assert actual_files == expected_files, (
        f"File sets differ.\nGot: {actual_files}\nExpected: {expected_files}"
    )
