import tkinter as tk

def center_window(window):
    window.update_idletasks()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window.geometry(f"+{x}+{y}")

def main():
    root = tk.Tk()
    root.withdraw()

    response = [None]  # Store user's choice

    def create_confirmation_dialog():
        window = tk.Toplevel(root)
        window.title("Confirmation")

        # Modern styling constants
        BG_COLOR = "#f8f9fa"    # Light background
        BUTTON_BG = "#e9ecef"   # Neutral button color
        BUTTON_ACTIVE_BG = "#dee2e6"  # Slightly darker on click
        TEXT_COLOR = "#212529"  # Dark text
        FONT = ("Segoe UI", 10) if 'win' in tk.Tcl().eval('tk windowingsystem') else ("Arial", 10)
        PADDING = 12

        window.config(bg=BG_COLOR)

        # Message label
        label = tk.Label(
            window,
            text="Are you sure?",
            font=(FONT[0], 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            pady=15
        )
        label.pack()

        # Button frame
        button_frame = tk.Frame(window, bg=BG_COLOR)
        button_frame.pack(pady=10, padx=20)

        # Button commands
        def on_yes():
            response[0] = True
            window.destroy()

        def on_no():
            response[0] = False
            window.destroy()

        # Yes Button
        yes_button = tk.Button(
            button_frame,
            text="Yes",
            command=on_yes,
            bg=BUTTON_BG,
            fg=TEXT_COLOR,
            activebackground=BUTTON_ACTIVE_BG,
            activeforeground=TEXT_COLOR,
            font=FONT,
            padx=PADDING,
            pady=6,
            bd=0,
            relief="flat"
        )
        yes_button.pack(side=tk.LEFT, padx=8)

        # No Button
        no_button = tk.Button(
            button_frame,
            text="No",
            command=on_no,
            bg=BUTTON_BG,
            fg=TEXT_COLOR,
            activebackground=BUTTON_ACTIVE_BG,
            activeforeground=TEXT_COLOR,
            font=FONT,
            padx=PADDING,
            pady=6,
            bd=0,
            relief="flat"
        )
        no_button.pack(side=tk.RIGHT, padx=8)

        center_window(window)
        window.resizable(False, False)
        window.wait_window(window)

    create_confirmation_dialog()

    if response[0]:
        print("You clicked Yes!")
    else:
        print("You clicked No!")

    root.destroy()

if __name__ == "__main__":
    main()