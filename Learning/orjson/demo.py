# import orjson
# import pandas as pd
#
# df = pd.read_csv("flipkart_404_links.csv")
#
# with open("gaurav_bhai.json", "r") as f:
#     json_data = orjson.loads(f.read())
#
# for url in df['purchase_url']:
#     json_data['product_url'] = url
#     json_data['error'] = True
#
# with open("updated_json.json","w") as file:
#     file.write(orjson.dumps(json_data))


import orjson
import pandas as pd

df = pd.read_csv("flipkart_404_links.csv")

with open("gaurav_bhai.json", "r") as f:
    json_data = orjson.loads(f.read())

# Create a list of modified entries
updated_data = []
for url in df['purchase_url']:
    item = json_data.copy()
    column_list = ['product_name', 'product_id', 'scrap_date_and_time', 'image_urls', 'category_hierarchy',
                   'number_of_ratings',
                   'avg_rating', 'individual_ratings_count', 'brand', 'description', 'product_description',
                   'product_url',
                   'requested_url', 'mrp', 'selling_price', 'discount', 'in_stock_out_of_stock_status', 'size_chart',
                   'seller_details', 'reviews', 'variant_level', 'similar_product', 'product_specification',
                   'product_detail',
                   'total_number_of_requests', 'color_list', 'size_list', 'color', 'size', 'strap_color_list',
                   'dial_color_list',
                   'strap_color', 'dial_color', 'pack_of_list', 'pack_of', 'height', 'frame_color',
                   'combo_attr_for_swatch',
                   'capacity', 'quantity_list', 'quantity', 'number_of_contents_in_sales_package', 'finish_color_list',
                   'finish_color', 'number_of_shelves', 'sleeve', 'stitching_type', 'number_of_containers_list',
                   'number_of_containers', 'air_flow_level_list', 'air_flow_level', 'capacity_list',
                   'induction_bottom_list',
                   'induction_bottom', 'power_consumption', 'shade', 'shade_list', 'seating_capacity_list',
                   'orientation_list',
                   'orientation', 'seating_capacity', 'storage_included', 'number_of_contents_in_sales_package_list',
                   'mug_capacity_list', 'mug_capacity', 'color_code_list', 'color_code', 'blouse_piece',
                   'weight_of_plates_list',
                   'weight_of_plates', 'spf_rating_list', 'spf_rating', 'storage_included_list', 'diameter_list',
                   'diameter',
                   'with_microphone', 'thickness', 'decal_color_list', 'decal_color', 'total_jars_list', 'total_jars',
                   'plating_list',
                   'plating', 'display_size_list', 'display_size', 'number_of_shelves_list', 'gear_list',
                   'tire_size_list',
                   'tire_size', 'frame_size', 'gear', 'number_of_burners_list', 'ignition_system_list', 'gas_type_list',
                   'number_of_burners', 'gas_type', 'ignition_system', 'straps_list', 'padding_list', 'back_style_list',
                   'detachable_straps_list', 'padding', 'straps', 'detachable_straps', 'back_style',
                   'number_of_bottle_list',
                   'number_of_bottle', 'brand_color_list', 'material', 'brand_color', 'shape_list', 'shape',
                   'launch_year',
                   'head_type', 'weight_list', 'weight', 'wifi_connectivity', 'maximum_load', 'number_of_tiers', 'type',
                   'power_consumption_list', 'potency', 'storage_list', 'ram_list', 'storage', 'ram', 'occasion_list',
                   'occasion',
                   'cable_length_list', 'cable_length', 'bag_capacity_list', 'bag_capacity', 'number_of_prongs_list',
                   'number_of_prongs', 'height_list', 'suitable_for', 'sleeve_list', 'age_group_list', 'age_group',
                   'dimension_list',
                   'dimension', 'length_list', 'length', 'overall_length_list', 'overall_length',
                   'bottle_capacity_list',
                   'bottle_capacity', 'designed_for_list', 'designed_for', 'lens_color_list', 'frame_color_list',
                   'capacity_in_litres_list', 'capacity_in_litres', 'utility_type', 'thickness_list', 'bluetooth',
                   'power_output',
                   'flavour_list', 'flavour', 'number_of_door_list', 'mirror_included_list', 'mirror_included',
                   'number_of_door',
                   'suitable_for_list', 'slr_variant_list', 'slr_variant', 'connectivity_list', 'connectivity',
                   'vehicle_model_name',
                   'number_of_eggs_boiled_list', 'number_of_eggs_boiled', 'number_of_clips', 'fragrance', 'flavor_list',
                   'flavor',
                   'blouse_piece_list', 'size_diameter_list', 'size_diameter', 'maximum_display_size_list',
                   'maximum_display_size',
                   'battery_capacity', 'blade_length_list', 'blade_length', 'number_of_batteries',
                   'washing_capacity_list',
                   'energy_rating_list', 'washing_capacity', 'energy_rating', 'width', 'total_capacity_list',
                   'total_capacity',
                   'purifying_technology', 'bottom_length', 'depth_list', 'depth', 'top_length',
                   'corrective_power_list',
                   'corrective_power', 'trimming_range', 'blade_material', 'number_of_sockets_list',
                   'number_of_sockets',
                   'power_cord_length', 'usb_port', 'water_tank_capacity', 'led_power_consumption', 'type_list',
                   'size_in_length',
                   'number_of_needles_list', 'number_of_needles', 'motor_technology_list', 'motor_technology',
                   'number_of_lights',
                   'system_memory_list', 'ssd_capacity', 'system_memory', 'screen_size', 'wifi_connectivity_list',
                   'width_list',
                   'number_of_elastic_list', 'number_of_elastic', 'design_and_style',
                   'number_of_blackhead_removers_list',
                   'number_of_blackhead_removers', 'foot_filer_surface_material_list', 'foot_filer_surface_material',
                   'laptop_size_list', 'laptop_size', 'size_in_mm_list', 'size_in_mm', 'lens_color',
                   'power_output_list',
                   'number_of_bulbs', 'device_chipset', 'sweep_diameter', 'battery_capacity_list', 'operating_system',
                   'hd_technology', 'sales_package_list', 'sales_package', 'number_of_compartments_list',
                   'number_of_compartments',
                   'frame_size_list', 'number_of_brushes_list', 'number_of_brushes', 'number_of_plates_list',
                   'number_of_plates',
                   'manufacture_year_list', 'manufacture_year', 'purifying_technology_list', 'number_of_tools_list',
                   'number_of_tools', 'with_microphone_list', 'primary_material_subtype_list',
                   'primary_material_subtype',
                   'number_of_contents_in_set_list', 'paper_density', 'number_of_contents_in_set',
                   'water_tank_capacity_list',
                   'number_of_tiers_list', 'ideal_for', 'shade_code_list', 'shade_code', 'bat_grade', 'display',
                   'length_in_number_list', 'length_in_number', 'star_rating_list', 'bee_rating_year_list',
                   'star_rating',
                   'bee_rating_year', 'number_of_sticks_per_box_list', 'set_of_list', 'set_of',
                   'number_of_sticks_per_box',
                   'number_of_steps_list', 'hand_rail', 'tool_tray', 'number_of_steps', 'pan_capacity',
                   'number_of_pieces_list',
                   'number_of_pieces', 'bed_size_list', 'bed_size', 'launch_year_list', 'number_of_digits_list',
                   'number_of_digits',
                   'plant_size_list', 'container_color_list', 'container_material_list', 'plant_size',
                   'container_color',
                   'container_material', 'output_power_list', 'output_power', 'number_of_storage_boxes_list',
                   'number_of_storage_boxes', 'number_of_channels_list', 'number_of_channels', 'hand_rail_list',
                   'number_of_bunks_list', 'number_of_bunks', 'additional_content_list', 'included_games',
                   'additional_content',
                   'wireless_speed', 'wheel_diameter', 'pan_capacity_list', 'number_of_batteries_list',
                   'top_length_list',
                   'trimming_range_list', 'wheel_size', 'frame_diameter_list', 'handle_length_list', 'frame_diameter',
                   'handle_length', 'number_of_paint_shades_list', 'number_of_paint_shades', 'design_and_style_list',
                   'number_of_key_chains', 'maximum_load_list', 'number_of_chairs_list', 'number_of_chairs',
                   'number_of_seam_rippers_list', 'number_of_seam_rippers', 'compatible_idol_width_list',
                   'compatible_idol_width',
                   'hd_technology_list', 'massager_list', 'massager', 'number_of_contents_in_combo_set_list',
                   'number_of_contents_in_combo_set', 'number_of_holders_list', 'number_of_holders',
                   'size_for_refiner_list',
                   'size_for_refiner', 'screen_size_list', 'ideal_for_list', 'number_of_pieces_per_pack_list',
                   'number_of_pieces_per_pack', 'model_version_list', 'model_version', 'booking_type', 'state',
                   'base_stand_with_drawer_list', 'base_stand_with_drawer', 'number_of_wash_programs_list',
                   'number_of_wash_programs',
                   'number_of_racks', 'ssd_capacity_list', 'air_suction_capacity_list', 'filter_type_list',
                   'filter_type',
                   'air_suction_capacity', 'bag_size', 'number_of_lingerie_fashion_tape_list',
                   'number_of_lingerie_fashion_tape',
                   'material_list', 'power_cord_length_list', 'usb_port_list', 'number_of_racks_list',
                   'blade_material_list',
                   'base_flavor', 'number_of_packets_list', 'number_of_packets', 'speed_list', 'speed',
                   'panel_length_list',
                   'panel_length', 'wheel_diameter_list', 'bottom_length_list', 'interface_support',
                   'interface_support_list',
                   'size_in_length_list', 'operating_system_list', 'maximum_capacity_list', 'maximum_capacity',
                   'compatible_laptop_size_list', 'compatible_laptop_size', 'number_of_key_chains_list',
                   'utility_type_list',
                   'minimum_blood_sample_needed_list', 'minimum_blood_sample_needed', 'number_of_clips_list',
                   'number_of_pads_list',
                   'number_of_pads', 'number_of_pencil_boxes', 'max_power_consumption_list', 'max_power_consumption',
                   'fragrance_list', 'memory_size_list', 'read_speed', 'memory_size', 'number_of_blocks_list',
                   'number_of_blocks',
                   'number_of_covers_list', 'number_of_covers', 'rechargeable_list', 'rechargeable',
                   'dedicated_graphic_memory_capacity', 'primary_color_list', 'primary_color', 'count_list', 'count',
                   'color_pack_list', 'color_pack', 'number_of_buttons_list', 'number_of_buttons', 'reading_power_list',
                   'reading_power', 'detachable_usb_cable', 'dual_usb_ports', 'output_current',
                   'number_of_devices_batteries_charged',
                   'tool_tray_list', 'maximum_height_list', 'maximum_width', 'maximum_height',
                   'maximum_load_capacity_list',
                   'maximum_load_capacity', 'operating_power', 'maximum_weight_capacity_list',
                   'maximum_weight_capacity',
                   'mount_type_list', 'mount_type', 'minimum_age_list', 'minimum_age', 'holding_capacity_list',
                   'holding_capacity',
                   'rms_power_handling_list', 'rms_power_handling', 'error']
    for column in column_list:
        if isinstance(item[column], str):
            item[column] = None

        if isinstance(item[column], list):
            item[column] = []

        if isinstance(item[column], dict):
            item[column] = {}

        if isinstance(item[column], int):
            item[column] = None

        if isinstance(item[column], float):
            item[column] = None

        if isinstance(item[column], bool):
            if item[column] == True:
                item[column] = True
            else:
                item[column] = False
        if "product_url" in column or "requested_url" in column:
            item['product_url'] = url
            item['requested_url'] = url
        if "error" in column:
            item['error'] = True

    updated_data.append(item)

df = pd.DataFrame(updated_data)
# print(df.columns.to_list())
df.to_excel("update_data.xlsx",index=False)
# Save the updated data as a list
with open("update_data.json", "wb") as file:
    file.write(orjson.dumps(updated_data, option=orjson.OPT_INDENT_2))
