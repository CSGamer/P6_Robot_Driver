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
    ProcessPublisher() : Node("process_publisher"), previous_value_("")
    {
        publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);

        // Launch the PR executable and read its output
        std::array<char, 128> buffer;
        std::string result;
        FILE *pipe = popen("./NanoDet", "r");
        if (!pipe)
        {
            throw std::runtime_error("Failed to open pipe for PR executable");
        }
        while (!feof(pipe))
        {
            if (fgets(buffer.data(), 128, pipe) != nullptr)
            {
                result = buffer.data();
                // Check if the new value is different from the previous one
                if (result != previous_value_) {
                    publish_message(result);
                    previous_value_ = result;
                }
            }
        }
        pclose(pipe);
    }

private:
    void publish_message(const std::string &msg)
    {
        auto message = std_msgs::msg::String();
        message.data = msg;
        RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
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


/*

#include <cstdio>
#include <cstdlib> // For system()
#include <string>
#include <iostream>

using namespace std;

int main(int argc, char ** argv)
{
  (void) argc;
  (void) argv;

      system("./PR &");
      while (1){
        string input;
        getline(std::cin, input);

        std::cout << "check: " << input << std::endl;
    }
    return 0;
}*/
