
import time
import helper
import playsound3
from pumpkinpipe.hand import HandDetector
from pumpkinpipe.utils.drawing import overlay_image
import cv2

from helper import verify_instructions

'''
Some information:
Webcam Resolution: 640x, 480y

'''

def main():
    """
    main() is responsible for running the main thread. Main thread runs through here to prevent any external imports of this file to run inadvertently
    main() is also responsible for handling the primary gameplay loop.

    :return: None
    """

    cap = cv2.VideoCapture(0)

    hand_detector = HandDetector(max_hands=2)

    # constants
    COUNTDOWN_TIMER = 5
    ROUND_TIMER = 10
    BASE_SCORE_GAIN = 500
    BASE_SCORE_LOSS = 275

    COLOR_CODE_SIZE = 25 # pixels
    LEFT_COLOR_CODE = (290, 30)
    RIGHT_COLOR_CODE = (350, 30)

    # globals
    instructions = None
    player_score = 0
    score_multiplier = 1

    easy_mode = input("\nEnable noob mode? (enables colored hands but reduces score gain) y/n: ")

    while True:
        if len(easy_mode) != 1:
            print("Just enter letter y or n for yes/no")
            easy_mode = input("Enable easy mode? (enables colored hands but reduces score gain) y/n: ")
        elif not easy_mode.isalpha():
            print("Just enter y or n for yes/no")
            easy_mode = input("Enable easy mode? (enables colored hands but reduces score gain) y/n: ")
        elif easy_mode.lower() == "y":
            print("good luck noob")
            BASE_SCORE_GAIN = 150
            easy_mode = True
            break
        else:
            if easy_mode.lower() == "n":
                easy_mode = False
                print("good luck")
            else:
                print("That was not letters y or n. I assume no.")
                easy_mode = False
            break

    if not easy_mode:
        hard_mode = input("Enable hard mode? (round times are shorter but more score gain) y/n: ")
        while True:
            if len(hard_mode) != 1:
                print("Just enter letter y or n for yes/no")
                hard_mode = input("Enable hard mode? y/n: ")
            elif not hard_mode.isalpha():
                print("Just enter y or n for yes/no")
                hard_mode = input("Enable hard mode? y/n: ")
            elif hard_mode.lower() == "y":
                print("you deserve some respect")
                ROUND_TIMER = 5
                BASE_SCORE_GAIN = 950
                break
            else:
                if hard_mode.lower() == "n":
                    print("okay")
                else:
                    print("That was not letters y or n. I assume no.")
                break

    print("Click on the new python window on your taskbar to open the game.")

    # initiate the beginning countdown
    countdown_start, round_start_time = time.time(), time.time()

    # BGR format
    left_landmark_color = (255, 255, 255)
    left_connection_color = (255, 255, 255)

    right_landmark_color = (255, 255, 255)
    right_connection_color = (255, 255, 255)

    # booleans that prevents events/code from executing
    # also called debouncers
    game_start = False
    round_start = False

    while True:

        success, frame = cap.read()

        if not success:
            print("Could not read webcam frame. main() returned 0")
            return

        frame = cv2.flip(frame, 1)
        hands = hand_detector.find_hands(frame)

        for hand in hands:

            if easy_mode:
                if hand.side == "Left":
                    hand.set_landmarks_style(
                        fill=left_landmark_color
                    )
                    hand.set_connection_style(
                        stroke=left_connection_color
                    )
                elif hand.side == "Right":
                    hand.set_landmarks_style(
                        fill=right_landmark_color
                    )
                    hand.set_connection_style(
                        stroke=right_connection_color
                    )
            else:
                hand.set_landmarks_style(
                    fill=(255, 255, 255)
                )
                hand.set_connection_style(
                    stroke=(255,255,255)
                )

            hand.draw()

        if time.time() - countdown_start < COUNTDOWN_TIMER and not game_start:

            rounded_countdown = round(time.time() - countdown_start, 1)

            # countdown
            cv2.putText(
                frame,
                str(round(COUNTDOWN_TIMER - rounded_countdown, 2)),
                (230, 240),
                cv2.FONT_HERSHEY_SIMPLEX,
                3,
                (255, 255, 255), # remember: this is BGR for whatever reason
                3
            )

            # tips before playing
            cv2.putText(
                frame,
                "Get ready. You might want to move back from your device. Avoid very bright lights.",
                (20, 300),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (255, 255, 255),
                2
            )
        else:
            game_start = True

        if game_start:

            # create the dividers
            cv2.line(
                frame,
                (0, 240),
                (640, 240),
                (0, 0, 0),
                2
            )
            cv2.line(
                frame,
                (320, 0),
                (320, 480),
                (0,0,0),
                2
            )

            if not round_start:
                round_start = True
                instructions = helper.generate_hand_instructions()
                round_start_time = time.time()
            else:

                if time.time() - round_start_time < ROUND_TIMER:

                    rounded_timer = round(time.time() - round_start_time, 2)
                    subtracted_timer = round(ROUND_TIMER - rounded_timer, 1)

                    # create score and score multiplier
                    cv2.putText(
                        frame,
                        f"Score: {round(player_score)}",
                        (25, 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.75,
                        (0,0,0),
                        2
                    )
                    cv2.putText(
                        frame,
                        f"Multiplier: {round(score_multiplier, 1)}",
                        (25, 140),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.75,
                        (0, 0, 0),
                        2
                    )

                    # create the round timer
                    cv2.putText(
                        frame,
                        str(subtracted_timer),
                        (25,40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 0),
                        2
                    )

                    # draw information

                    # quadrant color labels
                    cv2.circle(
                        frame,
                        (290, 210),
                        25,
                        (0, 0, 255),
                        -1
                    )
                    cv2.circle(
                        frame,
                        (350, 210),
                        25,
                        (255, 0, 0),
                        -1
                    )
                    cv2.circle(
                        frame,
                        (290, 270),
                        25,
                        (0, 255, 0),
                        -1
                    )
                    cv2.circle(
                        frame,
                        (350, 270),
                        25,
                        (0, 255, 255),
                        -1
                    )
                    #print(instructions)

                    left_instructions = instructions["Left"]
                    right_instructions = instructions["Right"]

                    # initialize left instructions
                    if left_instructions[0] == "red":

                        cv2.circle(
                            frame,
                            LEFT_COLOR_CODE,
                            COLOR_CODE_SIZE,
                            (0, 0, 255),
                            -1
                        )
                        left_landmark_color = (0, 0, 255)
                        left_connection_color = (0, 0, 255)


                    elif left_instructions[0] == "blue":

                        cv2.circle(
                            frame,
                            LEFT_COLOR_CODE,
                            COLOR_CODE_SIZE,
                            (255, 0, 0),
                            -1
                        )
                        left_landmark_color = (255, 0, 0)
                        left_connection_color = (255, 0, 0)

                    elif left_instructions[0] == "green":

                        cv2.circle(
                            frame,
                            LEFT_COLOR_CODE,
                            COLOR_CODE_SIZE,
                            (0, 255, 0),
                            -1
                        )
                        left_landmark_color = (0, 255, 0)
                        left_connection_color = (0, 255, 0)


                    elif left_instructions[0] == "yellow":

                        cv2.circle(
                            frame,
                            LEFT_COLOR_CODE,
                            COLOR_CODE_SIZE,
                            (0, 255, 255),
                            -1
                        )
                        left_landmark_color = (0, 255, 255)
                        left_connection_color = (0, 255, 255)

                    if left_instructions[1] == [1,1,0,0,1]:

                        overlay_image(
                            frame,
                            "ily_handsign.png",
                            (185, 5),
                            scale=0.1
                        )

                    elif left_instructions[1] == [0,1,1,0,0]:

                        overlay_image(
                            frame,
                            "peace_handsign.png",
                            (185, 5),
                            scale=0.1
                        )

                    elif left_instructions[1] == [0,0,1,1,1]:

                        overlay_image(
                            frame,
                            "ok_handsign.png",
                            (185, 5),
                            scale=0.15
                        )

                    elif left_instructions[1] == [1,0,0,0,1]:

                        overlay_image(
                            frame,
                            "shaka_handsign.png",
                            (185, 5),
                            scale=0.15
                        )

                    # initialize right instructions
                    if right_instructions[0] == "red":

                        cv2.circle(
                            frame,
                            RIGHT_COLOR_CODE,
                            COLOR_CODE_SIZE,
                            (0, 0, 255),
                            -1
                        )
                        right_landmark_color = (0, 0, 255)
                        right_connection_color = (0, 0, 255)

                    elif right_instructions[0] == "blue":

                        cv2.circle(
                            frame,
                            RIGHT_COLOR_CODE,
                            COLOR_CODE_SIZE,
                            (255, 0, 0),
                            -1
                        )
                        right_landmark_color = (255, 0, 0)
                        right_connection_color = (255, 0, 0)

                    elif right_instructions[0] == "green":

                        cv2.circle(
                            frame,
                            RIGHT_COLOR_CODE,
                            COLOR_CODE_SIZE,
                            (0, 255, 0),
                            -1
                        )
                        right_landmark_color = (0, 255, 0)
                        right_connection_color = (0, 255, 0)

                    elif right_instructions[0] == "yellow":

                        cv2.circle(
                            frame,
                            RIGHT_COLOR_CODE,
                            COLOR_CODE_SIZE,
                            (0, 255, 255),
                            -1
                        )
                        right_landmark_color = (0, 255, 255)
                        right_connection_color = (0, 255, 255)

                    if right_instructions[1] == [1, 1, 0, 0, 1]:

                        overlay_image(
                            frame,
                            "ily_handsign.png",
                            (385, 5),
                            scale=0.1
                        )

                    elif right_instructions[1] == [0, 1, 1, 0, 0]:

                        overlay_image(
                            frame,
                            "peace_handsign.png",
                            (385, 5),
                            scale=0.1
                        )

                    elif right_instructions[1] == [0, 0, 1, 1, 1]:

                        overlay_image(
                            frame,
                            "ok_handsign.png",
                            (385, 5),
                            scale=0.15
                        )

                    elif right_instructions[1] == [1, 0, 0, 0, 1]:

                        overlay_image(
                            frame,
                            "shaka_handsign.png",
                            (385, 5),
                            scale=0.15
                        )

                    verification = verify_instructions(hands, instructions)

                    if verification:
                        playsound3.playsound("urawinner.mp3", block=False)
                        round_start = False

                        if score_multiplier >= 1:
                            score_multiplier += 0.1
                        else:
                            score_multiplier = 1

                        player_score += BASE_SCORE_GAIN * score_multiplier


                else:
                    playsound3.playsound("buzzerlose.mp3", block=False)
                    round_start = False

                    if score_multiplier > 1:
                        score_multiplier -= 0.1

                    player_score -= BASE_SCORE_LOSS * score_multiplier




        cv2.imshow("Computer Vision Project", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if cv2.getWindowProperty("Computer Vision Project", cv2.WND_PROP_VISIBLE) < 1:
            break

if __name__ == "__main__":
    main()