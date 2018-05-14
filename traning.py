import subprocess
import shutil
import wx

IDLE_SAMPLE_RATE = 1500
SAMPLE_RATE = 200

class MainWindow(wx.Frame):
	title = 'Data Acquisition'

	def __init__(self):
		wx.Frame.__init__(self, None, title=self.title, size=(660,330))
		# Create GUI
		self.create_main_panel()

		self.recording = False
		self.t = 0

	def create_main_panel(self):
		# Panels
		self.img_panel = wx.Panel(self)
		self.joy_panel = wx.Panel(self)
		self.record_panel = wx.Panel(self)

		# Images
		img = ImageGrab.grab(bbox=(10,10,500,500))

		self.image_widget = wx.StaticBitmap(self.img_panel, wx.ID_ANY, wx.Bitmap(img))

		# Recording
		self.txt_outputDir = wx.TextCtrl(self.record_panel, wx.ID_ANY, pos=(5,0), size=(320,30))
		self.txt_outputDir.ChangeValue("samples/")

		self.btn_record = wx.Button(self.record_panel, wx.ID_ANY, label="Record", pos=(335,0), size=(100,30))

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(self.img_panel, 0, wx.ALL, 5)
		sizer.Add(self.joy_panel, 0, wx.ALL, 5)

		mainSizer_v = wx.BoxSizer(wx.VERTICAL)
		mainSizer_v.Add(sizer, 0 , wx.ALL, 5)
		mainSizer_v.Add(self.record_panel, 0 , wx.ALL, 5)

		# finalize layout
		self.SetAutoLayout(True)
		self.SetSizer(mainSizer_v)
		self.Layout()

		def draw(self):
			# Image
			img = self.bmp.ConvertToImage()
			img = img.Rescale(320,240)
			self.image_widget.SetBitmap(img.ConvertToBitmap())

		def on_exit(self, event):
			self.Destroy()

if __name__ == '__main__':
	#subprocess.Popen(['C:\\Program Files\\BizHawk\\EmuHawk.exe'])
	app = wx.App()
	app.frame = MainWindow()
	app.frame.Show()
	app.MainLoop()
