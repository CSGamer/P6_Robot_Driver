#include <cstdio>
#include <cstdlib> // For system()
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class HelloWorldNode : public rclcpp::Node
{
public:
  HelloWorldNode() : Node("hello_world_node")
  {
    publisher_ = this->create_publisher<std_msgs::msg::String>("hello_world_topic", 10);
    timer_ = this->create_wall_timer(std::chrono::seconds(1), std::bind(&HelloWorldNode::publishMessage, this));
  }

private:
  void publishMessage()
  {
    auto msg = std_msgs::msg::String();
    msg.data = "hello world bones package";
    RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", msg.data.c_str());
    publisher_->publish(msg);
  }

  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<HelloWorldNode>();

  // Run NanoDet executable
  system("./NanoDet &");

  rclcpp::executors::MultiThreadedExecutor executor;
  executor.add_node(node);
  executor.spin();

  rclcpp::shutdown();
  return 0;
}

