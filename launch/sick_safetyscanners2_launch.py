import os

from launch import LaunchDescription
from launch_ros.actions import Node
from ppmt_nav_common import common_utils

def generate_launch_description():
    ld = LaunchDescription()
    package_dir = get_package_share_directory("robot_params")

    sick_params_yaml_file = os.path.join(package_dir, "config", "sick_lidar_params.yaml")

    #read yaml file
    sick_params = common_utils.read_yaml_file(sick_params_yaml_file)
    sick_lidar_params = sick_params["SickSafetyscannersRos2"]["ros__parameters"]

    for sick_plugin in sick_lidar_params["sick_lidar_plugins"]:
        sick_node = Node(
                package="sick_safetyscanners2",
                executable="sick_safetyscanners2_node",
                name=sick_plugin + "_sick_safetyscanners2_node",
                output="screen",
                namespace=common_utils.get_robot_name(),
                emulate_tty=True,
                remappings=[("scan",sick_lidar_params[sick_plugin]["topic"])],
                parameters=[sick_lidar_params[sick_plugin]]
            )
        ld.add_action(sick_node)
    
    return ld