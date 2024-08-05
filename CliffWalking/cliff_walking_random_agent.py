import gym
import cv2
import numpy as np

# Creating the Environment
cliffEnv = gym.make("CliffWalking-v0")

# Handy functions for Visuals
def initialize_frame():
    width, height = 600, 200
    img = np.ones(shape=(height, width, 3)) * 255.0
    margin_horizontal = 6
    margin_vertical = 2

    # Vertical Lines
    for i in range(13):
        img = cv2.line(img, (49 * i + margin_horizontal, margin_vertical),
                       (49 * i + margin_horizontal, 200 - margin_vertical), color=(0, 0, 0), thickness=1)

    # Horizontal Lines
    for i in range(5):
        img = cv2.line(img, (margin_horizontal, 49 * i + margin_vertical),
                       (600 - margin_horizontal, 49 * i + margin_vertical), color=(0, 0, 0), thickness=1)

    # Cliff Box
    img = cv2.rectangle(img, (49 * 1 + margin_horizontal + 2, 49 * 3 + margin_vertical + 2),
                        (49 * 11 + margin_horizontal - 2, 49 * 4 + margin_vertical - 2), color=(255, 0, 255),
                        thickness=-1)
    img = cv2.putText(img, text="Cliff", org=(49 * 5 + margin_horizontal, 49 * 4 + margin_vertical - 10),
                      fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)

    # Goal
    frame = cv2.putText(img, text="G", org=(49 * 11 + margin_horizontal + 10, 49 * 4 + margin_vertical - 10),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 0), thickness=2)
    return frame

def put_agent(img, state):
    margin_horizontal = 6
    margin_vertical = 2

    try:
        print(f"State received: {state}")

        if isinstance(state, tuple):
            state = state[0]

        row = state // 12
        col = state % 12

        # Draw agent 'A' on the image
        cv2.putText(img, text="A", org=(49 * col + margin_horizontal + 10, 49 * (row + 1) + margin_vertical - 10),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 0), thickness=2)

    except Exception as e:
        print(f"Error in put_agent: {e}")
        raise

    return img

# Initializing our environment
done = False
frame = initialize_frame()
state = cliffEnv.reset()

# Main loop
while not done:
    # Show the current state of the environment
    print(f"State before put_agent: {state}")
    frame2 = put_agent(frame.copy(), state)

    # Debugging: Check if the agent 'A' is drawn correctly
    if not np.array_equal(frame, frame2):
        print("Agent 'A' successfully drawn on the frame.")
    else:
        print("Agent 'A' not drawn on the frame.")

    # Display the frame with the agent
    cv2.imshow("Cliff Walking", frame2)
    cv2.waitKey(250)  # Adjust refresh rate as needed

    # Select an action
    action = int(np.random.randint(low=0, high=4, size=1))

    # Take the action in the environment
    state, reward, done, _, _ = cliffEnv.step(action)

# Close the environment
cliffEnv.close()
cv2.destroyAllWindows()
