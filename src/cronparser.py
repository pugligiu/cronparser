class CronParser:

    _name_months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    _name_weekdays = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    _special_chars = ["*", ",", "-", "/"]
    # keep key COMMAND at the end and add more values after DAY OF WEEK
    _keys = ["MINUTE", "HOUR", "DAY OF MONTH", "MONTH", "DAY OF WEEK", "COMMAND"]

    def __init__(self, cron_string):
        cron_string = cron_string.split()

        if len(cron_string) != len(self._keys):
            raise ValueError("The input has to have all the fields")

        self._data = dict()
        for key, value in zip(self._keys, cron_string):
            if key != "COMMAND":
                value.upper()
                for c in value:
                    if c in self._special_chars:
                        continue
                    if ord(c) >= ord('A') and ord(c) <= ord('Z'):
                        continue
                    if ord(c) >= ord('0') and ord(c) <= ord('9'):
                        continue
                    raise ValueError("The permitted special chars are " + str(self._special_chars))

            self._data[key] = value

    def _sub_names(self, value, names):
        '''
        Convert value in the correspective index of list
        '''
        for i in range(len(names)):
            if value == names[i]:
                return i
        raise ValueError("the value has a string not known")

    def _check_values(self, values, limit_inf, limit_sup):
        '''
        Guarantee the values are coherent and from a specific set
        '''

        # loop status machine to guarantee the coherence in the values
        # 0 -> init , 1->name of months , 2->name of weekdays , 3->numbers
        status = 0

        if values[0] == "":
            raise ValueError("the value has to be integer or correct string name")

        if ord(values[0][0]) >= ord('0') and ord(values[0][0]) <= ord('9'):
            status = 3
        elif values[0] in self._name_months and limit_sup == 12:
            status = 1
        elif values[0] in self._name_weekdays and limit_sup == 6:
            status = 2

        if status == 0:
            raise ValueError("not valid value")

        for i in range(len(values)):
            if values[i] == "":
                raise ValueError("the value has to be integer or correct string name")
            if status == 1:
                values[i] = self._sub_names(values[i], self._name_months)
                values[i] += 1  # encrease of 1 because index starts from 0
            if status == 2:
                values[i] = self._sub_names(values[i], self._name_weekdays)

            try:
                values[i] = int(values[i])
            except ValueError:
                import sys
                raise ValueError("the value has to be integer or correct string name")

        if values[i] < limit_inf or values[i] > limit_sup:
            raise ValueError("the value has to be in the interval [" + str(limit_inf) + ", " + str(limit_sup) + "]")

    def _parse_interval(self, interval, limit_inf, limit_sup):
        '''
        Parse intervals like 1-5 or FEB-APR or FRI-SUN
        '''
        values = interval.split("-")

        if len(values) != 2:
            raise RuntimeError

        self._check_values(values, limit_inf, limit_sup)
        if values[0] >= values[1]:
            raise ValueError("the second value in the interval has to be bigger than first one")

        return list(range(values[0], values[1] + 1))

    def _parse_list(self, comma_list, limit_inf, limit_sup):
        '''
        Parse list like 5 or 1,5,6 or FEB,APR,JUN or FRI,SUN
        '''
        values = comma_list.split(",")

        if len(values) > limit_sup + 1 - limit_inf or len(values) <= 0:
            raise RuntimeError

        for v in values:
            for i in range(len(v)):
                if v[i] in self._special_chars:
                    raise RuntimeError

        self._check_values(values, limit_inf, limit_sup)

        values.sort()
        return values

    def _parse_repetition(self, repetition, limit_inf, limit_sup):
        '''
        Parse expression 1/3 or */2 or JAN/2 or THU/2
        '''
        values = repetition.split("/")

        if len(values) != 2:
            raise RuntimeError

        if values[0] == "*":
            values[0] = limit_inf
            new_values = [values[1]]
            self._check_values(new_values, limit_inf, limit_sup)
            values[1] = new_values[0]
        else:
            new_values = [values[0]]
            self._check_values(new_values, limit_inf, limit_sup)
            values[0] = new_values[0]
            new_values = [values[1]]
            self._check_values(new_values, limit_inf, limit_sup)
            values[1] = new_values[0]

        return list(range(values[0], limit_sup + 1, values[1]))

    def _parse_star(self, star, limit_inf, limit_sup):
        '''
        Parse single star expression like *
        '''
        if star == "*":
            return list(range(limit_inf, limit_sup + 1))
        else:
            raise RuntimeError

    def _parser(self, key, limit_inf, limit_sup):
        '''
        Find out which parser going to apply
        '''
        value = self._data[key]
        count_exceptions = 0
        parsed = []

        try:
            parsed = self._parse_interval(value, limit_inf, limit_sup)
        except RuntimeError:
            count_exceptions += 1

        if count_exceptions == 1:
            try:
                parsed = self._parse_repetition(value, limit_inf, limit_sup)
            except RuntimeError:
                count_exceptions += 1

        if count_exceptions == 2:
            try:
                parsed = self._parse_star(value, limit_inf, limit_sup)
            except RuntimeError:
                count_exceptions += 1

        if count_exceptions == 3:
            try:
                # parse list has to be the last one because matches easier than others
                parsed = self._parse_list(value, limit_inf, limit_sup)
            except RuntimeError:
                count_exceptions += 1

        if count_exceptions == 4:
            if key == "DAY OF WEEK":
                raise ValueError("the value has to be like: 1/2 or * or MON,TUE or 1 or 3-5")
            if key == "DAY OF MONTH":
                raise ValueError("the value has to be like: 1/2 or * or JAN,MAR or 1 or 3-5")
            else:
                raise ValueError("the value has to be like: 1/2 or * or 2,3 or 1 or 3-5")
        else:
            return parsed

    def _get_field(self, key, limit_inf, limit_sup):
        try:
            return(key, self._parser(key, limit_inf, limit_sup))
        except ValueError as e:
            import sys
            raise ValueError("Error in " + key.lower() + " field: " + str(e)) from e

    def get_minutes(self):
        '''
        Get the value representation of the minutes
        '''
        key = self._keys[0]
        limit_sup = 59
        limit_inf = 0
        return self._get_field(key, limit_inf, limit_sup)

    def get_hours(self):
        '''
        Get the value representation of the hours
        '''
        key = self._keys[1]
        limit_sup = 23
        limit_inf = 0
        return self._get_field(key, limit_inf, limit_sup)

    def get_month_days(self):
        '''
        Get the value representation of the month days
        '''
        key = self._keys[2]
        limit_sup = 31
        limit_inf = 1
        return self._get_field(key, limit_inf, limit_sup)

    def get_months(self):
        '''
        Get the value representation of the months
        '''
        key = self._keys[3]
        limit_sup = 12
        limit_inf = 1
        return self._get_field(key, limit_inf, limit_sup)

    def get_week_days(self):
        '''
        Get the value representation of the week days
        '''
        key = self._keys[4]
        limit_sup = 6
        limit_inf = 0
        return self._get_field(key, limit_inf, limit_sup)

    def get_command(self):
        key = self._keys[-1]
        return (key, self._data[key])

    def print_cron_table(self):
        (key, value) = self.get_minutes()
        print('{:<13s} {:<0s}'.format(key.lower(), " ".join(map(str, value))))

        (key, value) = self.get_hours()
        print('{:<13s} {:<0s}'.format(key.lower(), " ".join(map(str, value))))

        (key, value) = self.get_month_days()
        print('{:<13s} {:<0s}'.format(key.lower(), " ".join(map(str, value))))

        (key, value) = self.get_months()
        print('{:<13s} {:<0s}'.format(key.lower(), " ".join(map(str, value))))

        (key, value) = self.get_week_days()
        print('{:<13s} {:<0s}'.format(key.lower(), " ".join(map(str, value))))

        (key, value) = self.get_command()
        print('{:<13s} {:<0s}'.format(key.lower(), value))
