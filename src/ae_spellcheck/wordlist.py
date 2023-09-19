import pickle
from pathlib import Path

class WordList:
    def __init__(self, data_path: str = __file__):
        self.data_path = data_path
        self.abb_path = Path(self.data_path).parent / 'abbreviations.pkl'
        self.word_path = Path(self.data_path).parent / 'words.pkl'
        self.load_words()

    def __repr__(self) -> str:
        return f"Words({self.data_path})"

    def load_words(self) -> tuple[tuple, tuple]:

        if self.abb_path.exists():
            with open(self.abb_path, 'rb') as f:
                self.abbreviations = pickle.load(f)
            with open(self.word_path, 'rb') as f:
                self.words = pickle.load(f)
        else:
            self.abbreviations = ()
            self.words = ()
            self.save_words()

        return self.abbreviations, self.words

    def save_words(self, abbreviations: tuple = (), words: tuple = (), validate: bool = True) -> tuple[tuple[str], tuple[str]]:
        if validate:
            words = self.validate_words(words)
            abbreviations = self.validate_abbr(abbreviations)
        if abbreviations != ():
            self.abbreviations += abbreviations
        if words != ():
            self.words += words

        self.abbreviations = tuple(set(self.abbreviations))
        self.words = tuple(set(self.words))

        with open(self.abb_path, 'wb') as f:
            pickle.dump(self.abbreviations, f)
        with open(self.word_path, 'wb') as f:
            pickle.dump(self.words, f)
        return self.abbreviations, self.words # type: ignore

    def ingest_words(self, filepath: str) -> None:
        total_words = len(self.words)
        with open(filepath, 'r') as f:
            words = tuple(word.strip().lower() for word in f.readlines())
        total_new_words = len(words)
        self.save_words(words=words)
        total_saved_words = len(self.words) - total_words

        print(f"Total words in new file: {total_new_words}")
        print(f"Total words in dictionary: {len(self.words)}")
        print(f"Total NEW words saved: {total_saved_words}")
        print()

        return None
        

    def ingest_abbreviations(self, filepath: str) -> None:
        total_abbreviations = len(self.abbreviations)
        with open(filepath, 'r') as f:
            abbreviations = tuple(word.strip() for word in f.readlines())
        total_new_abbreviations = len(abbreviations)
        self.save_words(abbreviations=abbreviations)
        total_saved_abbreviations = len(self.abbreviations) - total_abbreviations
        print(f"Total abbreviations in new file: {total_new_abbreviations}")
        print(f"Total abbreviations in dictionary: {len(self.abbreviations)}")
        print(f"Total NEW abbreviations saved: {total_saved_abbreviations}")
        print()

        return None
    
    def validate_words(self, words: tuple[str]) -> tuple[str]:
        accepted_wordlist = []
        accepted_characters = tuple('abcdefghijklmnopqrstuvwxyz-')
        skipped = {}
        for word in words:
            if len(word) <= 1:          # Skip words with 1 or less characters
                skipped = _collect_skipped_in_validation(skipped, 'Skipped due to length', word)
                continue
            if any(character not in accepted_characters for character in word):     # Skip words with non-alphabetical characters
                skipped = _collect_skipped_in_validation(skipped, 'Skipped due to length', word)
                continue
            accepted_wordlist.append(word)
        print(_print_items_skipped_in_validation(skipped))
        return tuple(accepted_wordlist)

    def validate_abbr(self, abbreviations: tuple[str]) -> tuple[str]:
        accepted_wordlist = []
        accepted_characters = tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ-abcdefghijklmnopqrstuvwxyz')
        skipped = {}
        for abbreviation in abbreviations:
            if len(abbreviation) <= 1:          # Skip abbreviation with 1 or less characters
                skipped = _collect_skipped_in_validation(skipped, 'Skipped due to length', abbreviation)
                continue
            if any(character not in accepted_characters for character in abbreviation):     # Skip abbreviation with non-alphabetical characters
                skipped = _collect_skipped_in_validation(skipped, 'Skipped due to non-alphabetical characters', abbreviation)
                continue
            accepted_wordlist.append(abbreviation)
        print(_print_items_skipped_in_validation(skipped))
        return tuple(accepted_wordlist)

    def check(self, word: str) -> bool:
        if word in self.abbreviations:
            return True
        elif word.lower() in self.words:
            return True
        else:
            return False

    def find_errors(self, word_list: tuple[str]):
        for word in word_list:
            if not self.check(word):
                yield word

def _collect_skipped_in_validation(skipped:dict, reason: str, word: str) -> dict:
    if reason in skipped.keys():
        skipped[reason].append(word)
    else:
        skipped[reason] = [word]
    return skipped

def _print_items_skipped_in_validation(skipped: dict) -> str:
    output = ''
    for reason, words in skipped.items():
        output += f'\nWords {reason}:\n\t'
        output += ', '.join(words)

    return output