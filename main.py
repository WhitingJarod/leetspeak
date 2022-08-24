import re
leet_letters_upper = "48CD3FGHIJK1MN0PQR57UVWXYZ"
leet_letters_lower = "@bcd3fghijk1mn0pqr57uvwxyz"
leet_numerology = "0134578"
normal_people_letters_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
normal_people_letters_lower = "abcdefghijklmnopqrstuvwxyz"
sentence_pattern = re.compile(".+[\.\?\!]*")
word_pattern = re.compile("([A-Za-z0-9@]+)([^A-Za-z0-9@]+)*")

# Take a word and try to guess whether it is supposed to be a number, all uppercase, or all lowercase.
# This is because we don't want to de-leet a number that is supposed to be a number, and we need to determine whether a 5 is S or s.
def get_context(word):
    uppers = [l for l in word if l.isupper()]
    lowers = [l for l in word if l.islower()]
    numbers = [l for l in word if l.isdigit()]
    if len(numbers) == len(word):
        # the word is nothing but numbers
        # run this series of loops and checks to see if it contains any characters which are NOT leetspeak numbers
        # if they are all leetspeak numbers, we consider it to be 'lowercase' because we prioritize leetspeak over numbers.
        # this means that the number 1337 becomes "leet" but the number 2337 is left alone, assumed to be an actual number.
        # Not perfect, but what do you expect from something as irrational as leetspeak.
        is_compliant = True
        for a in word:
            loop_compliant = False
            for b in leet_numerology:
                if a == b:
                    loop_compliant = True
                    break
            if not loop_compliant:
                is_compliant = False
                break
        if not is_compliant: return "number"
        else: return "lower"
    if len(uppers) > len(lowers): return "upper"
    # sorry bois, ThIs KiNd Of WrItInG is unsupported. Words are full-uppercase or full-lowercase.
    # Proper nouns? What's a proper noun?
    # First-letters of sentences are handled elsewhere.
    return "lower"

# Take a letter and convert it. Context is used when converting from leet into rational language.
def convert_letter(letter, context = None):
    # not proud of this function but it's guaranteed to return something even in unforseen circumstances.
    # that's really all that matters in rushed code. I was considering making a lot of these for loops into separate functions.
    # not worth the time and it wouldn't clean the code overall, it would only clean up this one function visually.
    # plus, the code performs infinitesimally faster without making these functions.
    # Thank you for tuning in to Coding Philosophy with Jarod
    if context == "upper":
    # Also I wanted this 'context' var to be an enum but as far as I'm aware that's not generally a python thing without imports.
        for i, v in enumerate(leet_letters_upper):
            if v == letter:
                return normal_people_letters_upper[i]
        for i, v in enumerate(leet_letters_lower):
            if v == letter:
                return normal_people_letters_lower[i]
        return letter
    elif context == "lower":
        for i, v in enumerate(leet_letters_lower):
            if v == letter:
                return normal_people_letters_lower[i]
        for i, v in enumerate(leet_letters_upper):
            if v == letter:
                return normal_people_letters_upper[i]
        return letter
    elif context == "number":
        return letter
    else:
        for i, v in enumerate(normal_people_letters_lower):
            if v == letter:
                return leet_letters_lower[i]
        for i, v in enumerate(normal_people_letters_upper):
            if v == letter:
                return leet_letters_upper[i]
        return letter

# Take normal, reasonable, and perfectly rational input and butcher it into leet speak
def to_leet_speak(text):
    output = ""
    for sentence in sentence_pattern.finditer(text): # break it into sentences
        sentence = sentence.string
        for match in word_pattern.finditer(text): # breakt it into words
            word = match.group(1) # the word
            symbols = match.group(2) # symbols after the word. whitespace, commas, colons, etc.
            new_word = ""
            for letter in word:
                new_word += convert_letter(letter) # call convert_letter with only one argument to convert to leetspeak
            output += new_word
            if not (symbols is None): output += symbols
    return output

# Take leet input and return normal ppl string
def to_normal_people_speak(text):
    output = ""
    for sentence in sentence_pattern.finditer(text): # break it into sentences
        sentence = sentence.string
        first_word = True
        for match in word_pattern.finditer(sentence): # break it into words
            word = match.group(1) # word
            symbols = match.group(2) # whitespace, periods, commas, etc.
            context = get_context(word) # best guess whether the word is a number, all caps, or all lowercase.
            new_word = ""
            for letter in word:
                if first_word:
                    first_word = False
                    new_word += convert_letter(letter, "upper") # try to capitalize the first letter in the sentence. We're not heathens.
                    continue
                new_word += convert_letter(letter, context)
            output += new_word
            if not (symbols is None): output += symbols
    return output

# Entrance function, just ugly loops for user input
def main():
    print("\n\nWelcome to the rational language to leetspeak converter")
    mode = ""
    while True:
        print("Type 'leet' to enter convert-to-leetspeak mode, or type 'english' to enter convert-to-English mode")
        t = input("> ")
        if t == "leet":
            mode = "leet"
        elif t == "english":
            mode = "english"
        else:
            print("\nUnrecognized input. Commands are case-sensitive. Try again.")
            continue
        print("Mode set to "+mode+". You can change mode at any time by typing 'leet' or 'english'")
        break
    print("Type 'help' for a list of commands. If your command was translated, it wasn't a valid command. Capitalization matters.")
    print("Type anything else to convert it.")
    while True:
        print("Please input a command or text to translate.")
        t = input("> ")
        if t == "help":
            print("""Commands:
    help: Type this command to get back to here. Duh.
    leet: Switch to convert-to-leetspeak mode.
    english: Switch to convert-to-English mode.""")
        elif t == "leet":
            mode = "leet"
            print("Now converting to leetspeak")
        elif t == "english":
            mode = "english"
            print("Now converting to English")
        else:
            if mode == "english":
                print(to_normal_people_speak(t))
            else:
                print(to_leet_speak(t))
        
main()