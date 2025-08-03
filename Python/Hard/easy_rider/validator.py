import itertools
import operator

from datetime import datetime
from collections import defaultdict

from stop import Stop


class Validator:
    stops = []
    data_errors = defaultdict(int)
    format_errors = defaultdict(int)
    STOP_TYPES = {
        'S': 'Start',
        'T': 'Transfer',
        'F': 'Finish'
    }

    def __init__(self, data):
        for payload in data:
            try:
                stop = Stop.from_dict(payload)
            except Stop.InvalidData as ex:
                self.data_errors[ex.field] += 1
            except Stop.InvalidFormat as ex:
                self.format_errors[ex.field] += 1
            else:
                self.stops.append(stop)

    def list_by_field(self, field) -> dict:
        key = operator.attrgetter(field)
        return {k: list(g) for k, g in itertools.groupby(
                sorted(self.stops, key=key), key=key)}

    @property
    def lines(self) -> dict:
        return self.list_by_field('bus_id')

    @property
    def types(self) -> dict:
        return self.list_by_field('stop_type')

    @property
    def names(self) -> dict:
        return self.list_by_field('stop_name')

    @property
    def lines_types(self) -> dict:
        return {k: [stop.stop_type for stop in v]
            for k, v in self.lines.items()}

    @property
    def lines_arrivals(self) -> dict:
        return {k: [(stop.arr_time, stop.stop_name) for stop in v]
            for k, v in self.lines.items()}

    @property
    def types_names(self) -> dict:
        tmp = {k: {stop.stop_name for stop in v}
            for k, v in self.types.items()}
        tmp['T'] = {stop_name
            for stop_name, stops in self.names.items() if len(stops) > 1}
        return tmp

    def validate_lines(self):
        print('Line names and number of stops:')
        for line, stops in self.lines_types.items():
            if not ("S" in stops and "F" in stops):
                print("There is no start or end stop for the line", line)
                break
            else:
                print('bus_id:', line, 'stops:', len(stops))

    def validate_stops(self):
        stops_by_type = self.types_names
        for sign, type_name in self.STOP_TYPES.items():
            names = sorted(list(stops_by_type[sign]))
            print(f"{type_name} stops: {len(names)} {names}")

    def validate_on_demand(self):
        print('On demand stops test:')
        stops_by_type = self.types_names
        on_demand_errors = set()
        for sign, type_name in self.STOP_TYPES.items():
            on_demand_errors.update(
                stops_by_type['O'].intersection(stops_by_type[sign]))
        if on_demand_errors:
            print(f'Wrong stop type: {sorted(list(on_demand_errors))}')
        else:
            print('OK')

    def validate_arrivals(self):
        print('Arrival time test:')
        for line, arrivals in self.lines_arrivals.items():
            last_stop_time = datetime.strptime("00:00", "%H:%M")
            for time, name in arrivals:
                if last_stop_time > time:
                    print(f'bus_id line {line}: wrong time on station {name}')
                    break
                else:
                    last_stop_time = time
        else:
            print('OK')

    def run(self):
        print('Type and required field validation:',
              sum(self.data_errors.values()))
        for field, value in self.data_errors.items():
            print(field, value, sep=": ")
        print('Format validation:',
              sum(self.format_errors.values()), 'errors')
        for field, value in self.format_errors.items():
            print(field, value, sep=": ")
        self.validate_lines()
        self.validate_stops()
        self.validate_arrivals()
        self.validate_on_demand()
