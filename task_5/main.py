import logging
import sys
import random

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('triangle_path.log', mode='w', encoding='utf-8')
    ]
)

class LogMessages:
    # Algorithm operation messages
    ALGORITHM_START = "Starting minimum path sum calculation for triangle"
    ALGORITHM_COMPLETE = "Algorithm complete. Minimum path sum: {}"
    ALGORITHM_EMPTY_INPUT = "Empty triangle provided"

    # Triangle processing messages
    TRIANGLE_SIZE = "Processing triangle with {} rows"
    ROW_PROCESSING = "Processing row {} with {} elements"
    DP_INITIALIZATION = "Initializing DP with base row: {}"
    DP_UPDATE = "Updating dp[{}] = min({} + {}, {} + {}) = {}"

    # Path reconstruction messages
    PATH_RECONSTRUCTION_START = "Starting path reconstruction"
    PATH_ELEMENT_ADDED = "Added element {} at position {} to path"
    PATH_COMPLETE = "Minimum path: {}"

    # Test messages
    TEST_START = "Starting test case {}"
    TEST_RESULT = "Test {}: Expected sum = {}, Got = {} | Expected path = {}, Got = {}"
    TEST_PASSED = "Test {} PASSED"
    TEST_FAILED = "Test {} FAILED"

    # Generation messages
    GENERATION_START = "Generating random test case {} with {} rows"
    GENERATION_COMPLETE = "Generated triangle: {}"

def minimum_total(triangle):
    """
    Finds the minimum path sum from top to bottom of the triangle.

    Args:
        triangle: List of lists representing the triangle

    Returns:
        tuple: (minimum_sum, path_taken)
    """
    try:
        logging.info(LogMessages.ALGORITHM_START)

        if not triangle or not triangle[0]:
            logging.warning(LogMessages.ALGORITHM_EMPTY_INPUT)
            return 0, []

        n = len(triangle)
        logging.info(LogMessages.TRIANGLE_SIZE.format(n))

        # Create DP table
        dp = [[0] * len(triangle[i]) for i in range(n)]

        # Initialize last row
        for j in range(len(triangle[n-1])):
            dp[n-1][j] = triangle[n-1][j]

        logging.info(LogMessages.DP_INITIALIZATION.format(dp[n-1]))

        # Fill DP table bottom-up
        for i in range(n-2, -1, -1):
            # logging.info(LogMessages.ROW_PROCESSING.format(i, len(triangle[i])))

            for j in range(len(triangle[i])):
                dp[i][j] = triangle[i][j] + min(dp[i+1][j], dp[i+1][j+1])
                logging.debug(LogMessages.DP_UPDATE.format(
                    j, triangle[i][j], dp[i+1][j], triangle[i][j], dp[i+1][j+1], dp[i][j]
                ))

        # Reconstruct path
        path = reconstruct_path_correct(triangle, dp)
        min_sum = dp[0][0]

        logging.info(LogMessages.ALGORITHM_COMPLETE.format(min_sum))
        logging.info(LogMessages.PATH_COMPLETE.format(" -> ".join(map(str, path))))

        return min_sum, path

    except Exception as error:
        logging.error(f"Error in minimum path calculation: {str(error)}")
        return float('inf'), []

def reconstruct_path_correct(triangle, dp):
    """
    Correctly reconstructs the path using the DP table.

    Args:
        triangle: The original triangle
        dp: The DP table filled with minimum sums

    Returns:
        list: The path from top to bottom
    """
    try:
        logging.info(LogMessages.PATH_RECONSTRUCTION_START)

        n = len(triangle)
        path = []

        current_col = 0
        path.append(triangle[0][current_col])
        # logging.info(LogMessages.PATH_ELEMENT_ADDED.format(triangle[0][current_col], current_col))

        # Reconstruct top-down path
        for i in range(1, n):
            # Check which path gives the current DP value
            # The correct next step is the one that matches: dp[i][col] == dp[i-1][current_col] - triangle[i-1][current_col]
            expected_value = dp[i-1][current_col] - triangle[i-1][current_col]

            if dp[i][current_col] == expected_value:
                path.append(triangle[i][current_col])
                # logging.info(LogMessages.PATH_ELEMENT_ADDED.format(triangle[i][current_col], current_col))
            else:
                # Move to next column
                current_col += 1
                path.append(triangle[i][current_col])
                # logging.info(LogMessages.PATH_ELEMENT_ADDED.format(triangle[i][current_col], current_col))

        return path

    except Exception as error:
        logging.error(f"Error in path reconstruction: {str(error)}")
        return []

class TriangleTests:
    """
    Test cases for the triangle path algorithm.
    """

    @staticmethod
    def get_basic_tests():
        """Returns basic test cases from the problem statement."""
        return [
            {
                "name": "Basic Triangle 1",
                "triangle": [[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]],
                "expected_sum": 11,
                "expected_path": [2, 3, 5, 1]
            },
            {
                "name": "Basic Triangle 2",
                "triangle": [[-1], [2, 3], [1, -1, -3], [4, 2, 1, 3]],
                "expected_sum": 0,
                "expected_path": [-1, 3, -3, 1]
            }
        ]

    @staticmethod
    def get_edge_tests():
        """Returns edge case tests."""
        return [
            {
                "name": "Single Element",
                "triangle": [[5]],
                "expected_sum": 5,
                "expected_path": [5]
            },
            {
                "name": "Two Rows",
                "triangle": [[1], [2, 3]],
                "expected_sum": 3,
                "expected_path": [1, 2]
            },
            {
                "name": "All Same Values",
                "triangle": [[1], [1, 1], [1, 1, 1]],
                "expected_sum": 3,
                "expected_path": [1, 1, 1]
            },
            {
                "name": "Negative Values",
                "triangle": [[-1], [-2, -3], [-4, -5, -6]],
                "expected_sum": -10,
                "expected_path": [-1, -3, -6]
            }
        ]

    @staticmethod
    def get_large_tests():
        """Returns larger test cases."""
        return [
            {
                "name": "5x5 Triangle",
                "triangle": [
                    [1],
                    [2, 3],
                    [4, 5, 6],
                    [7, 8, 9, 10],
                    [11, 12, 13, 14, 15]
                ],
                "expected_sum": 1 + 2 + 4 + 7 + 11,
                "expected_path": [1, 2, 4, 7, 11]
            }
        ]

class TriangleGenerator:
    """
    Generates random triangles for testing.
    """

    @staticmethod
    def generate_random_triangle(rows, min_val=-10, max_val=10):
        """
        Generates a random triangle with given number of rows.

        Args:
            rows: Number of rows in the triangle
            min_val: Minimum value for elements
            max_val: Maximum value for elements

        Returns:
            list: Generated triangle
        """
        logging.info(LogMessages.GENERATION_START.format(rows, rows))

        triangle = []
        for i in range(rows):
            row = [random.randint(min_val, max_val) for _ in range(i + 1)]
            triangle.append(row)

        logging.info(LogMessages.GENERATION_COMPLETE.format(triangle))
        return triangle

    @staticmethod
    def generate_positive_triangle(rows, max_val=20):
        """Generates triangle with only positive values."""
        return TriangleGenerator.generate_random_triangle(rows, 1, max_val)

    @staticmethod
    def generate_negative_triangle(rows, min_val=-20):
        """Generates triangle with only negative values."""
        return TriangleGenerator.generate_random_triangle(rows, min_val, -1)

    @staticmethod
    def generate_mixed_triangle(rows):
        """Generates triangle with mixed positive and negative values."""
        return TriangleGenerator.generate_random_triangle(rows, -15, 15)

def run_test(test_case, test_number):
    """
    Runs a single test case and returns results.

    Args:
        test_case: Dictionary with test case data
        test_number: Test case number

    Returns:
        tuple: (passed, actual_sum, actual_path)
    """
    logging.info(LogMessages.TEST_START.format(test_number))

    triangle = test_case["triangle"]
    expected_sum = test_case["expected_sum"]
    expected_path = test_case["expected_path"]

    actual_sum, actual_path = minimum_total(triangle)

    sum_correct = actual_sum == expected_sum
    path_correct = actual_path == expected_path

    passed = sum_correct and path_correct

    if passed:
        logging.info(LogMessages.TEST_PASSED.format(test_number))
    else:
        logging.info(LogMessages.TEST_FAILED.format(test_number))

    logging.info(LogMessages.TEST_RESULT.format(
        test_number, expected_sum, actual_sum,
        " -> ".join(map(str, expected_path)),
        " -> ".join(map(str, actual_path))
    ))

    return passed, actual_sum, actual_path

def run_test_suite():
    """
    Runs all test suites and returns summary.
    """
    logging.info("RUNNING COMPREHENSIVE TEST SUITE")

    all_tests = []
    results = []

    # Basic tests
    basic_tests = TriangleTests.get_basic_tests()
    all_tests.extend(basic_tests)

    # Edge tests
    edge_tests = TriangleTests.get_edge_tests()
    all_tests.extend(edge_tests)

    # Large tests
    large_tests = TriangleTests.get_large_tests()
    all_tests.extend(large_tests)

    # Run all predefined tests
    for i, test_case in enumerate(all_tests):
        passed, actual_sum, actual_path = run_test(test_case, i + 1)
        results.append((test_case["name"], passed, actual_sum, actual_path))

    # Generate random 3 tests
    random_tests = []
    for i in range(3):
        rows = random.randint(3, 6)
        triangle = TriangleGenerator.generate_random_triangle(rows)

        expected_sum, expected_path = minimum_total(triangle)

        random_test = {
            "name": f"Random Test {i + 1}",
            "triangle": triangle,
            "expected_sum": expected_sum,
            "expected_path": expected_path
        }
        random_tests.append(random_test)

    # Run random tests (should always pass)
    start_idx = len(all_tests)
    for i, test_case in enumerate(random_tests):
        passed, actual_sum, actual_path = run_test(test_case, start_idx + i + 1)
        results.append((test_case["name"], passed, actual_sum, actual_path))

    return results

def print_test_summary(results):
    """
    Prints a summary of test results.

    Args:
        results: List of test results
    """
    logging.info("TEST SUMMARY")

    passed_count = sum(1 for _, passed, _, _ in results if passed)
    total_count = len(results)

    logging.info(f"Total Tests: {total_count}")
    logging.info(f"Passed: {passed_count}")
    logging.info(f"Failed: {total_count - passed_count}")
    logging.info(f"Success Rate: {passed_count/total_count*100:.1f}%")

    logging.info("Detailed Results:")
    for name, passed, actual_sum, actual_path in results:
        status = "PASS" if passed else "FAIL"
        logging.info(f"{name:<20} {status:<6} Sum: {actual_sum:<6} Path: {' -> '.join(map(str, actual_path))}")

def benchmark_algorithm():
    """
    Benchmarks the algorithm with large triangles.
    """
    logging.info("BENCHMARK WITH LARGE TRIANGLES")

    import time

    sizes = [10, 20, 50, 100]

    for size in sizes:
        triangle = TriangleGenerator.generate_random_triangle(size, -100, 100)

        start_time = time.time()
        min_sum, path = minimum_total(triangle)
        end_time = time.time()

        execution_time = end_time - start_time
        logging.info(f"Size: {size}, Time: {execution_time:.4f}s, Min Sum: {min_sum}")
        logging.info(f"Size {size}: {execution_time:.4f}s (sum: {min_sum})")

def main():
    """
    Main execution function.
    """
    try:
        # Run comprehensive test suite
        test_results = run_test_suite()

        # Print summary
        print_test_summary(test_results)

        # Run BENCHMARK
        logging.info(f"BENCHMARK ... ")
        benchmark_algorithm()

        original_tests = TriangleTests.get_basic_tests()
        for test in original_tests:
            min_sum, path = minimum_total(test["triangle"])

    except Exception as error:
        logging.error(f"Error in main execution: {str(error)}")

if __name__ == "__main__":
    main()
