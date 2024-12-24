import os
import numpy as np
import logging
from datetime import datetime
from tawhiri.wind import Dataset, unpack_grib

directory = "datasets"
ds_time = datetime(2013, 7, 9, 12, 0, 0)

fmtr = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")
handler = logging.StreamHandler() # stderr
handler.setLevel(logging.DEBUG)
handler.setFormatter(fmtr)
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(handler)

logging.info("setup")
gribmirror = Dataset.filename(ds_time, directory=directory, suffix=Dataset.SUFFIX_GRIBMIRROR)
temp = Dataset(ds_time, directory=directory, suffix='.temp', new=True)
actual = Dataset(ds_time, directory=directory)
checklist = Dataset.checklist()

logging.info("unpack")
unpack_grib(gribmirror, temp, checklist)

logging.info("check")
assert np.array_equal(actual.array, temp.array)

logging.info("cleanup")
os.unlink(Dataset.filename(ds_time, directory=directory, suffix='.temp'))
