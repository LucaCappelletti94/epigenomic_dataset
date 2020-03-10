import os
from epigenomic_dataset import build, mine, concatenate
import shutil
import pandas as pd


def run_me_twice(tmp, clear_download):
    cell_lines = ["GM12892"]
    build(
        bed_path="{}/test.bed".format(
            os.path.dirname(os.path.abspath(__file__))),
        cell_lines=cell_lines,
        epigenomes_path=tmp,
        targets_path=tmp,
        clear_download=clear_download
    )
    files = [
        candidate
        for candidate in os.listdir(tmp)
        if tmp.endswith(".bed")
    ]
    for bed in files:
        pd.testing.assert_frame_equal(
            pd.read_csv("{tmp}/{bed}".format(tmp=tmp, bed=bed), sep="\t"),
            pd.read_csv("{pwd}/expected/{bed}".format(
                pwd=os.path.dirname(os.path.abspath(__file__)),
                bed=bed
            ), sep="\t")
        )
    mine(tmp, {"max":True})
    concatenate(tmp, cell_lines, 1)


def test_build():
    tmp = "{}/epigenomes".format(os.path.dirname(os.path.abspath(__file__)))
    run_me_twice(tmp, False)
    run_me_twice(tmp, True)
    shutil.rmtree(tmp)
