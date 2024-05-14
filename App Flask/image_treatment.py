import cv2

# Calculate the color thresholding and region props
def imageTreatment(filename):
    frame = cv2.imread(filename)

    # The order of the colors is blue, green, red
    # floor_lower_color_bounds = (200, 0, 0)
    # floor_upper_color_bounds = (250,20,20)
    # Yellow
    chair_lower_color_bounds = (0,150,150)
    chair_upper_color_bounds = (100,255,255)
    # Magenta
    door_lower_color_bounds = (80,0,200)
    door_upper_color_bounds = (150,20,255)
    # Turquoise
    table_lower_color_bounds = (120,200,0)
    table_upper_color_bounds = (210,255,40)

    # Masks
    try:
        # floor_mask = cv2.inRange(frame, floor_lower_color_bounds, floor_upper_color_bounds)
        table_mask = cv2.inRange(frame, table_lower_color_bounds, table_upper_color_bounds)
        chair_mask = cv2.inRange(frame, chair_lower_color_bounds, chair_upper_color_bounds)
        door_mask = cv2.inRange(frame, door_lower_color_bounds, door_upper_color_bounds)
    except Exception as err:
        raise RuntimeError('Error creating the masks', err.args)
    
    # Aplicar erode para los muebles que tocan (op morfologica)
    # floor_mask_processed = cv2.morphologyEx(floor_mask, cv2.MORPH_OPEN, None)
    table_mask_processed = cv2.morphologyEx(table_mask, cv2.MORPH_OPEN, None)
    chair_mask_processed = cv2.morphologyEx(chair_mask, cv2.MORPH_OPEN, None)
    door_mask_processed = cv2.morphologyEx(door_mask, cv2.MORPH_OPEN, None)

    # floor_mask_processed = cv2.morphologyEx(floor_mask_processed, cv2.MORPH_CLOSE, None)
    table_mask_processed = cv2.morphologyEx(table_mask_processed, cv2.MORPH_CLOSE, None)
    chair_mask_processed = cv2.morphologyEx(chair_mask_processed, cv2.MORPH_CLOSE, None)
    door_mask_processed = cv2.morphologyEx(door_mask_processed, cv2.MORPH_CLOSE, None)

    # Show images with contours and centroids
    # cv2.imshow('Floor with contours', floor_with_props)
    # cv2.imshow('Table with contours', table_mask_processed)
    # cv2.imshow('Chair with contours', chair_mask_processed)
    # cv2.imshow('Door with contours', door_mask_processed)

    # print('Press <q> to exit')
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Apply contours and centroid for each mask
    try:
        table_regs = regionProps(table_mask_processed.copy())
    except Exception as err:
        raise RuntimeError('Error getting region props of table', err.args)
    try:
        chair_regs = regionProps(chair_mask_processed.copy())
    except Exception as err:
        raise RuntimeError('Error getting region props of chair', err.args)
    try:
        door_regs = regionProps(door_mask_processed.copy())
    except Exception as err:
        raise RuntimeError('Error getting region props of door:', err.args)
    
    # cv2.imshow('table with contours', table_regs['mask'])
    # cv2.imshow('chair with contours', chair_regs['mask'])
    # cv2.imshow('door with contours', door_regs['mask'])

    regs_data = {
        'tables': table_regs['data'],
        'chairs': chair_regs['data'],
        'doors': door_regs['data']
    }

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return regs_data

# Returns the posittion and dimensions of the contours and its centroid
# format:
# {
#   'mask': mask_image,
#   'data': [
#               {
#                 "x":478,
#                 "y":478,
#                 "w":34,
#                 "h":34,
#                 "centroid_x ":494,
#                 "centroid_y":494
#               },
#               { other contour },
#               ...
#           ]
# }
def regionProps(mask):
    contours, hierarchy  = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask_copy = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)  # Convertir a color
    contours_data = []
    for contour in contours:
        # Calculate area of the region
        area = cv2.contourArea(contour)
        if area > 0:
            # Calculate bounding rectangle dimensions
            x, y, w, h = cv2.boundingRect(contour)
            
            # Calculate perimeter of the region
            perimeter  = cv2.arcLength(contour, True)
            
            # Calculate centroid of the region
            M = cv2.moments(contour)
            centroid_x  = int(M["m10"] / M["m00"])
            centroid_y  = int(M["m01"] / M["m00"])
            
            # Draw contour, centroid, and bounding rectangle on a copy of the original mask
            # cv2.drawContours(mask_copy, [contour], -1, (0, 0, 255), 2)
            cv2.circle(mask_copy, (centroid_x , centroid_y), 5, (0, 0, 255), -1)
            cv2.rectangle(mask_copy, (x, y), (x + w, y + h), (50, 255, 50), 2)
            contours_data.append({
                'x': x,
                'y': y,
                'w': w,
                'h': h,
                'centroid_x ': centroid_x ,
                'centroid_y': centroid_y
            })
    return {
        'mask': mask_copy,
        'data': contours_data
        }
