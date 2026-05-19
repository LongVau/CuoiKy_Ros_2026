import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_dir = get_package_share_directory('cartographer_2d')
    config_dir = os.path.join(pkg_dir, 'config')

    return LaunchDescription([
        # Node chính của Cartographer
        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer_node',
            output='screen',
            parameters=[{'use_sim_time': True}], # Chuyển thành False nếu chạy robot thật
            arguments=[
                '-configuration_directory', config_dir,
                '-configuration_basename', 'cartographer_2d.lua'
            ],
            remappings=[
                ('/scan', '/scan') # Thay đổi nếu topic lidar của bạn khác tên
            ]
        ),
        
        # Node chuyển đổi dữ liệu map sang dạng OccupancyGrid để hiển thị trên RViz
        Node(
            package='cartographer_ros',
            executable='cartographer_occupancy_grid_node',
            name='cartographer_occupancy_grid_node',
            output='screen',
            parameters=[{'use_sim_time': True}],
            arguments=['-resolution', '0.05', '-publish_period_sec', '1.0']
        ),
    ])
