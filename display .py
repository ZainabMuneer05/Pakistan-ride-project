def display_cities(cities):
    print("\n" + "="*80)
    print("AVAILABLE CITIES")
    print("="*80)
    for i in range(0, len(cities), 4):
        row = cities[i:i+4]
        print("".join("{:<18}".format(c) for c in row))