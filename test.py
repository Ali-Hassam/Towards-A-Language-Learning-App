goethe_file_a2 = "goethe_a2_words.txt"
    
def read(file_name):
    with open(file_name, mode="r", encoding="utf-8") as file:
        return file.readlines()

goethe_a2_file = read(goethe_file_a2)
goethe_a2_list = []
for line in goethe_a2_file:
    parts = line.strip().split('; ')
    word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in parts}
    goethe_a2_list.append(word_dict)
print(len(goethe_a2_file))
