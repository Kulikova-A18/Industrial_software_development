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
    FILE_READ_START = "Attempting to read segments data from file: {}"
    FILE_READ_SUCCESS = "Successfully read {} segments from file"
    FILE_EMPTY = "Input file is empty"
    FILE_NOT_FOUND = "Input file not found: {}"
    FILE_FORMAT_INVALID = "Invalid segment count format: {}"
    FILE_UNEXPECTED_END = "Unexpected end of file at line {}"
    FILE_SEGMENT_INVALID = "Invalid segment data at line {}: {}"
    FILE_NUMERIC_INVALID = "Invalid numeric data at line {}: {}"
    
    # Algorithm operation messages
    ALGORITHM_START = "Starting minimum points calculation for segment coverage"
    ALGORITHM_COMPLETE = "Calculation complete. Required {} points: {}"
    ALGORITHM_EMPTY_INPUT = "Empty segments list provided"
    ALGORITHM_SEGMENT_COUNT = "Processing {} segments"
    ALGORITHM_SORTING_START = "Sorting segments by right endpoint"
    ALGORITHM_SORTING_COMPLETE = "Segments sorted successfully"
    ALGORITHM_VALIDATION_START = "Validating segments data"
    ALGORITHM_VALIDATION_COMPLETE = "Segments validation completed successfully"
    
    # Segment processing messages
    SEGMENT_INVALID_FORMAT = "Segment {} has invalid format: {}"
    SEGMENT_INVALID_RANGE = "Segment {} has start > end: {}"
    SEGMENT_PROCESSING_START = "Processing segment {}: ({}, {})"
    SEGMENT_NEW_POINT = "Selected new point: {} for segment ({}, {})"
    SEGMENT_COVERED = "Current point {} covers segment ({}, {})"
    
    # Point selection messages
    POINT_SELECTION_START = "Starting point selection process"
    POINT_SELECTION_COMPLETE = "Point selection completed. Selected {} points"
    POINT_INITIAL_SELECTION = "Initial point selected: {}"
    POINT_ADDITIONAL_SELECTION = "Additional point selected: {} (total: {} points)"

    # Pipeline messages
    PIPELINE_START = "Starting segment coverage processing pipeline ..."
    PIPELINE_COMPLETE = "Processing pipeline completed successfully"
    PIPELINE_FAILED = "Processing pipeline failed: {}"
    RESULTS_HEADER = "PROCESSING RESULTS"
    RESULTS_SEGMENTS = "Total segments processed: {}"
    RESULTS_POINTS = "Minimum points required: {}"
    RESULTS_LOCATIONS = "Optimal point locations: {}"
    
    # Error messages
    ERROR_GENERIC = "Error in {}: {}"
    ERROR_VALIDATION = "Segments validation error: {}"
    ERROR_CALCULATION = "Error in minimum points calculation: {}"
    ERROR_FILE_READING = "Unexpected error reading file {}: {}"
    ERROR_DEMONSTRATION = "Error in demonstration: {}"
    ERROR_CRITICAL = "Critical error in main execution: {}"

def find_minimum_points_to_cover_all_segments(list_of_segments):
    """
    Finds the minimum number of points required to cover all segments.
    
    Each segment is represented as a tuple (start_coordinate, end_coordinate).
    A point covers a segment if it lies within the segment's range.
    
    Args:
        list_of_segments: List of tuples representing segments (start, end)
        
    Returns:
        tuple: (number_of_points_required, list_of_selected_points)
        
    Raises:
        ValueError: If segments data is invalid
    """
    try:
        logging.info(LogMessages.ALGORITHM_START)

        segment_count = len(list_of_segments)
        logging.info(LogMessages.ALGORITHM_SEGMENT_COUNT.format(segment_count))
        
        if segment_count == 0:
            logging.warning(LogMessages.ALGORITHM_EMPTY_INPUT)
            return 0, []

        logging.info(LogMessages.ALGORITHM_VALIDATION_START)
        validation_segment_count = 0
        for segment_index, current_segment in enumerate(list_of_segments):
            validation_segment_count += 1
            logging.debug(f"Validating segment {validation_segment_count}/{segment_count}")
            
            if len(current_segment) != 2:
                error_message = LogMessages.SEGMENT_INVALID_FORMAT.format(segment_index, current_segment)
                logging.error(error_message)
                raise ValueError(error_message)
            
            start_coord, end_coord = current_segment
            if start_coord > end_coord:
                error_message = LogMessages.SEGMENT_INVALID_RANGE.format(segment_index, current_segment)
                logging.error(error_message)
                raise ValueError(error_message)
        
        logging.info(LogMessages.ALGORITHM_VALIDATION_COMPLETE)
        logging.info(f"Successfully validated {validation_segment_count} segments")
        
        # Sort segments by their right endpoint with counting
        logging.info(LogMessages.ALGORITHM_SORTING_START)
        segments_sorted_by_right_endpoint = sorted(list_of_segments, key=lambda segment: segment[1])
        logging.info(LogMessages.ALGORITHM_SORTING_COMPLETE)
        logging.info(f"Sorted {len(segments_sorted_by_right_endpoint)} segments by right endpoint")
        
        selected_points_list = []
        current_covering_point = None
        segments_processed_count = 0
        new_points_selected_count = 0
        
        logging.info(LogMessages.POINT_SELECTION_START)
        
        # Process each segment to find optimal points with detailed counting
        for segment_index, current_segment in enumerate(segments_sorted_by_right_endpoint):
            segments_processed_count += 1
            segment_start, segment_end = current_segment
            
            logging.info(LogMessages.SEGMENT_PROCESSING_START.format(
                segments_processed_count, segment_start, segment_end))
            logging.debug(f"Progress: {segments_processed_count}/{segment_count} segments processed")

            if current_covering_point is None or current_covering_point < segment_start:
                current_covering_point = segment_end
                selected_points_list.append(current_covering_point)
                new_points_selected_count += 1
                
                logging.info(LogMessages.SEGMENT_NEW_POINT.format(
                    current_covering_point, segment_start, segment_end))
                
                if new_points_selected_count == 1:
                    logging.info(LogMessages.POINT_INITIAL_SELECTION.format(current_covering_point))
                else:
                    logging.info(LogMessages.POINT_ADDITIONAL_SELECTION.format(
                        current_covering_point, new_points_selected_count))
                    
                logging.debug(f"Total points selected so far: {new_points_selected_count}")
            else:
                logging.info(LogMessages.SEGMENT_COVERED.format(
                    current_covering_point, segment_start, segment_end))
                logging.debug(f"Segment covered by existing point, no new point needed")
        
        total_points_required = len(selected_points_list)
        logging.info(LogMessages.POINT_SELECTION_COMPLETE.format(total_points_required))
        logging.info(LogMessages.ALGORITHM_COMPLETE.format(total_points_required, selected_points_list))
        
        # Final statistics
        logging.info(f"Algorithm statistics:")
        logging.info(f"Total segments processed: {segments_processed_count}")
        logging.info(f"Points selected: {total_points_required}")
        logging.info(f"Coverage efficiency: {segments_processed_count/total_points_required:.2f} segments per point")
        
        return total_points_required, selected_points_list
        
    except Exception as error:
        logging.error(LogMessages.ERROR_CALCULATION.format(str(error)))
        raise

def read_segments_data_from_input_file(input_filename):
    """
    Reads segments data from input file.
    
    Expected file format:
    First line: number_of_segments
    Subsequent lines: segment_start segment_end (separated by whitespace)
    
    Args:
        input_filename: Path to the input file
        
    Returns:
        list: List of tuples (start, end) representing segments
        
    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If file format is invalid
    """
    try:
        logging.info(LogMessages.FILE_READ_START.format(input_filename))
        
        with open(input_filename, 'r') as input_file:
            # Read number of segments
            first_line = input_file.readline().strip()
            if not first_line:
                logging.error(LogMessages.FILE_EMPTY)
                raise ValueError(LogMessages.FILE_EMPTY)
            
            try:
                total_segments_count = int(first_line)
                logging.info(f"File header indicates {total_segments_count} segments to read")
            except ValueError:
                logging.error(LogMessages.FILE_FORMAT_INVALID.format(first_line))
                raise ValueError(LogMessages.FILE_FORMAT_INVALID.format(first_line))
            
            segments_data = []
            lines_read_count = 0
            segments_read_count = 0
            lines_skipped_count = 0

            for line_number in range(2, total_segments_count + 2):
                lines_read_count += 1
                line_content = input_file.readline()
                
                if not line_content:
                    logging.error(LogMessages.FILE_UNEXPECTED_END.format(line_number))
                    raise ValueError(LogMessages.FILE_UNEXPECTED_END.format(line_number))
                
                line_content = line_content.strip()
                if not line_content:
                    lines_skipped_count += 1
                    logging.debug(f"Skipped empty line at position {line_number}")
                    continue

                line_tokens = line_content.split()
                if len(line_tokens) < 2:
                    logging.error(LogMessages.FILE_SEGMENT_INVALID.format(line_number, line_content))
                    raise ValueError(LogMessages.FILE_SEGMENT_INVALID.format(line_number, line_content))
                
                try:
                    start_coordinate = int(line_tokens[0])
                    end_coordinate = int(line_tokens[1])
                    
                    # start <= end
                    actual_start = min(start_coordinate, end_coordinate)
                    actual_end = max(start_coordinate, end_coordinate)
                    
                    segments_data.append((actual_start, actual_end))
                    segments_read_count += 1

                    # Log progress for every 10 segments
                    # if segments_read_count % 10 == 0:
                    #     logging.info(f"Progress: read {segments_read_count}/{total_segments_count} segments ...")
                        
                except ValueError:
                    logging.error(LogMessages.FILE_NUMERIC_INVALID.format(line_number, line_content))
                    raise ValueError(LogMessages.FILE_NUMERIC_INVALID.format(line_number, line_content))
            
            # Final file reading statistics
            logging.info(LogMessages.FILE_READ_SUCCESS.format(len(segments_data)))
            logging.info(f"File reading statistics:")
            logging.info(f"Expected segments: {total_segments_count}")
            logging.info(f"Actual segments read: {segments_read_count}")
            logging.info(f"Lines processed: {lines_read_count}")
            logging.info(f"Empty lines skipped: {lines_skipped_count}")
            
            if len(segments_data) != total_segments_count:
                logging.warning(f"Segment count mismatch: expected {total_segments_count}, got {len(segments_data)}")
            
            return segments_data
            
    except FileNotFoundError:
        logging.error(LogMessages.FILE_NOT_FOUND.format(input_filename))
        raise
    except Exception as error:
        logging.error(LogMessages.ERROR_FILE_READING.format(input_filename, str(error)))
        raise

def execute_main_processing_pipeline():
    """
    Main execution function that coordinates the entire processing pipeline.
    """
    try:
        logging.info(LogMessages.PIPELINE_START)
        input_data_filename = 'data_prog_contest_problem_1.txt'

        logging.info(f"Reading data from: {input_data_filename}")
        segments_collection = read_segments_data_from_input_file(input_data_filename)
        
        # Calculate minimum points required
        logging.info("Starting main calculation for contest data ...")
        total_points_needed, optimal_points = find_minimum_points_to_cover_all_segments(segments_collection)
        
        # Display results with detailed statistics
        logging.info(LogMessages.RESULTS_HEADER)
        logging.info(LogMessages.RESULTS_SEGMENTS.format(len(segments_collection)))
        logging.info(LogMessages.RESULTS_POINTS.format(total_points_needed))
        logging.info(LogMessages.RESULTS_LOCATIONS.format(optimal_points))
        
        # Additional statistics
        coverage_ratio = len(segments_collection) / total_points_needed if total_points_needed > 0 else 0
        logging.info(f"Coverage ratio: {coverage_ratio:.2f} segments per point")
        logging.info(f"Optimization achieved: {len(segments_collection) - total_points_needed} fewer points than segments")
        
        logging.info(LogMessages.PIPELINE_COMPLETE)
        
        return total_points_needed, optimal_points
        
    except Exception as error:
        logging.error(LogMessages.PIPELINE_FAILED.format(str(error)))
        return None, None

if __name__ == "__main__":
    try:
        final_point_count, final_points = execute_main_processing_pipeline()
        
        if final_point_count is not None:
            logging.info(f"Final result displayed to user: {final_point_count} points")
        else:
            logging.error("Final result not available")
            
    except KeyboardInterrupt:
        logging.info("Processing interrupted by user")
    except Exception as critical_error:
        logging.critical(LogMessages.ERROR_CRITICAL.format(str(critical_error)))
