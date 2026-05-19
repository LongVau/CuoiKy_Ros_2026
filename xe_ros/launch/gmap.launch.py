import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_xe_ros = get_package_share_directory('xe_ros')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    # Lấy đường dẫn gói mô phỏng của TurtleBot 3 để truy cập file world gốc


    # Định nghĩa đường dẫn trực tiếp đến file môi trường hình học (.world) của TurtleBot 3
    # Lệnh này bỏ qua file launch tự spawn robot của họ

    # 1. Khởi động Gazebo Server và Client với file world được chỉ định
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        ),
    )

    # 2. Node Static Transform (footprint -> link)
    tf_footprint_base = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='tf_footprint_base',
        arguments=[
            '--x', '0', '--y', '0', '--z', '0',
            '--roll', '0', '--pitch', '0', '--yaw', '0',
            '--frame-id', 'base_footprint', '--child-frame-id', 'base_link'
        ],
        parameters=[{'use_sim_time': True}]
    )

    # Đọc nội dung file URDF của robot của bạn
    urdf_file_path = os.path.join(pkg_xe_ros, 'urdf', 'xe_ros.urdf')
    with open(urdf_file_path, 'r') as infp:
        robot_desc = infp.read()
    
    rviz_config_path = os.path.join(pkg_xe_ros, 'rviz', 'xe_ros.rviz')

    # 3. Node Robot State Publisher
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': True 
        }]
    )

    # 4. Spawn mô hình robot riêng của bạn (xe_ros) vào vị trí trung tâm sa bàn
    spawn_model = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_model',
        output='screen',
        arguments=['-entity', 'xe_ros', '-topic', 'robot_description', '-x', '0.5', '-y', '0.5', '-z', '1.0']
    )
    # 5. Khởi chạy thuật toán Gmapping (Mã nguồn từ repo Project-MANAS)
    gmapping_node = Node(
        package='slam_gmapping',
        executable='slam_gmapping',
        name='slam_gmapping',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'particles': 15,                
            'map_update_interval': 5.0,     
            'base_frame': 'base_footprint', 
            'odom_frame': 'odom',           
            'map_frame': 'map',
            'maxUrange': 8.0                
        }],
        remappings=[('/scan', '/scan')]    
    )
    # 6. Kích hoạt Controller Manager và nạp các controller của robot
    load_joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    load_arm_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["arm_controller"],
    )

    # 7. Khởi chạy giao diện hiển thị RViz2
    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        tf_footprint_base,
        node_robot_state_publisher,
        spawn_model,
        #gmapping_node,
        load_joint_state_broadcaster,
        load_arm_controller,
        rviz2
    ])