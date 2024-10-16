from SimpleGraphEditor.plot_editor import SGEPlotEditor
from SimpleGraphEditor.graphs import GRAPH_TYPE

def main():
    x = [1, 2, 3, 4, 5]
    y = [10, 15, 13, 17, 19]

    plotEditor = SGEPlotEditor()
    plotEditor.type = GRAPH_TYPE.LINE
    plotEditor.graph.setXData(x)
    plotEditor.graph.setYData(y)
    plotEditor.graph.setTitle("Stock Price Over Time")
    plotEditor.graph.setXLabel("Days")
    plotEditor.graph.setYLabel("Stock Price (USD)")
    plotEditor.start()

if __name__ == "__main__":
    main()