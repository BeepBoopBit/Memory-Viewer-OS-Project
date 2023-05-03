# we'll mainly use this for sleep function
import time


# Contains an abstraction of the memory
class MemoryBlock:
    
    # Called at construction
    def __init__(self, availableMemory, jobs = []) -> None:
        
        # Initialize variables
        self.availableMemory = availableMemory # available memory for processing
        self.jobs = []  # current processing jobs
        
        # Add all the given job to the MemoryBlock
        for job in jobs:
            self.addJob(job)
        
    # returns a list of jobs
    def getJobs(self) -> list:
        return self.jobs

    # returns the current availableMemory
    def getAvailableMemory(self) -> int:
        return self.availableMemory
    
    # remove a certain value of memory
    def removeMemory(self, value=-1) -> None:
        self.availableMemory -= value

    # Add a job in the memory block if we can handle it
    # return true if successful
    def addJob(self, job: list()) -> bool:
        
        # if we have enough memory for the job
        if self.availableMemory >= job[0]:
            # decrement the availble memory by the job usage
            self.availableMemory -= job[0]
            
            # and append it to the job
            self.jobs.append(job)
            
            # return true if successful
            return True
        
        # False if not
        return False
    
    # decrement all jobs in the memory block by 1
    def processAllJobs(self) -> None:
        
        # use for reference
        jobIndexUsed = 0
        
        # loop through all the jobs
        for jobIndex in range(len(self.jobs)):
            
            # decrement a job usage by 1
            self.jobs[jobIndexUsed][1] -= 1
            
            # if it's less than or to zero, then it's time to delete it
            if(self.jobs[jobIndexUsed][1] <= 0):
                
                # restore the used memory in the block
                self.availableMemory += self.jobs[jobIndexUsed][0]
                
                # delete the job in the list of jobs
                del self.jobs[jobIndexUsed]
                
                # and decrement the reference index
                jobIndexUsed -= 1
                
            # increase the reference index
            jobIndexUsed += 1

class MemoryManagement:
    def __init__(self, MemoryList: list()):
        
        # Raise an error if the memory list is empty
        if(len(MemoryList) <= 0):
            raise "No Memory"
        
        # Initialize the Memory List
        self.memoryList = []
        
        # Append the memory in a form of: [ [Memory, [Job,Job]], [Memory, [Job,Job]] ]
        for memory in MemoryList:
            self.memoryList.append(MemoryBlock(memory))

        # Initialize Threads
        self.threads = []
        
        # Queue for the processes
        self.processQueue = []
        # Flags
        # [0]
        # 0 - compaction
        # 1 - coalescing
        # [1]
        # -1 - stop
        # 0 - pause
        # 1 - start
        # [2]
        # 0 - first fit
        # 1 - next fit
        # 2 - best fit
        self._flags = [1, 1, 2]
        
        # How fast we process each processes
        self._sleepValue = 0.1;
        
        # Total process done by the application
        self._totalProcessing = 0;
        
        # The index for the next-fit algorithm
        self._nextFitAlgorithmIndex = 0;
    
    # Setter of the sleep value
    def setSleepValue(self, seconds):
        self._sleepValue(seconds)
    
    # Setter of the flags
    def setFlags(self, index, value):
        self._flags[index] = value
    
    # Adder of process in the process queue
    def addProcess(self, process, time):
        self.processQueue.append([process, time])
    
    # Getter of the total process time
    def getTotalProcessingTime(self):
        return self._totalProcessing
    
    # We don't need this now, since we gave the threading responsibilty
    # to the GUI
    # however, we'll just stay as is as abstraction
    
    # start the background processing
    def startProcessing(self):
        self.__processing()
    
    # Adder of memory to the memory list
    def addMemory(self, memoryList: list()):
        for memory in memoryList:
            self.memoryList.append(MemoryBlock(memory))

    # Getter of memory list
    def getMemoryList(self):
        return self.memoryList

    # Calls the processing of the processor
    def __processing(self):
        
        # While the flag is not set to stop
        while self._flags[1] != -1 and len(self.processQueue) > 0:
            
            # Do the processes
            self.__processQueue()
            self.__processJob()
            
            # Pause
            while self._flags[1] == 0:
                pass
        
        # For debugging
        print("The process is not stopped")
        
        # Reset the values (after stopping the processing)
        self.processQueue = []
        self.memoryList = []

    def __processJob(self):
        
        # id for reference
        id = 0
        
        # jobStr for writing in the jobs.dat
        jobsStr = ""
        for memoryBlock in self.memoryList:
            
            # Decrement all Jobs in side of the memory block
            memoryBlock.processAllJobs()
            self._totalProcessing += 1
            
            # Get the necessarily information
            availableMemory = memoryBlock.getAvailableMemory()
            memoryJobs = memoryBlock.getJobs()
            
            # If a memory block becomes useless, then remove it to the list
            if availableMemory == 0 and len(memoryJobs) <= 0:
                del self.memoryList[id]
                break
            else:
            # Else, print it out
            
                # loop through all the jobs, transform it, and store it
                for jobs in memoryJobs:
                    jobsStr += str(jobs[0]) + ',' + str(jobs[1]) + '\n'
                
                # Debugging
                print(f"[{id}] Block ({availableMemory}): {memoryJobs}")

           # For ending of memory block (use for data reading)
            jobsStr += ';;;\n'
            
            # Sleep for sycronosity and to make sure that we can follow the data process
            time.sleep(self._sleepValue)
            
            # Increment ID
            id += 1

        # Open the file data to write
        fileData = open("jobs.dat", 'w')
        
        # Write the jobsStr to the file
        fileData.write(jobsStr)     
        
        # close it to save
        fileData.close()   

    # Processing the process queue
    def __processQueue(self):

        # If there's no value anymore in the process queue, return
        if (len(self.processQueue) <= 0):
            return        
        
        # Use as a flag to signify whether we need to do fragmentation solutions
        noAvailableMemory = True
        
        # First Fit
        # https://www.tutorialspoint.com/cplusplus-program-for-first-fit-algorithm-in-memory-management#:~:text=First%20Fit%20Algorithm%20is%20the,block%20to%20the%20coming%20process.
        if self._flags[2] == 0:
            # idx for index reference
            idx = 0
            
            # loop through all the memoryblock in the list
            for memoryBlock in self.memoryList:
                
                # If we are able to add it
                if len(self.processQueue) > 0 and memoryBlock.addJob(self.processQueue[0]):
                    # Delete the process queue
                    del self.processQueue[0]
                    
                    # mark the flag as False 
                    noAvailableMemory = False
                    
                    # And save the index in case the user change for the algorithm
                    self._nextFitAlgorithmIndex = idx
                    
                    # break as we've successfully added a job
                    break
                
                # Increment idx
                idx =+ 1
                
                # Increment total processing
                self._totalProcessing += 1
                
            #  if the _nextFitAlgorithmIndex surprass the current memory List
            # reset it
            if self._nextFitAlgorithmIndex >= len(self.memoryList):
                self._nextFitAlgorithmIndex = 0
        
        # Next Fit
        # https://www.geeksforgeeks.org/program-for-next-fit-algorithm-in-memory-management/
        elif self._flags[2] == 1:
            
            # Start at the index last used
            idx = self._nextFitAlgorithmIndex
            
            # loop through the memory block starting at the last used index
            for memoryBlock in range(self._nextFitAlgorithmIndex, len(self.memoryList)):
                
                # If we are able to add it
                if len(self.processQueue) > 0 and self.memoryList[memoryBlock].addJob(self.processQueue[0]):
                    
                    # Delete the process queue
                    del self.processQueue[0]
                    
                    # mark the flag as False 
                    noAvailableMemory = False
                    
                    # Save the index for later use
                    self._nextFitAlgorithmIndex = idx
                    
                    # break as we've successfully added a job
                    break;
                
                # increment idx
                idx += 1
                
                # Increment Total processing
                self._totalProcessing += 1
                
            #  if the _nextFitAlgorithmIndex surprass the current memory List
            # reset it
            if self._nextFitAlgorithmIndex >= len(self.memoryList):
                self._nextFitAlgorithmIndex = 0

        # Best Fit
        # https://www.geeksforgeeks.org/program-best-fit-algorithm-memory-management/
        elif self._flags[2] == 2:
            
            # initialize the currentLowest index and value to store
            # the memory that b est fir the flag
            currentLowestIndex, currentLowestValue = float('inf'), float('inf')
            
            # Flag whehter we found something to change or not
            toChange = False
            
            # idx for reference
            idx = 0
            
            # loop through all the memory block in the memory list
            for memoryBlock in self.memoryList:
                
                # get the necessarily information
                currentAvailableMemory = memoryBlock.getAvailableMemory()
                processMemoryUsage = self.processQueue[0][0]
                
                # If the current memory block has enough storage for the job
                if len(self.processQueue) > 0 and currentAvailableMemory >= processMemoryUsage:
                    
                    # and if it's less than the current lowest value
                    if currentLowestValue > processMemoryUsage:
                        
                        # assign the variables to it
                        currentLowestIndex = idx
                        currentLowestValue = processMemoryUsage

                        # and mark the flag to change
                        toChange = True
                # increment idx
                idx += 1
                
                # increment total processing
                self._totalProcessing += 1
            
            # if we found somethign to change
            if toChange:
                # add as job to the memory block we found it best fit
                self.memoryList[currentLowestIndex].addJob(self.processQueue[0])
                
                # update the next fit algorithm index
                self._nextFitAlgorithmIndex = currentLowestIndex
                
                # delete the job in the process queue
                del self.processQueue[0]
                
                # and mark the flag as false
                noAvailableMemory = False
                
            #  if the _nextFitAlgorithmIndex surprass the current memory List
            # reset it
            if self._nextFitAlgorithmIndex >= len(self.memoryList):
                self._nextFitAlgorithmIndex = 0
                
        # If there's not enough memory for a job, we'll do fragmenetation solutions
        if noAvailableMemory:
            if self._flags[0] == 0:
                self.__compaction(self.processQueue[0])
            else:
                self.__coalescing(self.processQueue[0])
    
    # Compaction algorithm
    def __compaction(self, job):
        
        # list of available memory to be used
        availableMemory = []
        
        # list of memory indexes of those available memory
        memoryIndex = []
        
        # and memoryIndexValue for appending in the memoryIndex
        memoryIndexValue = 0
        
        # loop through all the memory block of the memory list
        for memoryBlock in self.memoryList:
            
            # append that memory block availble memory to the available memory
            availableMemory.append(memoryBlock.getAvailableMemory())
            
            # append its index in the memory Index
            memoryIndex.append(memoryIndexValue)
            
            # increment the index value
            memoryIndexValue += 1
            
            # and increment the processing time
            self._totalProcessing += 1
            
        # get the sum of all those available memory
        summation = sum(availableMemory)
        
        # if it's enough to do the job
        if summation >= job[0] and summation != 0:  
            
            # loop through all the memory list          
            for memoryBlockIndex in range(0,len(self.memoryList)):
                # remove the memory we're going to use
                self.memoryList[memoryBlockIndex].removeMemory(availableMemory[memoryBlockIndex])
                
                # increment processing time
                self._totalProcessing += 1
                
            # then append the new memory block in the memory list
            self.memoryList.append(MemoryBlock(summation,[job]))

    # Coalescing Algorithm
    def __coalescing(self, job):
        
        # list of available memory to be used
        availableMemory = []
        
        # list of memory indexes of those available memory
        memoryIndex = []
        
        # idx for index reference
        idx = 0
        
        # loop through the memory block in the memory list
        for memoryBlock in self.memoryList:
            
            # get the necessary information
            memoryBlockAvailableMemory = memoryBlock.getAvailableMemory()
            
            # If it's > 0 then that means we can use it and it's still adjacent
            if(memoryBlockAvailableMemory > 0):
                # append it to the available memory as well as its index
                availableMemory.append(memoryBlockAvailableMemory)
                memoryIndex.append(idx)

            # However, if it's zero, that means that that is the end of the adjacent block, so we'll process it
            else:
                
                # Get the summation of the available memory
                summation = sum(availableMemory)
                
                # if it's enough to do the job
                if summation >= job[0]:
                    
                    # Decrease every available memory
                    for index in memoryIndex:
                        self.memoryList[index].removeMemory(self.memoryList[index].getAvailableMemory())

                        # while increasing the processing time
                        self._totalProcessing += 1
                    # append the new memory block in the memory list with the new job and the available memory
                    self.memoryList.append(MemoryBlock(summation, [job]))
                
                # reset the available memory and memory index for new adjacent blocks
                availableMemory = []
                memoryIndex = []
            idx += 1
            self._totalProcessing += 1
            
            
        # Get the summation of the available memory
        summation = sum(availableMemory)

        # if it's enough to do the job
        if summation >= job[0]:

            # Decrease every available memory
            for index in memoryIndex:
                self.memoryList[index].removeMemory(self.memoryList[index].getAvailableMemory())
                
                # while increasing the processing time
                self._totalProcessing += 1
                
            # append the new memory block in the memory list with the new job and the available memory
            self.memoryList.append(MemoryBlock(summation, [job]))
        
    def debugStart(self):
        self.addProcess(1,14)
        self.addProcess(5,11)
        self.addProcess(7,12)
        self.addProcess(2,12)
        self.addProcess(8,14)
        self.addProcess(3,15)
        self.addProcess(7,16)
        self.addProcess(9,17)
        self.addProcess(2,18)
        self.addProcess(2,19)
        self.addProcess(3,11)
        self.addProcess(5,12)
        self.addProcess(7,15)
        self.addProcess(7,14)
        self.addProcess(2,15)
        self.addProcess(3,16)
        self.addProcess(4,17)
        self.addProcess(6,18)
        self.addProcess(7,19)
        self.addProcess(9,11)
        self.addProcess(3,12)
        self.addProcess(1,16)
        self.addProcess(6,14)
        self.addProcess(2,15)
        self.addProcess(3,16)
        self.addProcess(5,17)
        self.addProcess(8,18)
        self.addProcess(1,19)
        self.addProcess(3,12)
        self.addProcess(4,11)
        self.addProcess(7,19)
        self.addProcess(9,11)
        self.addProcess(3,12)
        self.addProcess(1,16)
        self.addProcess(6,14)
        self.addProcess(2,15)
        self.addProcess(3,16)
        self.addProcess(5,17)
        self.addProcess(8,18)
        self.addProcess(1,19)
        self.addProcess(3,12)
        self.addProcess(4,11)
        self.addProcess(7,19)
        self.addProcess(9,11)
        self.addProcess(3,12)
        self.addProcess(1,16)
        self.addProcess(1,16)
        self.addProcess(6,14)
        self.addProcess(2,15)
        self.addProcess(3,16)
        self.addProcess(5,17)
        self.addProcess(8,18)
        self.addProcess(1,19)
        self.addProcess(3,12)
        self.addProcess(4,11)
        self.addProcess(7,19)
        self.addProcess(9,11)
        self.addProcess(3,12)
        self.addProcess(1,16)
        self.addProcess(1,16)
        self.addProcess(6,14)
        self.addProcess(2,15)
        self.addProcess(3,16)
        self.addProcess(5,17)
        self.addProcess(8,18)
        self.addProcess(1,19)
        self.addProcess(3,12)
        self.addProcess(4,11)
        self.addProcess(7,19)
        self.addProcess(9,11)
        self.addProcess(3,12)
        self.addProcess(1,16)
        self.addProcess(1,16)
        self.addProcess(6,14)
        self.addProcess(2,15)
        self.addProcess(3,16)
        self.addProcess(5,17)
        self.addProcess(8,18)
        self.addProcess(1,19)
        self.addProcess(3,12)
        self.addProcess(4,11)
        self.addProcess(7,19)
        self.addProcess(9,11)
        self.addProcess(3,12)
        self.addProcess(1,16)
        self.addProcess(6,14)
        self.addProcess(2,15)
        self.addProcess(3,16)
        self.addProcess(5,17)
        self.addProcess(8,18)
        self.addProcess(1,19)
        self.addProcess(3,12)
        self.addProcess(4,11)
        self.addProcess(7,19)
        self.addProcess(9,11)
        self.addProcess(3,12)
        self.addProcess(1,16)
        self.addProcess(6,14)
        self.addProcess(2,15)
        self.addProcess(3,16)
        self.addProcess(5,17)
        self.addProcess(8,18)
        self.addProcess(1,19)
        self.addProcess(3,12)
        self.addProcess(4,11)
        self.addProcess(7,19)
        self.addProcess(9,11)
        self.addProcess(3,12)
        self.addProcess(1,16)
        self.addProcess(6,14)
        self.addProcess(2,15)
        self.addProcess(3,16)
        self.addProcess(5,17)
        self.addProcess(8,18)
        self.addProcess(1,19)
        self.addProcess(3,12)
        self.addProcess(4,11)
        self.startProcessing()
        
if __name__ == "__main__":
    MemoryManagement([30,20,10]).debugStart()