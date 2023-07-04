NO_OF_CHARACTERS = 256

class Algorithms():
    def badCharacterHeuristic(string, length):
        bad_char = [-1]*NO_OF_CHARACTERS
        
        for i in range(length):
            bad_char[ord(string[i])] = i

        return bad_char

    def search(text, pattern):
        text = text.lower()
        pattern = pattern.lower()
        
        length_of_pattern = len(pattern)
        length_of_text = len(text)

        bad_char_table = Algorithms.badCharacterHeuristic(pattern, length_of_pattern)
        shift = 0

        while (shift <= length_of_text - length_of_pattern):
            current_index = length_of_pattern - 1

            while current_index >= 0 and pattern[current_index] == text[shift + current_index]:
                current_index -= 1

            if current_index < 0:
                print(f"found {pattern}")
                return True
            
            shift += max(1, current_index - bad_char_table[ord(text[shift + current_index])])
        
        return False
    
    def split_keywords(string):
        if not string:
            return []

        no_spaces = string.replace(" ", "")
        list = no_spaces.split(",")

        return list

