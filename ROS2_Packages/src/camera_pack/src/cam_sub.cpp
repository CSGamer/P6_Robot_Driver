#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include <iostream>
#include <vector>
#include <sstream>
#include <regex>

using std::placeholders::_1;

class ObjectSubscriber : public rclcpp::Node
{
public:
    ObjectSubscriber() : Node("cam_subscriber")
    {
        subscription_ = this->create_subscription<std_msgs::msg::String>(
            "Cam_Detections", 10, std::bind(&ObjectSubscriber::topic_callback, this, _1));
    }

private:
    void topic_callback(const std_msgs::msg::String::SharedPtr msg) const
    {
    	std::vector<float> values;
    	
    	// Regular expression to match a sequence of floating-point numbers
        std::regex pattern("-?\\d+(?:\\.\\d+)?");

        // Convert the std::string to a C-style string
        const char* cstr = msg->data.c_str();

        std::cmatch matches;
        const char* start = cstr;

        // Extract floating-point numbers from the message using regular expression
        while (std::regex_search(start, cstr + msg->data.size(), matches, pattern))
        {
            std::string match = matches.str();
            float value = std::stof(match);
            values.push_back(value);
            start = matches[0].second;
        }

        if (values.size() != 6)
        {
            RCLCPP_ERROR(this->get_logger(), "Invalid message format: '%s'. Expected 5 values, received %d.", msg->data.c_str(), values.size());
            return;
        }

        int id = static_cast<int>(values[0]);
        float x = values[1];
        float y = values[2];
        float x_size = values[3];
        float y_size = values[4];
        float fps = values[5];

        RCLCPP_INFO(this->get_logger(), "Received Object: [ID: %d, x: %.2f, y: %.2f, x_size: %.2f, y_size: %.2f, FPS: %.2f]",
                    id, x, y, x_size, y_size,fps);
    }

    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ObjectSubscriber>());
    rclcpp::shutdown();
    return 0;
}

