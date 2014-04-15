
import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

class Form2(Form):
	def __init__(self):
		self.InitializeComponent()
	
	def InitializeComponent(self):
		self._label1 = System.Windows.Forms.Label()
		self.SuspendLayout()
		# 
		# label1
		# 
		self._label1.BackColor = System.Drawing.Color.White
		self._label1.Location = System.Drawing.Point(72, 73)
		self._label1.MinimumSize = System.Drawing.Size(0, 2)
		self._label1.Name = "label1"
		self._label1.Size = System.Drawing.Size(100, 23)
		self._label1.TabIndex = 0
		self._label1.Text = "label1"
		self._label1.MouseDown += self.Label1MouseDown
		# 
		# Form2
		# 
		self.ClientSize = System.Drawing.Size(292, 266)
		self.Controls.Add(self._label1)
		self.Name = "Form2"
		self.Text = "Form2"
		self.ResumeLayout(False)


	def Label1MouseDown(self, sender, e):
		pass