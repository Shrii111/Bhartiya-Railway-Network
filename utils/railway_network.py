class RailwayNetwork:
    def __init__(self):
        # Example railway graph as dictionary
        self.graph = {
            'Delhi': ['Kanpur', 'Lucknow'],
            'Kanpur': ['Delhi', 'Bhopal'],
            'Lucknow': ['Delhi', 'Varanasi'],
            'Bhopal': ['Kanpur', 'Nagpur'],
            'Varanasi': ['Lucknow', 'Patna'],
            'Nagpur': ['Bhopal', 'Hyderabad'],
            'Patna': ['Varanasi'],
            'Hyderabad': ['Nagpur']
        }

    def get_graph(self):
        return self.graph
