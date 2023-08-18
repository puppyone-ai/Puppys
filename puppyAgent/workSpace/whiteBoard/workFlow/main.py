# workFlow.py
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class Workflow:
    def __init__(self, workflow:dict={}, overallstepNum=None, finishedstepNum=None, remainingstepNum=None):
        self._workflow = workflow
        self._overallstepNum = overallstepNum
        self._finishedstepNum = finishedstepNum
        self._remainingstepNum = remainingstepNum

    # get the workFlow and related information
    @property
    def workFlow(self):
        return self._workflow
    
    @property
    def overallstepNum(self):
        return self._overallstepNum
    
    @property
    def finishedstepNum(self):
        return self._finishedstepNum
    
    @property
    def remainingstepNum(self):
        return self._remainingstepNum


    def addWork(self, workName, assignee, estimatedDuration, dependencies=[]):
        if workName not in self._workflow:
            self._workflow[workName] = {'assignee': assignee, 'duration': estimatedDuration, 'dependencies': dependencies}
        else:
            self._workflow[workName]['assignee'] = assignee
            self._workflow[workName]['duration'] = estimatedDuration
            self._workflow[workName]['dependencies'] = dependencies
    

    # change the workflow's list representation to matrix representation
    def adjacencyListToMatrix(self):
        nodes = list(self._workflow.keys())
        for work in self._workflow.values():
            nodes.extend(work['dependencies'])
        nodes = list(set(nodes))
        nodes.sort()
        
        matrix = np.zeros((len(nodes), len(nodes)), dtype=int)
        for node, work in self._workflow.items():
            for neighbor in work['dependencies']:
                matrix[nodes.index(node)][nodes.index(neighbor)] = 1
        return matrix
    

    # draw the workflow with the assignee and duration
    def visualizeWorkflowFinal(self):
        self._pipeline_spacing = 2
        self._work_spacing = 0.1
        self._rectangle_height = 1
        self._font_size = 12

        G = nx.DiGraph()
        
        # Track unique assignees to determine y-positions
        assignees = list(set([details['assignee'] for details in self._workflow.values()]))
        assignee_mapping = {assignee: i for i, assignee in enumerate(assignees)}
        print(assignee_mapping)
        
        for work, details in self._workflow.items():
            G.add_node(work, assignee=details['assignee'], duration=details['duration'])
            for dependency in details['dependencies']:
                G.add_edge(dependency, work)
        
        # Initial position mapping
        pos = {}
        for node, attrs in G.nodes(data=True):
            assignee = attrs['assignee']
            y_position = assignee_mapping[assignee] * self._pipeline_spacing
            x_position = list(G.predecessors(node))
            if not x_position:
                x_position = 0
            else:
                x_position = len(x_position) * self._work_spacing
            pos[node] = (x_position, y_position)

        # Adjust positions to ensure left-to-right flow, within the main function
        adjusted = True
        while adjusted:
            adjusted = False
            for node in G.nodes():
                node_x = pos[node][0]
                node_duration = G.nodes[node]['duration']
                for predecessor in G.predecessors(node):
                    pred_x = pos[predecessor][0]
                    pred_duration = G.nodes[predecessor]['duration']
                    if node_x < pred_x + pred_duration + self._work_spacing:
                        node_x = pred_x + pred_duration + self._work_spacing
                        pos[node] = (node_x, pos[node][1])
                        adjusted = True
        
        # Drawing pipelines
        plt.figure(figsize=(14, 10))
        for assignee, y_position in assignee_mapping.items():
            plt.plot([-1, max([x for x, _ in pos.values()]) + 5], [y_position* self._pipeline_spacing, y_position* self._pipeline_spacing], color='lightgray', linestyle='--')
            plt.text(-1.5, y_position* self._pipeline_spacing, assignee, verticalalignment='center', fontsize=self._font_size)
            
        # Drawing nodes with rectangle shape and proportional width
        for node, (x, y) in pos.items():
            duration = G.nodes[node]['duration']
            rectangle = plt.Rectangle((x, y - self._rectangle_height / 2), duration, self._rectangle_height, color='skyblue', ec='black')
            plt.gca().add_patch(rectangle)
            plt.text(x + duration / 2, y, node, ha='center', va='center', fontsize=self._font_size, color='black')
            
        # Drawing edges with straight lines connecting end of one rectangle to the start of another
        for (u, v) in G.edges():
            start_x = pos[u][0] + G.nodes[u]['duration']
            start_y = pos[u][1]
            end_x = pos[v][0]
            end_y = pos[v][1]
            plt.plot([start_x, end_x], [start_y, end_y], color='gray', lw=1.5)
        
        plt.xlim(-2, max([x for x, _ in pos.values()]) + 6)  # Adjust xlim to provide space for longer duration tasks
        plt.ylim(-1, len(assignees) * self._pipeline_spacing + 1)
        plt.axis('off')
        plt.title("Final Workflow Visualization")
        plt.show()



# Testing the final visualization
A = Workflow()
A.addWork('A', 'puppy', 1, [])
A.addWork('B', 'puppy', 3, ['A'])
A.addWork('C', 'cat', 2, ['A'])
A.addWork('D', 'bird', 4, ['B', 'C'])
A.addWork('E', 'cat', 3, ['B', 'D'])
A.visualizeWorkflowFinal()
