#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <string>
#include <sstream>
#include <utility>
#include <stdexcept>
#include <chrono>
#include <iomanip>

class Logger {
private:
    std::ofstream log_file;
    bool debug_enabled;

public:
    Logger(const std::string& filename = "task.log", bool debug = false) 
        : debug_enabled(debug) {
        log_file.open(filename);
        if (!log_file.is_open()) {
            throw std::runtime_error("Cannot open log file: " + filename);
        }
    }

    ~Logger() {
        if (log_file.is_open()) {
            log_file.close();
        }
    }

    void info(const std::string& message) {
        std::string timestamp = get_current_timestamp();
        std::string log_message = timestamp + " - INFO - " + message;
        std::cout << log_message << std::endl;
        log_file << log_message << std::endl;
    }

    void debug(const std::string& message) {
        if (debug_enabled) {
            std::string timestamp = get_current_timestamp();
            std::string log_message = timestamp + " - DEBUG - " + message;
            std::cout << log_message << std::endl;
            log_file << log_message << std::endl;
        }
    }

    void warning(const std::string& message) {
        std::string timestamp = get_current_timestamp();
        std::string log_message = timestamp + " - WARNING - " + message;
        std::cout << log_message << std::endl;
        log_file << log_message << std::endl;
    }

    void error(const std::string& message) {
        std::string timestamp = get_current_timestamp();
        std::string log_message = timestamp + " - ERROR - " + message;
        std::cerr << log_message << std::endl;
        log_file << log_message << std::endl;
    }

private:
    std::string get_current_timestamp() {
        auto now = std::chrono::system_clock::now();
        auto time_t = std::chrono::system_clock::to_time_t(now);
        auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(
            now.time_since_epoch()) % 1000;
        
        std::stringstream ss;
        ss << std::put_time(std::localtime(&time_t), "%Y-%m-%d %H:%M:%S");
        ss << "." << std::setfill('0') << std::setw(3) << ms.count();
        return ss.str();
    }
};

class SegmentProcessor {
private:
    Logger& logger;

public:
    SegmentProcessor(Logger& log) : logger(log) {}

    std::pair<int, std::vector<int>> find_minimum_points_to_cover_all_segments(
        const std::vector<std::pair<int, int>>& segments) {
        
        logger.info("Starting minimum points calculation for segment coverage");
        
        int segment_count = segments.size();
        logger.info("Processing " + std::to_string(segment_count) + " segments");
        
        if (segment_count == 0) {
            logger.warning("Empty segments list provided");
            return {0, {}};
        }

        logger.info("Validating segments data");
        for (size_t i = 0; i < segments.size(); ++i) {
            const auto& segment = segments[i];
            if (segment.first > segment.second) {
                std::string error_msg = "Segment " + std::to_string(i) + 
                    " has start > end: (" + std::to_string(segment.first) + 
                    ", " + std::to_string(segment.second) + ")";
                logger.error(error_msg);
                throw std::invalid_argument(error_msg);
            }
        }
        logger.info("Segments validation completed successfully");

        // Sort segments by right endpoint
        logger.info("Sorting segments by right endpoint");
        std::vector<std::pair<int, int>> sorted_segments = segments;
        std::sort(sorted_segments.begin(), sorted_segments.end(),
            [](const std::pair<int, int>& a, const std::pair<int, int>& b) {
                return a.second < b.second;
            });
        logger.info("Segments sorted successfully");

        std::vector<int> selected_points;
        int current_covering_point = -1;
        int segments_processed = 0;
        int points_selected = 0;

        logger.info("Starting point selection process");

        for (const auto& segment : sorted_segments) {
            segments_processed++;
            int segment_start = segment.first;
            int segment_end = segment.second;

            logger.info("Processing segment " + std::to_string(segments_processed) + 
                       ": (" + std::to_string(segment_start) + ", " + 
                       std::to_string(segment_end) + ")");

            if (current_covering_point == -1 || current_covering_point < segment_start) {
                current_covering_point = segment_end;
                selected_points.push_back(current_covering_point);
                points_selected++;

                logger.info("Selected new point: " + std::to_string(current_covering_point) + 
                           " for segment (" + std::to_string(segment_start) + ", " + 
                           std::to_string(segment_end) + ")");

                if (points_selected == 1) {
                    logger.info("Initial point selected: " + std::to_string(current_covering_point));
                } else {
                    logger.info("Additional point selected: " + std::to_string(current_covering_point) + 
                               " (total: " + std::to_string(points_selected) + " points)");
                }
            } else {
                logger.info("Current point " + std::to_string(current_covering_point) + 
                           " covers segment (" + std::to_string(segment_start) + ", " + 
                           std::to_string(segment_end) + ")");
            }
        }

        int total_points_required = selected_points.size();
        logger.info("Point selection completed. Selected " + 
                   std::to_string(total_points_required) + " points");
        logger.info("Calculation complete. Required " + 
                   std::to_string(total_points_required) + " points");

        // Statistics
        logger.info("Algorithm statistics:");
        logger.info("Total segments processed: " + std::to_string(segments_processed));
        logger.info("Points selected: " + std::to_string(total_points_required));
        if (total_points_required > 0) {
            double coverage_ratio = static_cast<double>(segments_processed) / total_points_required;
            logger.info("Coverage efficiency: " + std::to_string(coverage_ratio) + " segments per point");
        }

        return {total_points_required, selected_points};
    }
};

class FileReader {
private:
    Logger& logger;

public:
    FileReader(Logger& log) : logger(log) {}

    std::vector<std::pair<int, int>> read_segments_from_file(const std::string& filename) {
        logger.info("Attempting to read segments data from file: " + filename);
        
        std::ifstream file(filename);
        if (!file.is_open()) {
            logger.error("Input file not found: " + filename);
            throw std::runtime_error("File not found: " + filename);
        }

        std::string first_line;
        if (!std::getline(file, first_line)) {
            logger.error("Input file is empty");
            throw std::runtime_error("Empty file");
        }

        // Parse first line
        std::stringstream first_ss(first_line);
        int total_segments_count;
        if (!(first_ss >> total_segments_count)) {
            logger.error("Invalid segment count format: " + first_line);
            throw std::runtime_error("Invalid format");
        }

        logger.info("File header indicates " + std::to_string(total_segments_count) + 
                   " segments to read");

        std::vector<std::pair<int, int>> segments_data;
        int lines_read = 0;
        int segments_read = 0;
        int lines_skipped = 0;
        std::string line;

        while (std::getline(file, line) && segments_read < total_segments_count) {
            lines_read++;
            
            if (line.empty()) {
                lines_skipped++;
                logger.debug("Skipped empty line at position " + std::to_string(lines_read));
                continue;
            }

            std::stringstream line_ss(line);
            int start, end;
            
            if (!(line_ss >> start >> end)) {
                logger.error("Invalid segment data at line " + std::to_string(lines_read) + 
                            ": " + line);
                throw std::runtime_error("Invalid segment data");
            }

            // start <= end
            int actual_start = std::min(start, end);
            int actual_end = std::max(start, end);
            
            segments_data.emplace_back(actual_start, actual_end);
            segments_read++;
        }

        if (segments_read < total_segments_count) {
            logger.error("Unexpected end of file at line " + std::to_string(lines_read + 1));
            throw std::runtime_error("Unexpected end of file");
        }

        logger.info("Successfully read " + std::to_string(segments_data.size()) + 
                   " segments from file");
        
        logger.info("File reading statistics:");
        logger.info("Expected segments: " + std::to_string(total_segments_count));
        logger.info("Actual segments read: " + std::to_string(segments_read));
        logger.info("Lines processed: " + std::to_string(lines_read));
        logger.info("Empty lines skipped: " + std::to_string(lines_skipped));

        if (segments_data.size() != total_segments_count) {
            logger.warning("Segment count mismatch: expected " + 
                          std::to_string(total_segments_count) + ", got " + 
                          std::to_string(segments_data.size()));
        }

        return segments_data;
    }
};

class ProcessingPipeline {
private:
    Logger& logger;
    FileReader file_reader;
    SegmentProcessor segment_processor;

public:
    ProcessingPipeline(Logger& log) 
        : logger(log), file_reader(log), segment_processor(log) {}

    std::pair<int, std::vector<int>> execute() {
        logger.info("Starting segment coverage processing pipeline");
        
        std::string input_filename = "data_prog_contest_problem_1.txt";
        logger.info("Reading data from: " + input_filename);

        try {
            auto segments = file_reader.read_segments_from_file(input_filename);
            
            logger.info("Starting main calculation for contest data");
            auto result = segment_processor.find_minimum_points_to_cover_all_segments(segments);
            
            logger.info("PROCESSING RESULTS");
            logger.info("Total segments processed: " + std::to_string(segments.size()));
            logger.info("Minimum points required: " + std::to_string(result.first));
            
            std::string points_str = "[";
            for (size_t i = 0; i < result.second.size(); ++i) {
                if (i > 0) points_str += ", ";
                points_str += std::to_string(result.second[i]);
            }
            points_str += "]";
            logger.info("Optimal point locations: " + points_str);

            if (result.first > 0) {
                double coverage_ratio = static_cast<double>(segments.size()) / result.first;
                logger.info("Coverage ratio: " + std::to_string(coverage_ratio) + " segments per point");
                int optimization = segments.size() - result.first;
                logger.info("Optimization achieved: " + std::to_string(optimization) + 
                           " fewer points than segments");
            }

            logger.info("Processing pipeline completed successfully");
            return result;

        } catch (const std::exception& e) {
            logger.error("Processing pipeline failed: " + std::string(e.what()));
            return {-1, {}};
        }
    }
};

int main() {
    try {
        Logger logger("task.log", false);
        ProcessingPipeline pipeline(logger);
        
        auto result = pipeline.execute();
        
        if (result.first != -1) {
            logger.info("Final result: " + std::to_string(result.first) + " points");
            for (size_t i = 0; i < result.second.size(); ++i) {
                if (i > 0) std::cout << ", ";
            }
        } else {
            logger.error("Processing failed. Check log for details" + std::string(e.what()));
        }

    } catch (const std::exception& e) {
        logger.error("Critical error in main execution" + std::string(e.what()));
        return 1;
    }

    return 0;
}
