# This is the base PyQT module that we will use to create widgets, and load the UI that we've created
# using the pyqt designer
# https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QWidget.html
# https://intellij-support.jetbrains.com/hc/en-us/community/posts/9522873838866-Problem-with-uic-module-from-PyQt5
# https://www.programcreek.com/python/example/96001/PyQt5.uic.loadUi
from PyQt5 import QtWidgets, uic

# QApplication and QMessage box are the one that we are going to use mainly
# QApplication is use for executing the main application loop
# QMessageBox is used for dialogue boxes for errors
# https://www.geeksforgeeks.org/pyqt5-qapplication/
# https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QMessageBox.html
from PyQt5.QtWidgets import QApplication, QLabel, QTableWidget,QTableWidgetItem,QMessageBox

# QRunnable is used for threading in the Qt World (the inerited class)
# QThreadPool is used for same here (the starter of the thread)
# https://www.pythontutorial.net/pyqt/qthreadpool/
from PyQt5.QtCore import QRunnable, QThreadPool,QTimer


# we'll mainly use this for sleep function
import time

# this is my own module, Processor contain the MemoryManagement class that
# is use to manage the processes of jobs, the alogirthms use, and the fragmentation solutions
from Processor import MemoryManagement


# A thread process for PyQT
# Unfortunately we can't really do the normal threading using PyQT since
# It requires the managemenet of the PyQT Objects to be in the parent or the main thread

# This class is used to handle the processing in the memory
class WorkerProcessor(QRunnable):
   
    # Initializing the Default Memory Size of the Memory Management 
    def __init__(self):
        super().__init__()
        self._manager = MemoryManagement([25,25])
    
    # This will be called after the start of this class
    def run(self):
        self._manager.debugStart()

    # This is an auxillary function for the use of other classes that requires information
    # from the memory management
    def getManager(self):
        return self._manager

# We've put it in global to make things a lot easier
workerProcessor = WorkerProcessor()


# The main GUi class for the AddNewProcessWindow
class AddNewProcessGUI(QtWidgets.QMainWindow):
    
    # Initialization after creation of the class
    def __init__(self):
        
        # Initialize the parent class
        super(AddNewProcessGUI,self).__init__()
        
        # Load the UI created from UI Designer
        uic.loadUi("AddNewProcessGUI.ui", self)
        
        # Connect the fButton_Confirm function to the Button_confirm button
        self.Button_Confirm.clicked.connect(self.fButton_Confirm)
        
        # Connect the fButton_Back function to the Button_Back button
        self.Button_Back.clicked.connect(self.fButton_Back)

    # When the confirm button is click
    def fButton_Confirm(self):
        try:
            # Try to get and convert the values inside of the TextFields
            # and store them
            processTime = int(self.TextField_ProcessTime.toPlainText())
            usageTime = int(self.TextField_MemoryUsage.toPlainText())

            # Then well just add the processs to our MemoryManagement
            workerProcessor.getManager().addProcess(processTime, usageTime)
            
            # Go back to the initial window
            self.fButton_Back()
        except:
            # If we can't store it, pop-up an error message
            msg = QMessageBox()
            msg.setWindowTitle("ERROR!!!")
            msg.setText("Information Must Be A Number!!!")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.show()
    
    def fButton_Back(self):
        
        # Set the window to be invisible 
        self.setVisible(False)
        
# The main GUi class for the FragmentationSolutionGUI
class FragmentationSolutionGUI(QtWidgets.QMainWindow):
    
    # Initialization after creation of the class
    def __init__(self):
        
        # Initialize the parent class
        super(FragmentationSolutionGUI,self).__init__()
        
        # Load the UI created from UI Designer
        uic.loadUi("FragmentationSolutionGUI.ui", self)
        
        # Connect the fButton_Confirm function to the Button_confirm button
        self.Button_Confirm.clicked.connect(self.fButton_Confirm)
        
        # Connect the fButton_Back function to the Button_Back button
        self.Button_Back.clicked.connect(self.fButton_Back)
        
        # Set the radio button to true, so that we have some
        # initial value
        self.RadioButton_Coalescing.setChecked(True)

    def fButton_Confirm(self):
        try:
            # check if the coalescing button is marked
            isCoalescing = self.RadioButton_Coalescing.isChecked()
            
            # Set the flag dependent on the marked algorithm
            workerProcessor.getManager().setFlags(0,isCoalescing)
            
            # Go back to the initial window
            self.fButton_Back()
        except:
            
            # If we can't store it, pop-up an error message
            msg = QMessageBox()
            msg.setWindowTitle("ERROR!!!")
            msg.setText("Information Must Be A Number!!!")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.show()
    
    def fButton_Back(self):
        
        # Set the window to be invisible 
        self.setVisible(False)

# The main GUi class for the MemoryAllocationAlgorithmGUI
class MemoryAllocationAlgorithmGUI(QtWidgets.QMainWindow):
    
    # Initialization after creation of the class
    def __init__(self):
        
        # Initialize the parent class
        super(MemoryAllocationAlgorithmGUI,self).__init__()
        
        # Load the UI created from UI Designer
        uic.loadUi("MemoryAllocationAlgorithmGUI.ui", self)
        
        # Connect the fButton_Confirm function to the Button_confirm button
        self.Button_Confirm.clicked.connect(self.fButton_Confirm)

        # Connect the fButton_Back function to the Button_Back button
        self.Button_Back.clicked.connect(self.fButton_Back)

        # Set the radio button to true, so that we have some
        # initial value
        self.RadioButton_BestFit.setChecked(True)

    def fButton_Confirm(self):
        try:
            # Check if one of the Radiobutton is checked
            isBestFit = self.RadioButton_BestFit.isChecked()
            isFirstFit = self.RadioButton_FirstFit.isChecked()
            
            # A short hand if-else statement to know understand the value
            value = 2 if isBestFit else 0 if isFirstFit else 1
            
            # Set the flag relative to the chosen algorithm
            workerProcessor.getManager().setFlags(0,value)
            
            # Go back to the initial window
            self.fButton_Back()
        except:
            
            # If we can't store it, pop-up an error message
            msg = QMessageBox()
            msg.setWindowTitle("ERROR!!!")
            msg.setText("Information Must Be A Number!!!")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.show()
    
    def fButton_Back(self):
        
        # Set the window to be invisible 
        self.setVisible(False)
        
# The main GUi class for the AddMemoryBlockGUI
class AddMemoryBlockGUI(QtWidgets.QMainWindow):
    
    # Initialization after creation of the class
    def __init__(self):
        
        # Initialize the parent class
        super(AddMemoryBlockGUI,self).__init__()

        # Load the UI created from UI Designer
        uic.loadUi("AddMemoryBlockGUI.ui", self)
        
        # Connect the fButton_Confirm function to the Button_confirm button
        self.Button_Confirm.clicked.connect(self.fButton_Confirm)

        # Connect the fButton_Back function to the Button_Back button
        self.Button_Back.clicked.connect(self.fButton_Back)

    # When the confirm button is click
    def fButton_Confirm(self):
        try:
            # Get the data Value in the text field
            dataValue = self.TextField_MemoryBlock.toPlainText()
            
            # Split the value by ','
            splittedValue = dataValue.split(',')
            
            # then convert each into ints
            intValues = []
            for value in splittedValue:
                intValues.append(int(value))
            
            # after that, just add all of it to the memory
            workerProcessor.getManager().addMemory(intValues)
            
            # Go back to the initial window
            self.fButton_Back()
        except:
            
            # If we can't store it, pop-up an error message
            msg = QMessageBox()
            msg.setWindowTitle("ERROR!!!")
            msg.setText("Information Must Be A Number!!!")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.show()
    
    def fButton_Back(self):
        
        # Set the window to be invisible 
        self.setVisible(False)
  

class MainGUI(QtWidgets.QMainWindow):
    
    # Initialization after creation of the class
    def __init__(self):
        
        # Initialize the parent class
        super(MainGUI,self).__init__()
        
        # Load the UI created from UI Designer
        uic.loadUi("MainGUI.ui", self)
        
        # Set-up initial values
        self._threadPool = QThreadPool() # Use for threading
        self.windows = []   # Use for showing GUI
        self._manager = None # The instance of the MemoryManagement class

        # Flag for restarting the BackgroundProcess
        # [0] restart
        # 0 -> Continue
        # 1 -> Restart
        self._flag = [0]
        
        # Connect all the buttons to their corresponding functions
        self.connectButtonSignals()
        
        # Show the GUI
        self.show()


    # Connect all the buttons to their corresponding functions
    def connectButtonSignals(self):
        
        # For standard Buttons
        self.Button_Start.clicked.connect(self.fButton_Start)
        self.Button_Pause.clicked.connect(self.fButton_Pause)
        self.Button_Add.clicked.connect(self.fButton_Add)
        self.Button_Stop.clicked.connect(self.fButton_Stop)
        
        # For Algorithms
        self.Button_FragmentationSolution.clicked.connect(self.fButton_FragmentationSolution)
        self.Button_MemoryAllocation.clicked.connect(self.fButton_MemoryAllocation)
        self.Button_ShowTotalProcessingTime.clicked.connect(self.fButton_ShowTotalProcessingTime)
        self.Button_AddMemoryBlock.clicked.connect(self.fButton_AddMemoryBlock)

    def fButton_Start(self):
        # To make sure that everything is syncronize
        # We'll put it to sleep for 2 seconds.
        time.sleep(2)
        
        # we'll check the flag if we need to restart the background process
        if self._flag[0] == 1:
            global workerProcessor 
            workerProcessor = WorkerProcessor()
            self._flag[0] = 0
        
        
        # Disable the add button to prevent memory conflicts 
        self.Button_Add.setEnabled(False)
        
        # The instance of the MemoryManagement class
        self._manager = workerProcessor.getManager()
        
        # Set the manager flag to continue
        self._manager.setFlags(1,1)
        
        # Use for the threading
        self._threadPool.start(workerProcessor)
    
    def fButton_Add(self):
        # Show the AddNewProcessGUI
        self.window = AddNewProcessGUI()
        self.window.show()
    
    def fButton_Pause(self):
        # Pause the background-process by setting-up the flag
        self.Button_Add.setEnabled(True)
        self._manager.setFlags(1,0)

    def fButton_Stop(self):
        # Stop the background-process by setting-up the flag
        self.Button_Add.setEnabled(True)
        self._manager.setFlags(1,-1)
        self._flag[0] = 1

    def fButton_MemoryAllocation(self):
        # Show the MemoryAllocationAlgorithmGUI
        self.window = MemoryAllocationAlgorithmGUI()
        self.window.show()
    
    def fButton_FragmentationSolution(self):
        # Show the FragmentationSolutionGUI
        self.window = FragmentationSolutionGUI()
        self.window.show()
        
    def fButton_AddMemoryBlock(self):
        # Show the AddMemoryBlockGUI
        self.window = AddMemoryBlockGUI()
        self.window.show()
        pass
    
    def fButton_ShowTotalProcessingTime(self):
        # Show the total processing time through message box
        msg = QMessageBox()
        msg.setWindowTitle("Total Processing Time")
        msg.setText(f"Total Processing Time: {workerProcessor.getManager().getTotalProcessingTime()}")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()
        
    
    

if __name__ == "__main__":
    _app = QApplication([])
    _mainGUI = MainGUI()
    _app.exec()