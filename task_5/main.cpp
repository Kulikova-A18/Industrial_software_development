#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
#include <limits>
#include <random>
#include <chrono>
#include <fstream>
#include <memory>

class Logger {
private:
    std::ofstream file_stream;
    bool log_to_file;
    
public:
    Logger(bool to_file = true) : log_to_file(to_file) {
        if (log_to_file) {
            file_stream.open("triangle_path.log", std::ios::out);
        }
    }
    
    ~Logger() {
        if (file_stream.is_open()) {
            file_stream.close();
        }
    }
    
    void info(const std::string& message) {
        log("INFO", message);
    }
    
    void warning(const std::string& message) {
        log("WARNING", message);
    }
    
    void error(const std::string& message) {
        log("ERROR", message);
    }
    
    void debug(const std::string& message) {
        log("DEBUG", message);
    }
    
private:
    void log(const std::string& level, const std::string& message) {
        auto now = std::chrono::system_clock::now();
        auto time_t = std::chrono::system_clock::to_time_t(now);
        
        std::stringstream ss;
        ss << std::ctime(&time_t);
        std::string time_str = ss.str();
        time_str.pop_back();
        
        std::string log_message = time_str + " - " + level + " - " + message;
        
        std::cout << log_message << std::endl;
        if (log_to_file && file_stream.is_open()) {
            file_stream << log_message << std::endl;
        }
    }
};

struct LogMessages {
    static const std::string ALGORITHM_START;
    static const std::string ALGORITHM_COMPLETE;
    static const std::string ALGORITHM_EMPTY_INPUT;
    static const std::string TRIANGLE_SIZE;
    static const std::string ROW_PROCESSING;
    static const std::string DP_INITIALIZATION;
    static const std::string DP_UPDATE;
    static const std::string PATH_RECONSTRUCTION_START;
    static const std::string PATH_ELEMENT_ADDED;
    static const std::string PATH_COMPLETE;
    static const std::string TEST_START;
    static const std::string TEST_RESULT;
    static const std::string TEST_PASSED;
    static const std::string TEST_FAILED;
    static const std::string GENERATION_START;
    static const std::string GENERATION_COMPLETE;
};

const std::string LogMessages::ALGORITHM_START = "Starting minimum path sum calculation for triangle";
const std::string LogMessages::ALGORITHM_COMPLETE = "Algorithm complete. Minimum path sum: ";
const std::string LogMessages::ALGORITHM_EMPTY_INPUT = "Empty triangle provided";
const std::string LogMessages::TRIANGLE_SIZE = "Processing triangle with ";
const std::string LogMessages::ROW_PROCESSING = "Processing row ";
const std::string LogMessages::DP_INITIALIZATION = "Initializing DP with base row: ";
const std::string LogMessages::DP_UPDATE = "Updating dp[";
const std::string LogMessages::PATH_RECONSTRUCTION_START = "Starting path reconstruction";
const std::string LogMessages::PATH_ELEMENT_ADDED = "Added element ";
const std::string LogMessages::PATH_COMPLETE = "Minimum path: ";
const std::string LogMessages::TEST_START = "Starting test case ";
const std::string LogMessages::TEST_RESULT = "Test ";
const std::string LogMessages::TEST_PASSED = "Test PASSED";
const std::string LogMessages::TEST_FAILED = "Test FAILED";
const std::string LogMessages::GENERATION_START = "Generating random test case ";
const std::string LogMessages::GENERATION_COMPLETE = "Generated triangle: ";

std::string vectorToString(const std::vector<int>& vec) {
    std::stringstream ss;
    ss << "[";
    for (size_t i = 0; i < vec.size(); ++i) {
        ss << vec[i];
        if (i < vec.size() - 1) ss << ", ";
    }
    ss << "]";
    return ss.str();
}

std::string triangleToString(const std::vector<std::vector<int>>& triangle) {
    std::stringstream ss;
    ss << "[";
    for (size_t i = 0; i < triangle.size(); ++i) {
        ss << "[";
        for (size_t j = 0; j < triangle[i].size(); ++j) {
            ss << triangle[i][j];
            if (j < triangle[i].size() - 1) ss << ", ";
        }
        ss << "]";
        if (i < triangle.size() - 1) ss << ", ";
    }
    ss << "]";
    return ss.str();
}

std::string pathToString(const std::vector<int>& path) {
    std::stringstream ss;
    for (size_t i = 0; i < path.size(); ++i) {
        ss << path[i];
        if (i < path.size() - 1) ss << " -> ";
    }
    return ss.str();
}

std::pair<int, std::vector<int>> minimum_total(const std::vector<std::vector<int>>& triangle, Logger& logger) {
    try {
        logger.info(LogMessages::ALGORITHM_START);

        if (triangle.empty() || triangle[0].empty()) {
            logger.warning(LogMessages::ALGORITHM_EMPTY_INPUT);
            return {0, {}};
        }

        int n = triangle.size();
        logger.info(LogMessages::TRIANGLE_SIZE + std::to_string(n) + " rows");

        
        std::vector<std::vector<int>> dp(n);
        for (int i = 0; i < n; ++i) {
            dp[i].resize(triangle[i].size());
        }

        for (size_t j = 0; j < triangle[n-1].size(); ++j) {
            dp[n-1][j] = triangle[n-1][j];
        }

        logger.info(LogMessages::DP_INITIALIZATION + vectorToString(dp[n-1]));

        for (int i = n-2; i >= 0; --i) {
            for (size_t j = 0; j < triangle[i].size(); ++j) {
                dp[i][j] = triangle[i][j] + std::min(dp[i+1][j], dp[i+1][j+1]);
                
                std::string debug_msg = LogMessages::DP_UPDATE + 
                    std::to_string(j) + "] = min(" + 
                    std::to_string(triangle[i][j]) + " + " + std::to_string(dp[i+1][j]) + ", " +
                    std::to_string(triangle[i][j]) + " + " + std::to_string(dp[i+1][j+1]) + ") = " +
                    std::to_string(dp[i][j]);
                logger.debug(debug_msg);
            }
        }

        logger.info(LogMessages::PATH_RECONSTRUCTION_START);
        std::vector<int> path;
        int current_col = 0;
        path.push_back(triangle[0][current_col]);

        for (int i = 1; i < n; ++i) {
            int expected_value = dp[i-1][current_col] - triangle[i-1][current_col];
            
            if (dp[i][current_col] == expected_value) {
                path.push_back(triangle[i][current_col]);
            } else {
                current_col += 1;
                path.push_back(triangle[i][current_col]);
            }
        }

        int min_sum = dp[0][0];
        logger.info(LogMessages::ALGORITHM_COMPLETE + std::to_string(min_sum));
        logger.info(LogMessages::PATH_COMPLETE + pathToString(path));

        return {min_sum, path};

    } catch (const std::exception& error) {
        logger.error("Error in minimum path calculation: " + std::string(error.what()));
        return {std::numeric_limits<int>::max(), {}};
    }
}

class TriangleGenerator {
private:
    std::random_device rd;
    std::mt19937 gen;
    
public:
    TriangleGenerator() : gen(rd()) {}
    
    std::vector<std::vector<int>> generate_random_triangle(int rows, int min_val = -10, int max_val = 10) {
        Logger logger(false);
        logger.info(LogMessages::GENERATION_START + std::to_string(rows) + " with " + std::to_string(rows) + " rows");
        
        std::vector<std::vector<int>> triangle;
        std::uniform_int_distribution<int> dis(min_val, max_val);
        
        for (int i = 0; i < rows; ++i) {
            std::vector<int> row;
            for (int j = 0; j <= i; ++j) {
                row.push_back(dis(gen));
            }
            triangle.push_back(row);
        }
        
        logger.info(LogMessages::GENERATION_COMPLETE + triangleToString(triangle));
        return triangle;
    }
};

struct TestCase {
    std::string name;
    std::vector<std::vector<int>> triangle;
    int expected_sum;
    std::vector<int> expected_path;
};

class TriangleTests {
public:
    static std::vector<TestCase> get_basic_tests() {
        return {
            {"Basic Triangle 1", {{2}, {3, 4}, {6, 5, 7}, {4, 1, 8, 3}}, 11, {2, 3, 5, 1}},
            {"Basic Triangle 2", {{-1}, {2, 3}, {1, -1, -3}, {4, 2, 1, 3}}, 0, {-1, 3, -3, 1}}
        };
    }
    
    static std::vector<TestCase> get_edge_tests() {
        return {
            {"Single Element", {{5}}, 5, {5}},
            {"Two Rows", {{1}, {2, 3}}, 3, {1, 2}},
            {"All Same Values", {{1}, {1, 1}, {1, 1, 1}}, 3, {1, 1, 1}},
            {"Negative Values", {{-1}, {-2, -3}, {-4, -5, -6}}, -10, {-1, -3, -6}}
        };
    }
    
    static std::vector<TestCase> get_large_tests() {
        return {
            {"5x5 Triangle", {{1}, {2, 3}, {4, 5, 6}, {7, 8, 9, 10}, {11, 12, 13, 14, 15}}, 
             1 + 2 + 4 + 7 + 11, {1, 2, 4, 7, 11}}
        };
    }
};

struct TestResult {
    std::string name;
    bool passed;
    int actual_sum;
    std::vector<int> actual_path;
};

TestResult run_test(const TestCase& test_case, int test_number, Logger& logger) {
    logger.info(LogMessages::TEST_START + std::to_string(test_number));
    
    auto [actual_sum, actual_path] = minimum_total(test_case.triangle, logger);
    
    bool sum_correct = (actual_sum == test_case.expected_sum);
    bool path_correct = (actual_path == test_case.expected_path);
    bool passed = sum_correct && path_correct;
    
    if (passed) {
        logger.info(LogMessages::TEST_PASSED);
    } else {
        logger.info(LogMessages::TEST_FAILED);
    }
    
    std::string result_msg = LogMessages::TEST_RESULT + 
        std::to_string(test_number) + ": Expected sum = " + std::to_string(test_case.expected_sum) +
        ", Got = " + std::to_string(actual_sum) + " | Expected path = " + 
        pathToString(test_case.expected_path) + ", Got = " + pathToString(actual_path);
    logger.info(result_msg);
    
    return {test_case.name, passed, actual_sum, actual_path};
}

std::vector<TestResult> run_test_suite(Logger& logger) {
    logger.info("RUNNING COMPREHENSIVE TEST SUITE");
    
    std::vector<TestResult> results;
    std::vector<TestCase> all_tests;
    
    auto basic_tests = TriangleTests::get_basic_tests();
    all_tests.insert(all_tests.end(), basic_tests.begin(), basic_tests.end());
    
    auto edge_tests = TriangleTests::get_edge_tests();
    all_tests.insert(all_tests.end(), edge_tests.begin(), edge_tests.end());
    
    auto large_tests = TriangleTests::get_large_tests();
    all_tests.insert(all_tests.end(), large_tests.begin(), large_tests.end());
    
    for (size_t i = 0; i < all_tests.size(); ++i) {
        results.push_back(run_test(all_tests[i], i + 1, logger));
    }
    
    TriangleGenerator generator;
    for (int i = 0; i < 3; ++i) {
        int rows = 3 + (i * 2); // 3, 5, 7 rows
        auto triangle = generator.generate_random_triangle(rows);
        
        auto [expected_sum, expected_path] = minimum_total(triangle, logger);
        
        TestCase random_test = {
            "Random Test " + std::to_string(i + 1),
            triangle,
            expected_sum,
            expected_path
        };
        
        results.push_back(run_test(random_test, all_tests.size() + i + 1, logger));
    }
    
    return results;
}

void print_test_summary(const std::vector<TestResult>& results, Logger& logger) {
    logger.info("TEST SUMMARY");
    
    int passed_count = 0;
    for (const auto& result : results) {
        if (result.passed) passed_count++;
    }
    
    int total_count = results.size();
    
    logger.info("Total Tests: " + std::to_string(total_count));
    logger.info("Passed: " + std::to_string(passed_count));
    logger.info("Failed: " + std::to_string(total_count - passed_count));
    logger.info("Success Rate: " + std::to_string(static_cast<double>(passed_count) / total_count * 100) + "%");
    
    logger.info("Detailed Results:");
    for (const auto& result : results) {
        std::string status = result.passed ? "PASS" : "FAIL";
        logger.info(result.name + " " + status + " Sum: " + std::to_string(result.actual_sum) + 
                   " Path: " + pathToString(result.actual_path));
    }
}

void benchmark_algorithm(Logger& logger) {
    logger.info("BENCHMARK WITH LARGE TRIANGLES");
    
    TriangleGenerator generator;
    std::vector<int> sizes = {10, 20, 50, 100};
    
    for (int size : sizes) {
        auto triangle = generator.generate_random_triangle(size, -100, 100);
        
        auto start = std::chrono::high_resolution_clock::now();
        auto [min_sum, path] = minimum_total(triangle, logger);
        auto end = std::chrono::high_resolution_clock::now();
        
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        double execution_time = duration.count() / 1000000.0;
        
        logger.info("Size: " + std::to_string(size) + ", Time: " + 
                   std::to_string(execution_time) + "s, Min Sum: " + std::to_string(min_sum));
    }
}

int main() {
    try {
        Logger logger;
        
        auto test_results = run_test_suite(logger);
        
        print_test_summary(test_results, logger);
        
        logger.info("BENCHMARK ... ");
        benchmark_algorithm(logger);
        
        auto original_tests = TriangleTests::get_basic_tests();
        for (const auto& test : original_tests) {
            auto [min_sum, path] = minimum_total(test.triangle, logger);
        }
        
    } catch (const std::exception& error) {
        std::cerr << "Error in main execution: " << error.what() << std::endl;
        return 1;
    }
    
    return 0;
}
