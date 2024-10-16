from enum import Enum

class GRAPH_TYPE(Enum):
    LINE = "line"
    BAR = "bar"
    SCATTER = "scatter"
    PIE = "pie"
    HISTOGRAM = "histogram"

# Not used currently while waiting for more graph types to be implemented
class SGEGraph():
    def __init__(self, graphType):
        self.title = "Title"
        self.data = []
        self.type = graphType