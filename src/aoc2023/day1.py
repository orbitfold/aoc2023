import click

def parse(inputs):
    result = []
    for line in inputs:
        for c in line:
            if c.isdigit():
                a = int(c)
                break
        for c in line[::-1]:
            if c.isdigit():
                b = int(c)
                break
        result.append(a * 10 + b)
    return result

if __name__ == '__main__':
    pass
