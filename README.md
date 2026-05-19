# CuoiKy_Ros_2026

## Gmapping

```bash
colcon build
source install/setup.bash
```

### Chạy launch

```bash
# Cho map của Turtlebot3
ros2 launch xe_ros cuoiky.launch.py

# Cho map trống
ros2 launch xe_ros gmap.launch.py
```

### Trong RViz

- Add -> By Topic -> map
- Đổi Fixed Frame thành `map`

---

## Cartographer

### Tải các package cần thiết

```bash
sudo apt update
sudo apt install ros-humble-cartographer ros-humble-cartographer-ros
```

### Chạy chương trình

#### Terminal 1

```bash
ros2 launch xe_ros gazebo.launch.py
```

#### Terminal 2

```bash
ros2 launch cartographer_2d cartographer.launch.py
```

### Trong RViz

- Add -> By Topic -> map
- Đổi Fixed Frame thành `map`

---

## RTAB-Map

### Tải các package cần thiết

```bash
sudo apt install ros-humble-rtabmap-ros
```

### Chạy chương trình

#### Terminal 1

```bash
ros2 launch xe_ros gazebo.launch.py
```

#### Terminal 2

```bash
ros2 launch rtabmap_launch rtabmap.launch.py \
use_sim_time:=true \
rtabmap_args:="--delete_db_on_start" \
rgb_topic:=/camera/cam/image_raw \
depth_topic:=/camera/cam/depth/image_raw \
camera_info_topic:=/camera/cam/depth/camera_info \
frame_id:=base_link \
approx_sync:=true \
visual_odometry:=false \
odom_topic:=/odom \
qos:=2 \
rviz:=false \
rtabmap_viz:=false
```

### Trong RViz

- Add -> By Topic -> map
- Add -> By Topic -> /rtabmap/cloud_map -> PointCloud2
- Đổi Fixed Frame thành `map`
## Chạy robot bằng teleop_twist
Mở một terminal mới
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
## Lưu ý
Trường hợp Gazebo không thể tìm thấy file mesh (.STL), ta phải chỉ đường cho nó (thay đổi thành đường dẫn tương ứng)
```bash
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/humble_ws/install/xe_ros/share
```
