import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Circle
import numpy as np

from SimpleGraphEditor.graphs.graph_line import SGEGraphLine

class SGEPlotEditor:
    def __init__(self):
        self.sortedX = True # Whether Xs need to be in ascending order

        self.root = tk.Tk()
        self.root.title("Simple Graph Editor")
        self.root.geometry("600x600")

        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=1)
        fig = Figure(figsize=(5,4), dpi=100)

        localPlot = fig.add_subplot(111)
        self.graph = SGEGraphLine(localPlot)
        self.graph.setTitle("Title")
        self.graph.setXLabel("X-Axis")
        self.graph.setYLabel("Y-Axis")
        #TODO: Might be worth zipping x and y together

        self.canvas = FigureCanvasTkAgg(fig, master=frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        self.createTable()
        self.populateTable()

        btnFrame = ttk.Frame(self.root)
        btnFrame.pack(side=tk.RIGHT, fill=tk.Y)
        addBtn = ttk.Button(btnFrame, text="Add Row", command=self.addRow)
        addBtn.pack(pady=5)
        delBtn = ttk.Button(btnFrame, text="Delete Row", command=self.deleteRow)
        delBtn.pack(pady=5)

        self.dataTable.bind("<Double-1>", self.dataTableDoubleClick)

        self.canvas.mpl_connect('button_press_event', lambda event: self.onDoubleClickCanvas(event) if event.dblclick else None)
        self.canvas.mpl_connect('motion_notify_event', self.onMouseMove)

    def start(self):
        self.populateTable()
        self.graph.updatePlot(self.canvas)
        self.root.mainloop()


    def onMouseMove(self, event):
        circleYThresh = 0.8
        dataX = self.graph.getXData()
        dataY = self.graph.getYData()
        if event.inaxes is not None:  # Check if mouse is in the axes
            #TODO: The following won't work when X data can be a string
            if event.xdata < min(dataX) or event.xdata > max(dataX):
                return

            for i in range(len(dataX) - 1):
                if dataX[i] <= event.xdata <= dataX[i + 1]:
                    # Linear interpolation to find the corresponding y value
                    slope = (dataY[i + 1] - dataY[i]) / (dataX[i + 1] - dataX[i])
                    intrpY = dataY[i] + slope * (event.xdata - dataX[i])
                    closestX = event.xdata
                    closestY = intrpY

                    if np.abs(event.ydata - closestY) >= circleYThresh:
                        self.graph.plot.patches.clear()
                        return
                    break

            self.graph.plot.patches.clear()

            circle = Circle((closestX, closestY), 0.1, color='red', alpha=0.8)
            self.graph.plot.add_artist(circle)

            self.graph.annotation.set_position((event.xdata, event.ydata))
            self.graph.annotation.set_text(f'X: {closestX:.2f}\nY: {closestY:.2f}')
            self.canvas.draw_idle()

    def getLabelClicked(self, event):
        titleLabel = self.graph.plot.title.get_window_extent(renderer=self.canvas.get_renderer())
        tbX,tbY,tbW,tbH = titleLabel.bounds
        if self.isClickInside(tbX, tbY, tbW, tbH, event.x, event.y):
            return "Title"
        xAxisLabel = self.graph.plot.xaxis.label.get_window_extent(renderer=self.canvas.get_renderer())
        xaX,xaY,xaW,xaH = xAxisLabel.bounds
        if self.isClickInside(xaX, xaY, xaW, xaH, event.x, event.y):
            return "X-Axis"
        yAxisLabel = self.graph.plot.yaxis.label.get_window_extent(renderer=self.canvas.get_renderer())
        yaX,yaY,yaW,yaH = yAxisLabel.bounds
        if self.isClickInside(yaX, yaY, yaW, yaH, event.x, event.y):
            return "Y-Axis"
        return ""

    def onDoubleClickCanvas(self, event):
        entryUpdate = None
        boundingBox = None
        labelToEdit = self.getLabelClicked(event)
        if (labelToEdit != ""):
            entryUpdate = tk.Entry(self.root)

        if labelToEdit == "Title":
            boundingBox = self.graph.plot.title.get_window_extent(renderer=self.canvas.get_renderer())
            entryUpdate.insert(0, self.graph.getTitle())
            def updatePlotTitle(event):
                self.graph.setTitle(entryUpdate.get())
                self.canvas.draw()
                entryUpdate.destroy()
            entryUpdate.bind('<Return>', updatePlotTitle)
        elif labelToEdit == "X-Axis":
            boundingBox = self.graph.plot.xaxis.label.get_window_extent(renderer=self.canvas.get_renderer())
            entryUpdate.insert(0, self.graph.getXLabel())
            def updatePlotXAxis(event):
                self.graph.setXLabel(entryUpdate.get())
                self.canvas.draw()
                entryUpdate.destroy()
            entryUpdate.bind('<Return>', updatePlotXAxis)
        elif labelToEdit == "Y-Axis":
            boundingBox = self.graph.plot.yaxis.label.get_window_extent(renderer=self.canvas.get_renderer())
            entryUpdate.insert(0, self.graph.getYLabel())
            def updatePlotYAxis(event):
                self.graph.setYLabel(entryUpdate.get())
                self.canvas.draw()
                entryUpdate.destroy()
            entryUpdate.bind('<Return>', updatePlotYAxis)

        if labelToEdit != "":
            bbX,bbY, _,bbH = boundingBox.bounds
            canvas_h = self.canvas.get_tk_widget().winfo_height()
            entryUpdate.place(x=bbX, y=canvas_h - bbY - bbH)
            entryUpdate.focus_set()
            entryUpdate.bind('<FocusOut>', lambda e: entryUpdate.destroy())

    def dataTableDoubleClick(self, event):
        region = self.dataTable.identify_region(event.x, event.y)
        if region != 'cell':
            return

        item = self.dataTable.selection()
        if item:
            colTag = self.dataTable.identify_column(event.x)
            colIndex = int(colTag.replace('#', '')) - 1
            selectY = self.dataTable.bbox(item)[1] # Bbox is (x, y, w, h)
            colX = 0
            for i in range(colIndex):
                colX += self.dataTable.column(f'#{i+1}')['width']


            entry = tk.Entry(self.root)
            entry.insert(0, self.dataTable.item(item)["values"][colIndex])
            entry.place(x=self.dataTable.winfo_x() + colX, y=self.dataTable.winfo_y() + selectY)
            entry.focus_set()

            def saveChange(event):
                newVal = entry.get()
                outVal = None
                try:
                    outVal = int(newVal)
                except ValueError:
                    try:
                        outVal = float(newVal)
                    except ValueError:
                        return

                if colIndex == 0:
                    self.graph.setXData(self.graph.getXData()[:self.dataTable.index(item)] +
                                        [outVal] + self.graph.getXData()[self.dataTable.index(item)+1:])
                elif colIndex == 1:
                    self.graph.setYData(self.graph.getYData()[:self.dataTable.index(item)] +
                                        [outVal] + self.graph.getYData()[self.dataTable.index(item)+1:])

                self.populateTable()
                self.graph.updatePlot(self.canvas)
                entry.destroy()

            entry.bind('<Return>', saveChange)
            entry.bind('<FocusOut>', lambda e: entry.destroy())

    def isClickInside(self, x, y, width, height, eventX, eventY):
        return (x <= eventX <= x + width and
            y <= eventY <= y + height)

    def createTable(self):
        self.dataTable = ttk.Treeview(self.root, columns=("X", "Y"), show="headings")
        self.dataTable.heading("X", text="X Data")
        self.dataTable.heading("Y", text="Y Data")
        self.dataTable.pack(side=tk.RIGHT, fill=tk.Y, expand=1)

    def populateTable(self):
        if (self.sortedX == True):
            self.graph.sortByX()
        self.dataTable.delete(*self.dataTable.get_children())

        for x, y in zip(self.graph.getXData(), self.graph.getYData()):
            self.dataTable.insert("", "end", values=(x, y))

    def addRow(self):
        x = max(self.graph.getXData()) + 1
        y = 0
        self.graph.setXData(self.graph.getXData() + [x])
        self.graph.setYData(self.graph.getYData() + [y])
        self.populateTable()
        self.graph.updatePlot(self.canvas)

    def deleteRow(self):
        selected_item = self.dataTable.selection()
        if selected_item:
            xVal = self.dataTable.item(selected_item)["values"][0]
            index = self.graph.getXData().index(xVal)
            self.graph.setXData(self.graph.getXData()[:index] + self.graph.getXData()[index + 1:])
            self.graph.setYData(self.graph.getYData()[:index] + self.graph.getYData()[index + 1:])
            self.populateTable()
            self.graph.updatePlot(self.canvas)
