from colorist import Color as COLOR
from random import sample, choice
from math import prod

def clear():
    """Clears the console screen based on the operating system."""
    from os import system, name
    system('cls' if name == 'nt' else 'clear')

class Mastermind:
    def __init__(self):
        """
        Initializes the Mastermind game.
        """
        self.greet()
        
        self.difficulty_level = self.get_difficulty()
        self.max_attempts = prod(range(10, 10 - self.difficulty_level, -1))
        self.n_attempt = 0
        
        self.hints = []
        self.hints_taken = 0
        self.is_game_finished = False
        self.end_msg = ''
        
        self.secret_key = self.generate_key()
        print(f"{COLOR.MAGENTA}Key Generated.{COLOR.OFF}\n")

        self.game_loop()

    def greet(self):
        """
        Displays the welcome message and game instructions.
        """
        clear()
        print(f"\t\t{COLOR.MAGENTA}Welcome to the classic game Mastermind!{COLOR.OFF} 🧠")
        print(f"\n{COLOR.CYAN}HELP:{COLOR.OFF}",
              "number: not present in key,",
              f"{COLOR.YELLOW}number{COLOR.OFF}: present in key,",
              f"{COLOR.GREEN}number{COLOR.OFF}: present and in correct location in key.",
              f"{COLOR.BLUE}hint{COLOR.OFF}: to receive a hint about the secret key,",
              f"{COLOR.BLUE}newgame{COLOR.OFF}: to start a new game,",
              f"{COLOR.BLUE}exit{COLOR.OFF}: to exit the game,",
              f"{COLOR.RED}No digits are repeated.{COLOR.OFF}", sep='\n    ')
        print(f"\n{COLOR.CYAN}Good Luck! 👍{COLOR.OFF}\n")
        print(f"{COLOR.CYAN}Press enter to continue with default difficulty level: 4{COLOR.OFF}")

    def get_difficulty(self, err_msg='') -> int:
        """
        Prompts the user to enter a valid difficulty level for the game.

        Returns:
            int: The difficulty level.
        """
        difficulty = input(err_msg + "Enter difficulty (1-10): ")
        if difficulty == '':
            return 4
        try:
            difficulty = int(difficulty)
        except:
            return self.get_difficulty(err_msg=f"{COLOR.RED}Enter only numeric value!{COLOR.OFF}\n")
        else:
            if 1 <= difficulty <= 10:
                return difficulty
            else:
                return self.get_difficulty(err_msg=f"{COLOR.RED}Not in range!{COLOR.OFF}\n")

    def generate_key(self) -> str:
        """
        Generates a random secret key consisting of unique digits.

        Returns:
            str: The generated secret key.
        """
        from string import digits
        key = ''.join(sample(digits, self.difficulty_level))
        
        return key

    def game_loop(self):
        """
        Main loop of the game that continues until the user guesses the key.
        """
        while not self.is_game_finished:
            self.get_user_guess()
            self.evaluate_guess()
        else:
            print(self.end_msg)
            print(rf"{COLOR.CYAN}Great Guessing! （*＾-＾*）{COLOR.OFF}")
            if input(f"{COLOR.MAGENTA}Replay? (y/N):{COLOR.OFF} ").lower() == 'y':
                Mastermind()
    
    def generateHints(self):
        """
        Generates hints about the secret key.
        """
        listed_key = list(map(int, self.secret_key))
        sum_of_digits = sum(listed_key)
        prod_of_digits = prod(listed_key)
        range_of_digits = f"{min(listed_key)} -> {max(listed_key)}"
        self.hints = [
            f"{COLOR.BLUE}The sum of the digits is: {sum_of_digits}{COLOR.OFF}",
            f"{COLOR.BLUE}The product of the digits is: {prod_of_digits}{COLOR.OFF}",
            f"{COLOR.BLUE}The range of the digits is: {range_of_digits}{COLOR.OFF}",
        ]

    def get_user_guess(self):
        """
        Prompts the user to enter their guess and validates the input.
        """        
        user_input = input(f"{COLOR.CYAN}Enter guess:{COLOR.OFF} ").strip()
        if user_input == "hint":
            if not self.hints:
                self.generateHints()
            print(choice(self.hints))
            return self.get_user_guess()
        elif user_input == "newgame":
            print("Ok!")
            Mastermind()
            import sys
            sys.exit()
        elif user_input == "exit":
            print("👋")
            import sys
            sys.exit()
        
        self.n_attempt += 1
        self.is_game_finished = self.n_attempt == self.max_attempts
        if self.is_game_finished:
            self.end_msg = f"\n{COLOR.YELLOW}Uh Oh! Max attempts reached! o_o{COLOR.OFF}\n"\
                            + f"{COLOR.YELLOW}The secret key was `{self.secret_key}`{COLOR.OFF}\n"
        
        if not user_input.isdigit():
            print(f"{COLOR.RED}Must contain only numeric characters.{COLOR.OFF}")
            return self.get_user_guess()
        elif len(user_input) != self.difficulty_level:
            print(f"{COLOR.RED}Expected guess length {self.difficulty_level} got {len(user_input)}.{COLOR.OFF}")
            return self.get_user_guess()
        elif len(set(user_input)) != self.difficulty_level:
            print(f"{COLOR.RED}Every digit must be unique.{COLOR.OFF}")
            return self.get_user_guess()

        self.user_guess = user_input
    
    def evaluate_guess(self):
        """
        Evaluates the user's guess against the secret key and generates feedback.
        """
        if self.user_guess == self.secret_key:
            self.end_msg = f"{COLOR.GREEN}Secret key unveiled: {self.user_guess} !{COLOR.OFF}\n"
            self.is_game_finished = True
        else:
            remarks = ''
            for i, digit in enumerate(self.user_guess):
                if digit == self.secret_key[i]:
                    remarks += f"{COLOR.GREEN}{digit}{COLOR.OFF} "
                elif digit in self.secret_key:
                    remarks += f"{COLOR.YELLOW}{digit}{COLOR.OFF} "
                else:
                    remarks += f"{digit} "
            
            print("Remark: " + remarks)


if __name__ == "__main__":
    Mastermind()
