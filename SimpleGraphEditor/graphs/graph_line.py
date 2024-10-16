from .graph import SGEGraph, GRAPH_TYPE

class SGEGraphLine(SGEGraph):
    def __init__(self, plot):
        super().__init__(GRAPH_TYPE.LINE)
        self.title = "Title"
        self.xLabel = "X-Axis"
        self.yLabel = "Y-Axis"
        self.dataX = []
        self.dataY = []
        #TODO: Merge data w/ zip and store in SGEGraph

        self.plot = plot
        self.plot.set_aspect('equal', adjustable='datalim')
        self.initPlot()
        #TODO: Fix annotations - Visible if this is moved to plot_editor.py, but doesn't work right
        self.annotation = self.plot.text(0, 0, '', fontsize=12, ha='center', va='center', color='black',
                                         bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.5))


    def initPlot(self):
        if (len(self.dataX) > 0):
            if (isinstance(self.dataX[0], int) or isinstance(self.dataX[0], float)):
                self.plot.set_xlim(min(self.dataX) - 1, max(self.dataX) + 1)
            self.plot.set_ylim(min(self.dataY) - 1, max(self.dataY) + 1)
        self.plot.plot(self.dataX, self.dataY)
        self.plot.set_title(self.title)
        self.plot.set_xlabel(self.xLabel)
        self.plot.set_ylabel(self.yLabel)

    def getTitle(self):
        return self.title

    def getXLabel(self):
        return self.xLabel

    def getYLabel(self):
        return self.yLabel

    def setXLabel(self, label):
        self.xLabel = label
        self.plot.set_xlabel(label)

    def setYLabel(self, label):
        self.yLabel = label
        self.plot.set_ylabel(label)

    def getXData(self):
        return self.dataX

    def getYData(self):
        return self.dataY

    def setXData(self, newData):
        self.dataX = newData

    def setYData(self, newData):
        self.dataY = newData

    def updatePlot(self, canvas):
        self.plot.clear()
        self.initPlot()
        canvas.draw()

    def setTitle(self, title):
        self.title = title
        self.plot.set_title(title)

    def setXLabel(self, label):
        self.xLabel = label
        self.plot.set_xlabel(label)

    def setYLabel(self, label):
        self.yLabel = label
        self.plot.set_ylabel(label)

    def sortByX(self):
        if (len(self.dataX) < 2):
            return
        combined = list(zip(self.dataX, self.dataY))
        sorted_combined = sorted(combined)

        sortedX, sortedY = zip(*sorted_combined)

        self.dataX = list(sortedX)
        self.dataY= list(sortedY)
