NUMBER_OF_CHARACTERS = 256

class Algorithms():
    def bad_table_init(pattern, length_of_pattern):
        bad_char_table = [length_of_pattern] * NUMBER_OF_CHARACTERS

        for i in range(length_of_pattern):
            value = length_of_pattern - i - 1
            if value == 0:
                value = length_of_pattern
            bad_char_table[ord(pattern[i])] = value

        return bad_char_table

    def good_suffix_init(pattern, length_of_pattern):
        border_position = [0] * (length_of_pattern + 1)
        good_suffix_table = [0] * (length_of_pattern + 1)
        
        pattern_index = length_of_pattern
        table_index = length_of_pattern + 1
        border_position[pattern_index] = table_index
    
        while pattern_index > 0:
            while table_index <= length_of_pattern and pattern[pattern_index - 1] != pattern[table_index - 1]:
                if good_suffix_table[table_index] == 0:
                    good_suffix_table[table_index] = table_index - pattern_index
                table_index = border_position[table_index]
            pattern_index -= 1
            table_index -= 1
            border_position[pattern_index] = table_index

        # fill the remaining table
        value = border_position[0]
        for index in range(length_of_pattern + 1):
            
            if good_suffix_table[index] == 0:
                good_suffix_table[index] = value
                
            if index == value:
                value = border_position[value]
        
        return good_suffix_table
        
    def search(text, pattern):
        text = Algorithms.remove_spaces(text.lower())
        pattern = pattern.lower()

        length_of_text = len(text)
        length_of_pattern = len(pattern)
        
        bad_char_table = Algorithms.bad_table_init(pattern, length_of_pattern)
        good_suffix_table = Algorithms.good_suffix_init(pattern, length_of_pattern)

        shift = 0

        while (shift <= length_of_text - length_of_pattern):
            current_index = length_of_pattern - 1
            total_match = 0

            while current_index >= 0 and pattern[current_index] == text[shift + current_index]:
                current_index -= 1
                total_match += 1

            if current_index < 0:
                return True
            
            if ord(text[shift + current_index]) > 256:
                shift += 1
                continue
            shift += max(good_suffix_table[current_index + 1], bad_char_table[ord(text[shift + current_index])])

        return False
    
    def split_keywords(string):
        if not string:
            return []

        string = Algorithms.remove_spaces(string)
        list = string.split(",")
            
        return list
    
    def remove_spaces(string):
        string = string.replace(" ", "")
        return string

