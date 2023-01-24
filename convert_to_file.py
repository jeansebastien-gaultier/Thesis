def new_file(place, name, text: str):
    new_file = open(f'{place}/{name}.txt', 'x')
    new_file.write(text)
    new_file.close