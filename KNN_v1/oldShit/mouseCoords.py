from pynput import mouse


def on_click(x, y, button, pressed):
	if pressed:
		print(f"{x}, {y}")


# Set up the mouse listener
with mouse.Listener(on_click=on_click) as listener:
	listener.join()
