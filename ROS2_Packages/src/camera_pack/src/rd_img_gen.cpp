#include <iostream>
#include <cstdio>
#include <memory>
#include <stdexcept>
#include <string>
#include <array>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class ProcessPublisher : public rclcpp::Node
{
public:
    ProcessPublisher() : Node("process_publisher"), previous_value_("") {
        publisher_ = this->create_publisher<std_msgs::msg::String>("Cam_Detections", 10);

        // Launch the PR executable and read its output
        std::array<char, 128> buffer;
        std::string result;
        FILE *pipe = popen("./NanoImg", "r");
        if (!pipe) {
            throw std::runtime_error("Failed to open pipe for PR executable");
        }
        while (!feof(pipe)) {
            if (fgets(buffer.data(), 128, pipe) != nullptr) {
                result = buffer.data();
                // Assuming the output format of NanoDet is: [ID, x, y, x_size, y_size]
                // Parse the output and publish it in the desired format
                publish_message(parse_output(result));
            }
        }
        pclose(pipe);
    }

private:
    std::string parse_output(const std::string &output) {
        // Parse the output string and return in the desired format
        // Assuming the output format of NanoDet is: [ID, x, y, x_size, y_size]
        // You may need to adjust this parsing according to the actual output format
        return output;
    }

    void publish_message(const std::string &msg) {
        auto message = std_msgs::msg::String();
        message.data = msg;
        RCLCPP_INFO(this->get_logger(), "%s", message.data.c_str());
        publisher_->publish(message);
    }

    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    std::string previous_value_;
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ProcessPublisher>());
    rclcpp::shutdown();
    return 0;
}

