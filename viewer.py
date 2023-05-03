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


# The main GUI class for the MemoryViewerGUI
class MemoryViewerGUI(QtWidgets.QMainWindow):
    
    # Initialization after creation of the class
    def __init__(self):

        # Initialize the parent class
        super(MemoryViewerGUI,self).__init__()

        # Load the UI created from UI Designer
        uic.loadUi("MemoryViewerGUI.ui", self)
        
        # Set-up Initial Variables
        self.tableValues = []                     # Use to store values to be displayed in the table
        self.timerReader = QTimer()               # Timer for Reading File Data
        self.timerLoading = QTimer()              # Timer for Loading the Value to the table
        self.timerReader.timeout.connect(self.readData)       # connect the timer to the appropriate function
        self.timerLoading.timeout.connect(self.loadValues)    # connect the timer to the appropriate function
        
        # Show the GUI
        self.show()
    
    # Start the background processes
    def startProcess(self):
        self.timerReader.start(10)
        self.timerLoading.start(10)
        
    
    # Read the data in the job.dat file
    def readData(self):
        # reset the table of values
        self.tableValues = []
        
        # Open the jobs.dat file for reading
        fileData = open("jobs.dat", 'r')
        
        # Read a line in the jobs.dat
        dataValue = fileData.readline()
        
        # Create a temporaray List of Values
        tempListvalues = []
        
        # Loop until there's no data left
        while dataValue:
            
            # If it's the end of the memory block
            if dataValue != ';;;\n' and dataValue != ';;;':
                # Split the read line 
                separatedStr = dataValue.split(',')
                
                # Format the string for displaying
                tempStr = "<" + separatedStr[0] + "," + separatedStr[1][:-1] + ">"
                
                # Append it the temp list of value
                tempListvalues.append(tempStr)
            else:
                # if it's the end of the block, then it's time to append it to the real
                # table values
                self.tableValues.append(tempListvalues)
                
                # and reset the temporary for new memory block 
                tempListvalues = []
                
            # Then it's time to read the file again
            dataValue = fileData.readline()

        # We shouldn't forget to close the file data
        fileData.close()
        
    
    # Load the values into the table
    def loadValues(self):
        
        # Create a new table widget
        newTable = QTableWidget()

        # Remove all existing tab
        while self.TabViewWidget.count() != 0:
            self.TabViewWidget.removeTab(0)
            

        # List of column names
        columnNames = []
        
        # loop through how many columns (number of memory block)
        for i in range(0, len(self.tableValues)):
            
            # insert a new column (since we don't have one yet) 
            newTable.insertColumn(newTable.columnCount())
            
            # Set it to be stretchable
            newTable.horizontalHeader().setSectionResizeMode(newTable.columnCount()-1, QHeaderView.Stretch)

            # append its name to the columnNames
            columnNames.append("Memory Block [" + str(i) + "]")
        
        # set all the columns to the initialized column names
        newTable.setHorizontalHeaderLabels(columnNames)
        

        # Use to refered to the current column for displaying
        columnIndex = 0
        
        # loop through all the memory blocks
        for memoryBlock in self.tableValues:
            
            # Signifies the current row we are in
            numberOfRows = 0
            
            # loop through all the jobs in the memory block
            for job in memoryBlock:
                
                # if the number of rows is greater than the available row in the table
                if numberOfRows >= newTable.rowCount():
                    # Create a new row with no data in it
                    newTable.insertRow(newTable.rowCount())
                
                # set the row data in the numberOfRow at columnIndex with the job as it's display value
                newTable.setItem(numberOfRows, columnIndex, QTableWidgetItem(job))
                
                # Increment the number of row
                numberOfRows += 1
                
            # Increment the Column Index
            columnIndex += 1
            
        # Set the tab name to processor [0]
        self.TabViewWidget.addTab(newTable, "Processor " + str(0))

if __name__ == "__main__":
    _app = QApplication([])
    _mainGUI = MemoryViewerGUI()
    _mainGUI.startProcess()
    _app.exec()