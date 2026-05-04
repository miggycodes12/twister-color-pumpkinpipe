
import random


# these are helper functions for the helper functions...
def id_to_quadrant(id: int) -> str | None:

    """
    id_to_quadrant is a helper function for generate_hand_instructions. It converts ids 1-4 into hand color information.

    :param id: An integer to be matched with a quadrant color
    :return: A string of a quadrant color
    """

    match id:
        case 1:
            return "red"
        case 2:
            return "blue"
        case 3:
            return "green"
        case 4:
            return "yellow"

    print("WARNING id_to_quadrant(): given id did not match with any cases")
    return None

def id_to_finger_flags(id) -> list | None:

    """
    id_to_finger_flags is a helper function for generate_hand_instructions. It coverts ids 1-4 into specific finger flag lists.

    :param id: An integer to be matched with a finger flag list or specific hand sign
    :return: A binary list containing finger flag information
    """

    match id:
        case 1:
            return [1, 1, 0, 0, 1] # "I love you"
        case 2:
            return [0, 1, 1, 0, 0] # "peace"
        case 3:
            return [0, 0, 1, 1, 1] # "ok"
        case 4:
            return [1, 0, 0, 0, 1] # "shaka"

    print("WARNING id_to_finger_flags(): given id did not match with any cases")
    return None

######

def point_in_region(point_xy: tuple[int, int], top_left: tuple[int, int], bottom_right: tuple[int, int]) -> bool:

    """
    point_in_region takes a given point and checks if the point is within a 2D region defined by the top left and bottom right points of that region.

    :param point_xy: A tuple containing the x and y positions of the main point to be checked.
    :param top_left: A tuple containing the x and y positions of the top left point of the region.
    :param bottom_right: A tuple containing the x and y positions of the bottom right point of the region.
    :return: Either true or false. True if the point is within the region and False if it is not.
    """

    x_point = point_xy[0]
    y_point = point_xy[1]

    x1_region = top_left[0]
    y1_region = top_left[1]

    x2_region = bottom_right[0]
    y2_region = bottom_right[1]

    if x1_region <= x_point <= x2_region and y1_region <= y_point <= y2_region:
        return True
    else:
        return False

def generate_hand_instructions():

    """
    generate_hand_instructions generates random integers between 1 and 4 and converts them to a specific set of color and finger flag information.

    :return: A dictionary containing keys "Left" and "Right" that holds tuples containing the color and hand sign instructions for their corresponding hand.
    """

    instructions = {}

    # [1, 1, 1, 1, 1] finger flags is Thumb, Index, Middle, Ring, and Pinky respectively.

    left_color = random.randint(1, 4)
    right_color = random.randint(1, 4)

    left_sign = random.randint(1, 4)
    right_sign = random.randint(1, 4)

    left_instructions = (id_to_quadrant(left_color), id_to_finger_flags(left_sign))
    right_instructions = (id_to_quadrant(right_color), id_to_finger_flags(right_sign))

    instructions["Left"] = left_instructions
    instructions["Right"] = right_instructions

    return instructions

def verify_instructions(hand_objects: list, instructions: dict) -> bool:

    """
    verify_instructions takes detected hand objects of a certain frame and information from generate_hand_instructions.
    It then compares whether the detected hands within the frame match the Left and Right hand information within the given instructions' dictionary.

    :param hand_objects: A list of detected hand objects from a frame
    :param instructions: A dictionary containing two keys: "Left" and "Right" that hold information on where both hands should be positioned and their finger flags.
    :return: Either true or false. If false, then the given hand_object list doesn't have both hand present or the hands do not follow the dictionary's instructions. If it is true then the hands correctly match the instructions given.
    """

    if len(hand_objects) != 2:
        return False

    RED_QUADRANT = ((0, 0), (320, 240))
    BLUE_QUADRANT = ((320, 0), (640, 240))
    GREEN_QUADRANT = ((0, 240), (320, 480))
    YELLOW_QUADRANT = ((320,240), (640, 480))

    left_color, right_color = None, None
    left_flags, right_flags = None, None

    for hand in hand_objects:
        in_red = point_in_region(hand.center, RED_QUADRANT[0], RED_QUADRANT[1])
        in_blue = point_in_region(hand.center, BLUE_QUADRANT[0], BLUE_QUADRANT[1])
        in_yellow = point_in_region(hand.center, YELLOW_QUADRANT[0], YELLOW_QUADRANT[1])
        in_green = point_in_region(hand.center, GREEN_QUADRANT[0], GREEN_QUADRANT[1])

        if hand.side == "Left":

            left_flags = hand.flags

            if in_red:
                left_color = "red"
            elif in_blue:
                left_color = "blue"
            elif in_yellow:
                left_color = "yellow"
            elif in_green:
                left_color = "green"
        elif hand.side == "Right":

            right_flags = hand.flags

            if in_red:
                right_color = "red"
            elif in_blue:
                right_color = "blue"
            elif in_yellow:
                right_color = "yellow"
            elif in_green:
                right_color = "green"


    left_instruction = instructions["Left"]
    right_instruction = instructions["Right"]

    compare_left = left_color == left_instruction[0] and left_flags == left_instruction[1]
    compare_right = right_color == right_instruction[0] and right_flags == right_instruction[1]

    #print(f"compare_left: {compare_left}, compare_right: {compare_right}")

    return compare_left and compare_right