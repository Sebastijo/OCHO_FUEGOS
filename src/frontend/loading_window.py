"""
This module's purpose is to create a loading window that will be displayed when the user is waiting for the program to finish a task.
The tasks that will be performed are tmainly loading a window lol.

THIS ISN'T USED AS OF RIGHT NOW. IT MIGHT BE IMPLEMENTED IF TIME PERMITS.
"""

import tkinter as tk
from tkinter import Toplevel
import threading
import time

def open_slow_window_wrapper(open_slow_window, loading_screen):
    """
    Wrapper function to open the slow window and close the loading screen.
    """
    print("Wrapper function started")
    open_slow_window()  # Call the function to open the slow window
    print("Slow window opened, closing loading screen")
    loading_screen.destroy()  # Close the loading screen after the slow window is opened

# Function to open the loading screen and handle threading
def open_with_loading_screen(open_slow_window: callable) -> None:
    """
    Function to show a loading screen while a slow window is being opened.

    Args:
        open_slow_window (callable): Function to open the slow window

    Returns:
        None
    
    Raises:
        AssertionError: If open_slow_window is not a callable function
    """
    assert callable(open_slow_window), "open_slow_window must be a callable function"
    loading_screen = Toplevel()  # Create the loading screen
    loading_screen.title("Loading...")
    tk.Label(loading_screen, text="Please wait...").pack()

    # Start a thread to open the slow window while keeping the loading screen active
    thread = threading.Thread(
        target=open_slow_window_wrapper,
        args=(open_slow_window, loading_screen),
        daemon=True,
    )
    thread.start()

if __name__ == "__main__":

    # Function to open the slow window
    def open_slow_window():
        print("Opening slow window")
        slow_window = Toplevel()
        slow_window.title("Slow Window")
        tk.Label(slow_window, text="This is a slow window").pack()

        # Simulate a slow process
        time.sleep(5)  # Reduced time for quicker testing
        print("Slow window process completed")

    # Main window setup
    root = tk.Tk()
    root.title("Main Window")

    # Button to trigger the slow window loading process
    open_button = tk.Button(root, text="Open Slow Window", command=lambda: open_with_loading_screen(open_slow_window))
    open_button.pack(pady=20)

    # Start the Tkinter event loop
    root.mainloop()