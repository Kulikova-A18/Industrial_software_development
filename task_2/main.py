import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('task.log', mode='w')
    ]
)

class LogMessages:
    # File operations messages
    FILE_READ_START = "Attempting to read sequence data from file: {}"
    FILE_READ_SUCCESS = "Successfully read {} numbers from file"
    FILE_EMPTY = "Input file is empty"
    FILE_NOT_FOUND = "Input file not found: {}"
    
    # Algorithm operation messages
    ALGORITHM_START = "Starting shortest segment search containing all alphabet letters"
    ALGORITHM_COMPLETE = "Algorithm complete. Shortest segment length: {}"
    ALGORITHM_EMPTY_INPUT = "Empty sequence provided"
    ALGORITHM_SEQUENCE_LENGTH = "Processing sequence of length {}"
    
    # Segment tracking messages
    SEGMENT_FOUND = "Found segment of length {} containing all letters"
    SEGMENT_UPDATED = "Updated shortest segment length to {}"
    ALPHABET_NOT_FOUND = "Complete alphabet not found in sequence"
    
    # Window tracking messages
    WINDOW_EXPAND = "Expanding window to position {}, current unique letters: {}"
    WINDOW_SHRINK = "Shrinking window from position {}, current unique letters: {}"
    LETTER_ADDED = "Added letter '{}' (code: {})"
    LETTER_REMOVED = "Removed letter '{}' (code: {})"

def find_shortest_segment_containing_alphabet(sequence):
    """
    Finds the shortest segment (contiguous subsequence) that contains all letters A-Z (codes 1-26).
    
    Args:
        sequence: List of integers representing letter codes
        
    Returns:
        int or str: Length of shortest segment or "NONE" if not found
    """
    try:
        if not sequence:
            logging.warning(LogMessages.ALGORITHM_EMPTY_INPUT)
            return "NONE"
        
        sequence_length = len(sequence)
        logging.info(LogMessages.ALGORITHM_SEQUENCE_LENGTH.format(sequence_length))
        
        # Map numbers to letters for logging
        number_to_letter = {i: chr(64 + i) for i in range(1, 27)}
        
        # Sliding window algorithm
        target_letter_count = 26
        current_unique_letters = 0
        letter_frequency = {}
        
        left_pointer = 0
        shortest_segment_length = float('inf')
        
        # logging.info("Starting sliding window algorithm...")
        
        for right_pointer in range(sequence_length):
            current_number = sequence[right_pointer]
            human_right_pos = right_pointer + 1
            
            # Process only valid letter codes (1-26)
            if 1 <= current_number <= 26:
                current_letter = number_to_letter[current_number]
                
                # Add letter to frequency count
                if current_number not in letter_frequency or letter_frequency[current_number] == 0:
                    current_unique_letters += 1
                    logging.debug(LogMessages.LETTER_ADDED.format(current_letter, current_number))
                
                letter_frequency[current_number] = letter_frequency.get(current_number, 0) + 1
                
                logging.debug(LogMessages.WINDOW_EXPAND.format(human_right_pos, current_unique_letters))
            
            # Shrink window from left while we have all letters
            while current_unique_letters == target_letter_count and left_pointer <= right_pointer:
                current_segment_length = right_pointer - left_pointer + 1
                
                if current_segment_length < shortest_segment_length:
                    shortest_segment_length = current_segment_length
                    # logging.info(LogMessages.SEGMENT_UPDATED.format(shortest_segment_length))
                    # logging.debug(f"Segment positions: {left_pointer + 1} to {human_right_pos}")
                
                left_number = sequence[left_pointer]
                human_left_pos = left_pointer + 1
                
                # Remove left letter from frequency count
                if 1 <= left_number <= 26:
                    left_letter = number_to_letter[left_number]
                    letter_frequency[left_number] -= 1
                    
                    if letter_frequency[left_number] == 0:
                        current_unique_letters -= 1
                        logging.debug(LogMessages.LETTER_REMOVED.format(left_letter, left_number))
                
                logging.debug(LogMessages.WINDOW_SHRINK.format(human_left_pos, current_unique_letters))
                left_pointer += 1

        # Check if found a valid segment
        if shortest_segment_length != float('inf'):
            # logging.info(LogMessages.SEGMENT_FOUND.format(shortest_segment_length))
            # logging.info(LogMessages.ALGORITHM_COMPLETE.format(shortest_segment_length))
            return shortest_segment_length
        else:
            logging.info(LogMessages.ALPHABET_NOT_FOUND)
            logging.info(LogMessages.ALGORITHM_COMPLETE.format("NONE"))
            return "NONE"
        
    except Exception as error:
        logging.error(f"Error in shortest segment search: {str(error)}")
        return "NONE"

def read_sequence_from_file(filename):
    """
    Reads sequence data from input file.
    
    Expected format:
    First line: length numbers...
    Subsequent lines: continuation of numbers
    
    Args:
        filename: Path to the input file
        
    Returns:
        list: List of integers representing the sequence
    """
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            
            if not lines:
                logging.error(LogMessages.FILE_EMPTY)
                raise ValueError(LogMessages.FILE_EMPTY)
            
            sequence = []
            
            # Parse first line
            first_line = lines[0].strip().split()
            if not first_line:
                logging.error("First line is empty")
                raise ValueError("First line is empty")
            
            # Skip the first number (length) and add the rest
            for num_str in first_line[1:]:
                sequence.append(int(num_str))
            
            # Parse remaining lines
            for line_num, line in enumerate(lines[1:], 2):
                line = line.strip()
                if line:
                    numbers = line.split()
                    for num_str in numbers:
                        sequence.append(int(num_str))

            return sequence
            
    except FileNotFoundError:
        logging.error(LogMessages.FILE_NOT_FOUND.format(filename))
        raise
    except Exception as error:
        logging.error(f"Error reading file {filename}: {str(error)}")
        raise

def main():
    """
    Main execution function.
    """
    try:
        filename = 'data_prog_contest_problem_2.txt'
        sequence = read_sequence_from_file(filename)
        
        # Find shortest segment containing all alphabet letters
        result = find_shortest_segment_containing_alphabet(sequence)

        logging.info(f"FINAL RESULT: {result}")

    except Exception as error:
        logging.error(f"Error in main execution: {str(error)}")
        print("Error processing file. Check log for details.")

if __name__ == "__main__":
    main()
