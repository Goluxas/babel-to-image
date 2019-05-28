with open('book.txt', 'r') as infile, open('flat.txt', 'w') as outfile:
    text = ''
    for line in infile:
        text += line.replace('\n', '')

    print >>outfile, text
