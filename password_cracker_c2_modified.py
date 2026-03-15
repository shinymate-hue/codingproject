import hashlib
import argparse
import sys
from typing import Set

class PasswordCracker:
    """
    A modular class designed to perform dictionary-based hash cracking.
    
    By wrapping the logic in a class (Object-Oriented Programming), we encapsulate
    the state (the loaded hashes, the algorithm) and the behavior (loading, cracking).
    This makes the code much easier to import and reuse in larger security 
    toolkits or automation scripts later on.
    """
    
    def __init__(self, target_file: str, algorithm: str = 'md5'):
        """
        The constructor method initializes the state of our PasswordCracker object.
        
        Args:
            target_file (str): The path to the text file containing the hashes we want to crack.
            algorithm (str): The hashing algorithm to use (defaults to md5).
        """
        self.target_file = target_file
        
        # Normalize the algorithm name to ensure it matches hashlib's expected format.
        # For example, if a user types "SHA-256", this converts it to "sha256".
        self.algorithm = algorithm.lower().replace("-", "")
        
        # Initialize an empty set to hold our target hashes.
        # Type hinting (Set[str]) is used here to indicate this variable will hold a set of strings.
        self.target_hashes: Set[str] = set()

        # Input Validation: Check if the provided algorithm is actually supported by hashlib.
        # It is best practice to fail early in the initialization phase rather than 
        # encountering an error deep inside the processing loop.
        if self.algorithm not in hashlib.algorithms_available:
            print(f"[!] Error: Unsupported algorithm '{self.algorithm}'.")
            print(f"    Available algorithms: {', '.join(hashlib.algorithms_guaranteed)}")
            # Exit the script with a status code of 1, indicating an error occurred.
            sys.exit(1)

    def load_hashes(self) -> None:
        """
        Reads the target hash file and loads the hashes into memory using a Set.
        """
        try:
            # Open the file using a context manager ('with' statement).
            # This ensures the file is safely and automatically closed even if an error occurs.
            # Using encoding='utf-8' prevents UnicodeDecodeErrors across different operating systems.
            with open(self.target_file, 'r', encoding='utf-8') as f:
                
                # Set Comprehension: This is a highly optimized, Pythonic way to read the file.
                # It iterates through each line 'f', removes whitespace/newlines using 'strip()',
                # converts the hash to lowercase (to ensure consistent matching), and adds it 
                # directly to the 'self.target_hashes' set.
                # It also ignores empty lines using the 'if line.strip()' condition.
                self.target_hashes = {line.strip().lower() for line in f if line.strip()}
                
            print(f"[*] Successfully loaded {len(self.target_hashes)} hashes into memory.")
            
        except FileNotFoundError:
            # Handle the specific case where the user provided a bad file path.
            print(f"[!] Error: The target hash file was not found at '{self.target_file}'")
            sys.exit(1)

    def crack(self, wordlist_path: str) -> int:
        """
        Executes the dictionary attack by hashing words from the wordlist and 
        comparing them against the loaded target hashes.
        
        Args:
            wordlist_path (str): The file path to the dictionary/wordlist.
            
        Returns:
            int: The total number of passwords successfully cracked.
        """
        # Safety check: Ensure we actually have hashes to crack before starting the heavy lifting.
        if not self.target_hashes:
            print("[-] No target hashes loaded. Please run load_hashes() first.")
            return 0

        found_count = 0

        try:
            # Open the wordlist in 'rb' (read-binary) mode.
            # Real-world wordlists (like rockyou.txt) often contain corrupted or non-UTF-8 
            # characters. Reading in binary mode prevents the script from crashing when 
            # it encounters these strange bytes.
            with open(wordlist_path, "rb") as wordlist_file:
                
                # Iterate through the file line by line. This is highly memory efficient 
                # because it only loads one word into RAM at a time, allowing us to process 
                # massive multi-gigabyte wordlists without crashing the system.
                for word_bytes in wordlist_file:
                    
                    # Remove trailing whitespaces or newline characters from the byte string.
                    word_bytes = word_bytes.rstrip()
                    
                    # Skip the iteration if the line was empty.
                    if not word_bytes:
                        continue 

                    # Dynamically generate the hash for the current word.
                    # 'hashlib.new()' is the standard, safest way to call a hashing function 
                    # by its string name. It is faster and more reliable than using 'getattr'.
                    hashed_entry = hashlib.new(self.algorithm, word_bytes).hexdigest()

                    # Time Complexity check: Because 'self.target_hashes' is a Set, 
                    # this 'in' lookup operates in $O(1)$ constant time. If it were a List, 
                    # it would be $O(n)$, which would drastically slow down the cracking process.
                    if hashed_entry in self.target_hashes:
                        
                        # We found a match! Call our helper method to print the result.
                        self._handle_found_password(hashed_entry, word_bytes)
                        found_count += 1
                        
                        # Optimization: Remove the cracked hash from our target set.
                        # This keeps the set small, maintaining maximum lookup speed,
                        # and prevents us from accidentally cracking the same hash twice.
                        self.target_hashes.remove(hashed_entry)

                        # Early Exit Optimization: If the set is empty, we have cracked 
                        # all our targets. There is no need to continue reading the rest 
                        # of the wordlist. We break out of the loop to save time and CPU cycles.
                        if not self.target_hashes:
                            print("[*] All hashes cracked! Stopping early to save time.")
                            break

        except FileNotFoundError:
            print(f"[!] Error: The wordlist file was not found at '{wordlist_path}'")
            sys.exit(1)

        # Return the total number of successful cracks to the main function.
        return found_count

    def _handle_found_password(self, hashed_entry: str, word_bytes: bytes) -> None:
        """
        A private helper method (indicated by the leading underscore) responsible 
        for safely formatting and printing the discovered passwords to the console.
        """
        try:
            # Attempt to decode the raw binary bytes back into a readable UTF-8 string.
            word_string = word_bytes.decode('utf-8')
            print(f"[+] Password Found! | Hash: {hashed_entry} -> Password: {word_string}")
        except UnicodeDecodeError:
            # Fallback: If the password consists of weird characters that cannot be 
            # printed as standard text, print the raw hexadecimal representation instead.
            print(f"[!] Password Found (Hex due to decode error): {hashed_entry} -> {word_bytes.hex()}")


def main():
    """
    The main execution block of the script. It handles command-line arguments 
    and orchestrates the workflow of the PasswordCracker class.
    """
    # Initialize the ArgumentParser to handle command-line inputs gracefully.
    parser = argparse.ArgumentParser(description='Crack hashes using a highly optimized dictionary attack.')
    
    # Define the expected arguments.
    # '-w' is required because a dictionary attack cannot run without a dictionary.
    parser.add_argument('-w', '--wordlist', required=True, help='Path to the wordlist file')
    parser.add_argument('-t', '--target', default='password-hashes.txt', help='File containing hashes to crack (Default: password-hashes.txt)')
    parser.add_argument('-a', '--algorithm', default='md5', help='Hash algorithm to use (e.g., md5, sha256). Default is md5.')

    # Parse the arguments provided by the user in the terminal.
    args = parser.parse_args()

    # Print a clean, informative header so the user knows exactly what configuration is running.
    print(f"[*] Wordlist file: {args.wordlist}")
    print(f"[*] Target hash file: {args.target}")
    print(f"[*] Hash Algorithm: {args.algorithm.upper()}")
    print("-" * 50)

    # Step 1: Instantiate our PasswordCracker object with the user's settings.
    cracker = PasswordCracker(target_file=args.target, algorithm=args.algorithm)
    
    # Step 2: Load the targets into memory.
    cracker.load_hashes()
    
    # Step 3: Begin the cracking process and store the final count of found passwords.
    found_count = cracker.crack(wordlist_path=args.wordlist)
    
    # Step 4: Print a final summary of the operation.