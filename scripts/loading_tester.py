import tkinter as tk
from tkinter import ttk
import time


def show_loading_screen():
    loading_screen = tk.Toplevel(root)
    loading_screen.title("Loading...")

    # Add a progress bar in determinate mode
    progress = ttk.Progressbar(loading_screen, mode="determinate")
    progress.pack(pady=10)

    # Optional: Center the loading screen on the main window
    loading_screen.geometry(
        "+{}+{}".format(
            root.winfo_rootx() + root.winfo_reqwidth() // 2 - 50,
            root.winfo_rooty() + root.winfo_reqheight() // 2 - 50,
        )
    )

    root.update()  # Force an update to display the loading screen

    # Perform time-consuming tasks here
    total_tasks = 10  # Adjust the total number of tasks as needed

    for i in range(total_tasks):
        # Update progress bar (assuming equal progress for each task)
        progress_value = (i + 1) * 100 / total_tasks
        progress["value"] = progress_value
        loading_screen.update_idletasks()  # Force an update of the GUI

        time.sleep(0.5)  # Simulating a time-consuming task

    # After finishing loading, destroy the loading screen
    loading_screen.destroy()


root = tk.Tk()

# Create a button to trigger loading
button = tk.Button(root, text="Load", command=show_loading_screen)
button.pack()

root.mainloop()
