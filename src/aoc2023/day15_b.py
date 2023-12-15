import click

def elfhash(st):
    value = 0
    for c in list(st):
        value += ord(c)
        value *= 17
        value %= 256
    return value

def remove_lens(box, label):
    for i, st in enumerate(box):
        if st.startswith(label):
            del box[i]
            return box

def update_lens(box, label, value):
    for i, st in enumerate(box):
        if st.startswith(label):
            box[i] = f"{label}={value}"
            return box
    box.append(f"{label}={value}")
    return box

def get_label(st):
    if st.find('=') != -1:
        return st.split('=')[0].strip()
    elif st.find('-') != -1:
        return st.split('-')[0].strip()
    else:
        raise RuntimeError("Invalid input!")

def hashmap(boxes, st):
    box_nr = elfhash(get_label(st))
    if st.find('=') != -1:
        label, value = st.split('=')
        label = label.strip()
        value = value.strip()
        update_lens(boxes[box_nr], label, value)
    elif st.find('-') != -1:
        remove_lens(boxes[box_nr], st.split('-')[0].strip())
    else:
        raise RuntimeError("Invalid input!")

def print_boxes(boxes):
    for i, box in enumerate(boxes):
        if len(box) > 0:
            print(i, box)

def evaluate_boxes(boxes):
    result = 0
    for i, box in enumerate(boxes):
        for j, st in enumerate(box):
            value = (i + 1) * (j + 1) * int(st.split('=')[1])
            result += value
            print(value)
    return result

@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    boxes = [[] for _ in range(256)]
    with open(input_file, 'r') as fd:
        line = fd.read()
        puzzle_input = [x.strip() for x in line.split(',')]
    for st in puzzle_input:
        print(st)
        hashmap(boxes, st)
        print_boxes(boxes)
    print(evaluate_boxes(boxes))

if __name__ == '__main__':
    main()
