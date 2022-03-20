# Typecast GUI
# Use threading for audio output
# Simple input boxes will suffice (tkinter)

from tkinter import *
import PIL
from PIL import ImageTk, Image
import client
from threading import *

class TypeCastApp():
	# class var	
	count = 0
	lock = Lock()

	# constructor, init, root is the GUI
	def __init__(self):
		self.root = Tk()
		self.root.overrideredirect(1)

		#title
		self.root.title('Typecast Typer with Sound')
		self.root.iconbitmap('assets/v2v.ico')

		#preset
		self.root.attributes("-topmost", True)
		
		# GUI box
		self.root.geometry(f"+{500}+{500}")

		# drag and move
		self.grip = Label(self.root, bitmap="gray25", bg='#495261')
		self.grip.pack(side="top", fill="both")
		self.preset = Label(self.root, text="ICONS", bg='#495261', fg='#ffffff')
		self.preset.pack(side="left", fill="both", expand=True)
		self.grip.bind("<ButtonPress-1>", self.start_move)
		self.grip.bind("<ButtonRelease-1>", self.stop_move)
		self.grip.bind("<B1-Motion>", self.do_move)

		# Quit button
		self.frame = Frame(self.root, width=480, height=850, borderwidth=10)
		self.frame.configure(background='#515151')
		self.frame.pack_propagate(False	)
		self.frame.pack()
		self.bQuit = Button(self.frame, text="QUIT", command=self.root.quit)


		# Main Image 		
		# Create an object of tkinter ImageTk
		main = ImageTk.PhotoImage(Image.open("assets/img01.png"))
		# Create a Label Widget to display the text or Image
		self.label = Label(self.root, image = main)
		self.label.image = main

		# TODO:	input box for text 
		# TODO: Dropdownlist for different voice actors
		# Upon changing the selection, change the corresponding images as well from the background
		self.description = Label(self.frame, text="TYPE SOMETHING TO THE FOLLOWING FIELD")
		self.entry = Entry(self.frame, width=50)

		VOICES = ['MIO', 'CHANGU', 'DUCKGU', 'JAMMIN', "AHRI", "DUCKHOO", "BORA", "JIAN"]
		
		var = StringVar(self.frame)
		var.set(VOICES[0])
		opt=OptionMenu(self.frame, var, *VOICES)
		
	
		# Return keycode = 55 event triggers to submit the entered text
		# TODO: Create a submit button for submission - SELECTION
		# () => submit(self.description, voiceactor-selection)		
		self.entry.bind('<Return>', lambda x=None: self.submit(self.entry.get(), str(var.get())))
		
		
		# Grid Setup
		#self.label.grid(row=0, column=0)
		self.label.pack()
		opt.grid(row=0, column=1)
		self.description.grid(row=0, column=0)
		self.entry.grid(row=1, column=0, columnspan=2)
		self.bQuit.grid(row=2, column=0, columnspan=2)
		
		
	def start_move(self, e):
		self.root.x = e.x
		self.root.y = e.y
	def stop_move(self, e):
		self.root.x = None
		self.root.y = None
	def do_move(self, e):
		deltax = e.x - self.root.x
		deltay = e.y - self.root.y
		x = self.root.winfo_x() + deltax
		y = self.root.winfo_y() + deltay
		self.root.geometry(f"+{x}+{y}")

	def submit(self, text, voiceactor):
		t1 = Thread(target = self.work, args=(text,voiceactor,))
		t1.start()

	def work(self, text,voiceactor):
		self.lock.acquire() 
		print("Entered Text: " + text + "\nVoice actor: " + str(voiceactor))
		# Send the request to client.py and play the audio
		client.audio_play(client.generate_audio(text, self.count, voiceactor))
		self.count = self.count + 1
		if (self.count == 9):
			self.count = 0
			client.clearfiles()
		self.lock.release()
		return
		
	

def main():
	#TODO: remove test cases when imported
	app = TypeCastApp()
	app.root.mainloop()

	return

if __name__ == "__main__": main()
