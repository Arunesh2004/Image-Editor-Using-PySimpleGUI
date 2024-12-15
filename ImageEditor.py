import PySimpleGUI as sg
from PIL import Image, ImageFilter, ImageOps
from io import BytesIO

# Function to update the image based on user inputs
def update_image(original, blur, contrast, emboss, contour, flipx, flipy):
    global image

    # Apply Gaussian blur to the original image based on the slider value
    image = original.filter(ImageFilter.GaussianBlur(blur))

    # Apply unsharp mask to adjust the contrast based on the slider value
    image = image.filter(ImageFilter.UnsharpMask(contrast))

    # Apply emboss filter if the checkbox is selected
    if emboss:
        image = image.filter(ImageFilter.EMBOSS())

    # Apply contour filter if the checkbox is selected
    if contour:
        image = image.filter(ImageFilter.CONTOUR())

    # Flip the image horizontally if the checkbox is selected
    if flipx:
        image = ImageOps.mirror(image)

    # Flip the image vertically if the checkbox is selected
    if flipy:
        image = ImageOps.flip(image)

    # Convert the processed image to a format compatible with PySimpleGUI
    bio = BytesIO()
    image.save(bio, format='PNG')

    # Update the displayed image in the GUI window
    window['-IMAGE-'].update(data=bio.getvalue())

# Open a file dialog to select an image and get its path
image_path = sg.popup_get_file('Open an Image', no_window=True)

# Ensure a file was selected
if not image_path:
    sg.popup("No image selected. Exiting.", title="Error")
    exit()

# Define the layout for the control panel (sliders, checkboxes, and save button)
control_col = sg.Column([
    [sg.Frame('Blur', layout=[[sg.Slider(range=(0, 10), orientation='h', key='-BLUR-', default_value=0)]])],
    [sg.Frame('Contrast', layout=[[sg.Slider(range=(0, 10), orientation='h', key='-CONTRAST-', default_value=0)]])],
    [sg.Checkbox('Emboss', key='-EMBOSS-')],
    [sg.Checkbox('Contour', key='-CONTOUR-')],
    [sg.Checkbox('Flip x', key='-FLIPX-')],
    [sg.Checkbox('Flip y', key='-FLIPY-')],
    [sg.Button('Save Image', key='-SAVE-')],
])

# Define the layout for displaying the image
image_col = sg.Column([[sg.Image(image_path, key='-IMAGE-')]])

# Combine the control panel and image display into the main layout
layout = [[control_col, image_col]]

# Open the selected image using PIL
try:
    original = Image.open(image_path)
except Exception as e:
    sg.popup(f"Error loading image: {e}", title="Error")
    exit()

# Create the GUI window
window = sg.Window('Image Editor', layout)

# Event loop to handle user interactions
while True:
    # Read events and values from the GUI window
    event, values = window.read(timeout=50)

    # Break the loop and close the window if the user closes it
    if event == sg.WIN_CLOSED:
        break

    # Update the image based on the current values of the sliders and checkboxes
    update_image(
        original, 
        values['-BLUR-'], 
        values['-CONTRAST-'], 
        values['-EMBOSS-'], 
        values['-CONTOUR-'],
        values['-FLIPX-'], 
        values['-FLIPY-']
    )

    # Handle the Save Image button click
    if event == '-SAVE-':   
        # Open a file dialog to get the save path
        save_path = sg.popup_get_file('Save Edited Image', save_as=True, no_window=True, file_types=(("PNG Files", "*.png"),))
        
        # Check if a save path was provided
        if save_path:
            # Ensure the file has a .png extension
            if not save_path.lower().endswith('.png'):
                save_path += '.png'
            try:
                # Save the edited image to the specified path
                image.save(save_path, format='PNG')
                sg.popup(f"Image saved successfully at:\n{save_path}", title="Success")
            except Exception as e:
                sg.popup(f"Error saving image: {e}", title="Error")
        else:
            sg.popup("Save operation canceled.", title="Canceled")

# Close the GUI window
window.close()
 
# Thanks