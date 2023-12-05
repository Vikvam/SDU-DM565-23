from props_reader import PropertiesReader

PROPERTIES_FILE = "conf.properties"


def main():
    props_reader = PropertiesReader()
    props = props_reader.load_properties(PROPERTIES_FILE)
    print(props)


if __name__ == '__main__':
    main()
