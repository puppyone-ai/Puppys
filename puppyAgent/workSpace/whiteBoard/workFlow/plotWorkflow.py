import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class WorkflowVisualization:
    def __init__(self, workflow):
        self._workflow = workflow
        self._pipeline_spacing = 2
        self._work_spacing = 0.1
        self._rectangle_height = 1
        self._font_size = 12
        self._assignee_mapping = self._create_assignee_mapping()

    def _create_assignee_mapping(self):
        assignees = list(set([details['assignee'] for details in self._workflow.values()]))
        return {assignee: i for i, assignee in enumerate(assignees)}

    def _build_network(self):
        G = nx.DiGraph()
        for work, details in self._workflow.items():
            G.add_node(work, assignee=details['assignee'], duration=details['duration'])
            for dependency in details['dependencies']:
                G.add_edge(dependency, work)
        return G

    def _calculate_initial_positions(self, G):
        pos = {}
        for node, attrs in G.nodes(data=True):
            assignee = attrs['assignee']
            y_position = self._assignee_mapping[assignee] * self._pipeline_spacing
            x_position = list(G.predecessors(node))
            x_position = len(x_position) * self._work_spacing if x_position else 0
            pos[node] = (x_position, y_position)
        return pos

    def _adjust_positions(self, G, pos):
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
        return pos

    def _draw_pipelines(self, pos):
        plt.figure(figsize=(14, 10))
        for assignee, y_position in self._assignee_mapping.items():
            plt.plot([-1, max([x for x, _ in pos.values()]) + 5], 
                     [y_position * self._pipeline_spacing, y_position * self._pipeline_spacing], 
                     color='lightgray', linestyle='--')
            plt.text(-1.5, y_position * self._pipeline_spacing, assignee, verticalalignment='center', fontsize=self._font_size)

    def _draw_nodes(self, G, pos):
        for node, (x, y) in pos.items():
            duration = G.nodes[node]['duration']
            rectangle = plt.Rectangle((x, y - self._rectangle_height / 2), duration, self._rectangle_height, color='skyblue', ec='black')
            plt.gca().add_patch(rectangle)
            plt.text(x + duration / 2, y, node, ha='center', va='center', fontsize=self._font_size, color='black')

    def _draw_edges(self, G, pos):
        for (u, v) in G.edges():
            start_x = pos[u][0] + G.nodes[u]['duration']
            start_y = pos[u][1]
            end_x = pos[v][0]
            end_y = pos[v][1]
            plt.plot([start_x, end_x], [start_y, end_y], color='gray', lw=1.5)

    def visualizeWorkflowFinal(self):
        G = self._build_network()
        pos = self._calculate_initial_positions(G)
        pos = self._adjust_positions(G, pos)
        
        self._draw_pipelines(pos)
        self._draw_nodes(G, pos)
        self._draw_edges(G, pos)
        
        plt.xlim(-2, max([x for x, _ in pos.values()]) + 6)
        plt.ylim(-1, len(self._assignee_mapping) * self._pipeline_spacing + 1)
        plt.axis('off')
        plt.title("Final Workflow Visualization")
        plt.show()

# Rerun the improved class for visualization
A = WorkflowVisualization(sample_workflow)
A.visualizeWorkflowFinal()


