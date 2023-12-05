class PropertiesReader:
    def load_properties(self, file_path, separator='='):
        props = {}

        with open(file_path, "rt") as file:
            for line in file:
                line = line.strip()

                key_value = line.split(separator)
                key = key_value[0].strip()
                value = separator.join(key_value[1:]).strip().strip('"')
                props[key] = value

        return props
