import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import winsound

def generate_keys():
    keys=[]
    for i in range(1, 8):
        for j in range(2**i-1):
            keys.append(bin(j)[2:].zfill(i))
    return keys

keys = generate_keys()
 
def decode_message(header, encoded_message):

    keys_mapping = {keys[i]: header[i] for i in range(len(header))}

    decoded_message = ""
    i = 0
    while i < len(encoded_message):
        key_length = int(encoded_message[i:i + 3], 2)
        i += 3
        if key_length == 0:
            break
        key_end = "1" * key_length
        while i < len(encoded_message):
            if encoded_message[i:i + key_length] in keys_mapping:
                decoded_message += keys_mapping[encoded_message[i:i + key_length]]
                i += key_length
            elif encoded_message[i:i + key_length] == key_end:
                i += key_length
                break
    return decoded_message

def encoded_message(decoded_message):
    header = ""

    unique_chars = set()

    for char in decoded_message:
        unique_chars.add(char)

    header = ''.join(unique_chars)

    keys_mapping = {header[i]: keys[i] for i in range(len(header))}

    message = ""
    for char in decoded_message:
        if char in keys_mapping:
            key = keys_mapping[char]
            key_length = len(key)
            encoded_key = bin(key_length)[2:].zfill(3) 
            message += encoded_key+keys_mapping[char]+"1"*key_length
    message += "000"
    return(header,message)



def openFileDecode():
    textbox.delete("1.0",tk.END)
    filepath = filedialog.askopenfilename(title="Select encoded file", filetypes=[("Text Files", "*.txt")])
    if filepath:
        with open(filepath, 'r') as file:
            lines = file.readlines()
            lines = [line.replace('\n', '').replace('\r','') for line in lines]
            i = 0
            while i < len(lines):
                header = lines[i]
                i += 1
                message = ""
                while i < len(lines):
                    if lines[i][-3:] != "000":
                        message += lines[i]
                        i += 1
                    else:
                        message += lines[i]
                        i += 1
                        break
                decoded_message = decode_message(header, message)
                textbox.pack(fill=tk.BOTH, expand=True)
                textbox.insert(tk.END, decoded_message + "\n")
            play_audio()

def openFileEncode():
    textbox.delete("1.0",tk.END)
    filepath = filedialog.askopenfilename(title="Select decoded file", filetypes=[("Text Files", "*.txt")])
    if filepath:
        with open(filepath, 'r') as file:
                lines = file.readlines()
                lines = [line.replace('\n', '').replace('\r','') for line in lines]
                i = 0
                while i < len(lines):
                    decode = lines[i]
                    i += 1
                    header,message=encoded_message(decode)
                    textbox.pack(fill=tk.BOTH, expand=True)
                    textbox.insert(tk.END,header+"\n"+message+"\n")
                play_audio()

def play_audio():
    audio_file = "C:/Users/banvar/Desktop/mixkit-soap-bubble-sound-2925.wav"
    winsound.PlaySound(audio_file, winsound.SND_ASYNC)

window = tk.Tk()
window.geometry("1520x900")
window.configure(bg='light cyan')
window.title("Encoding and Decoding")

frame=tk.Frame(window, bg="DodgerBlue4")
frame.pack(side=tk.LEFT, fill=tk.Y)

button1 = ttk.Button(frame,text="Decode", command=openFileDecode, width=15)
button1.pack(side = tk.TOP,padx=15,pady=20)
button1.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

button2 = ttk.Button(frame,text="Encode", command=openFileEncode, width=15)
button2.place(relx=0.5, rely=1.20, anchor=tk.CENTER)
button2.pack(side = tk.LEFT,padx=15,pady=20)

style = ttk.Style()
style.configure('TButton', font=('Helvetica', 14), padding=20)

img = Image.open("C:/Users/banvar/Desktop/python project/ENCODING AND DECODING (1).png")
test = ImageTk.PhotoImage(img)
label = tk.Label(image=test)
label.image = test
label.place(x=315, y=50)

textbox = tk.Text(window,height=30,width=95)
textbox = tk.Text(window, font=('Helvetica', 16), foreground='black', background='light blue')
textbox.configure(borderwidth=2, relief='groove', padx=10, pady=10)

scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
textbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=textbox.yview)

window.mainloop()


