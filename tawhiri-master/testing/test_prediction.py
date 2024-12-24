import sys
from os.path import abspath, split, join
sys.path.append(join(split(abspath(__file__))[0], '..'))

from datetime import datetime
import json
import calendar

from tawhiri import solver, models, kml
from tawhiri.dataset import Dataset as WindDataset
from tawhiri.warnings import WarningCounts
from ruaumoko import Dataset as ElevationDataset

lat0 = 52.5563
lng0 = 360 - 3.1970
alt0 = 100.0
t0 = calendar.timegm(datetime(2016, 11, 28, 15).timetuple())

wind = WindDataset.open_latest()
elevation = ElevationDataset()
warningcounts = WarningCounts()

stages = models.standard_profile(5.0, 30000, 5.0, wind, elevation, warningcounts)
rise, fall = solver.solve(t0, lat0, lng0, alt0, stages)

assert rise[-1] == fall[0]

with open("test_prediction_data.js", "w") as f:
    f.write("var data = ")
    json.dump([(lat, lon) for _, lat, lon, _ in rise + fall], f, indent=4)
    f.write(";\n")

markers = [
    {'name': 'launch', 'description': 'TODO', 'point': rise[0]},
    {'name': 'landing', 'description': 'TODO', 'point': fall[-1]},
    {'name': 'burst', 'description': 'TODO', 'point': fall[0]}
]

print("Warnings:", str(warningcounts.to_dict()))

kml.kml([rise, fall], markers, 'test_prediction.kml')
