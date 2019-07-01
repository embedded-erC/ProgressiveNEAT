"""
Module level docstring stub
"""

import plotly
import plotly.graph_objs as go


class Visualization(object):
    """
    Class level docstring stub
    -Species tracking:
        -Species creation and extinction events will be shown
        -The size of each species will be reported every generation
        -The total fitness (sum of the adjusted fitnesses for each species member) of the species each generation will be tracked
        -The max fitness of the best individual in that species for that generation will be recorded
        -The topology of the best individual for that species for each generation will be visible

    -Topology visualization:
        -Topology should be derivable from an individual's genome
        -Zones for nodes should be defined as Inputs on the left or bottom, outputs on the right or top, and hidden in between
        -Innovation numbers will be visible for nodes and connections
        -Weights will be visible on connections

    -General Statistics:
        -Total number of individuals spawned will be tracked
        -Current innovation number by generation will be tracked
        -Total number of node evaluations will be recorded by generation
        -A list of all fitnesses for that generation will be saved for optional statistical analysis
        -The number of hidden nodes will be recorded per generation
        -The number of total connections will be recorded per generation
        -The number of disabled connections will be recorded per generation

    -Real-time visualization a-la MarIO for a given ANN?!
        -Future requirement

    Generational data structure:
        Dict:
            Keys = generations
            Values = Species-containing dicts

        Species-containing dicts:
            Keys = Species IDs
            Values = Species Stats

        Species Stats dicts:
            Keys/values = <defined in gather_generational_stats() interface>

        If, for example, you wanted to know the size of species #5 on generation 81, you would request:
            self.generational_stats[81][5]["size"]
    """

    def __init__(self):
        super().__init__()
        self.current_generation = 0
        self.species_generational_stats = dict()
        self.overall_generational_stats = dict()

    def set_generation(self, _generation):
        self.current_generation = _generation
        self.species_generational_stats[_generation] = dict()

    def gather_overall_generational_stats(self, _stats_dict):
        self.overall_generational_stats[self.current_generation] = _stats_dict

    def gather_species_generational_stats(self, _species_id, _stats_dict):
        """
        This will interface with Species report_stats() methods.
        Species.report_stats() will return a dict containing the following fields as text dictionary keys:
            1. "size" - the number of individuals in that species in that generation
            2. "species fitness" - the sum total of each individual's performance measure
            3. "peak individual" - full copy of the best performing individual that generation
            4. "extinction generation" - None if an active species, else the generation that it died out
            5. "average connections" - Average number of connection genes (enabled and disabled)
            6. "average nodes" - Average number of node genes for that species.
        :return:
        """
        self.species_generational_stats[self.current_generation].update({_species_id: _stats_dict})

    def _graph_num_speices(self):

        x = sorted(self.species_generational_stats.keys())
        y = [len(self.species_generational_stats[generation]) for generation in x]

        data = [go.Scatter(
            x=x,
            y=y,
            mode='lines+markers'
        )]

        plotly.offline.plot(data, filename='Number of Species Per Generation.html')

    def _graph_champion(self, _winner):

        """
        cycle through the node genes and assign them a y-value.
        cycle through the conn genes and use their inbound/outbound fields to draw the lines.
            Use the conn wt as the hover text

        figure out how to do the recursive connections.
        :return:
        """

        genome = _winner.genome

        layers = dict()
        for node in genome.node_genes.values():
            try:
                layers[node.layer].append(node)
            except KeyError:
                layers[node.layer] = [node]

        offset = 0.15
        for layer in layers:
            n = 1
            for node in layers[layer]:
                node.y_pos = n / (len(layers[layer]) + 1)
                if (layer > 1 and layer % 2) and node.node_type != 'output':
                    node.y_pos += offset
                elif (layer > 1 and not layer % 2) and node.node_type != 'output':
                    node.y_pos -= offset
                n += 1
            offset -= 0.015

        # Create Edges
        edge_traces = []

        for conn in genome.connection_genes.values():
            red = str(max(0, min(255, 127 - (128 * conn.conn_weight))))
            blue = str(max(0, min(255, 127 + (128 * conn.conn_weight))))
            width_multipler = 0.1 * round(abs(conn.conn_weight), 0)
            x0, y0 = genome.node_genes[conn.in_node].layer, genome.node_genes[conn.in_node].y_pos
            x1, y1 = genome.node_genes[conn.out_node].layer, genome.node_genes[conn.out_node].y_pos
            dash = 'solid' if conn.enabled else 'dash'
            edge_traces.append(go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                line=dict(
                    width=0.3+width_multipler,
                    dash=dash,
                    color='rgb({0}, 0, {1})'.format(red, blue),
                )
            ))

        node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            hoverinfo='text',
            marker=dict(
                size=10,
                line=dict(width=2)))

        for node in genome.node_genes.values():
            x, y = node.layer, node.y_pos
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])
            node_trace['text'] += tuple([node.innov_num])

        # Create network graph
        fig = go.Figure(data=edge_traces + [node_trace],
                        layout=go.Layout(
                            title='<br>Champion Topology',
                            titlefont=dict(size=16),
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            annotations=[dict(
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002)],
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

        plotly.offline.plot(fig, filename='champion.html')

    def _graph_species_sizes(self):

        traces = {}
        for generation in sorted(self.species_generational_stats.keys()):
            pop_size_this_gen = sum(
                [self.species_generational_stats[generation][specie]['size'] for specie in self.species_generational_stats[generation]])
            for specie in self.species_generational_stats[generation]:
                try:
                    if self.species_generational_stats[generation][specie]['extinction generation']:
                        pass
                    else:
                        traces[specie]['size'].append(self.species_generational_stats[generation][specie]['size'])
                        traces[specie]['y-value'].append(pop_size_this_gen)
                        traces[specie]['x-value'].append(generation)
                except KeyError:
                    traces[specie] = {'y-value': [pop_size_this_gen],
                                      'x-value': [generation],
                                      'size': [self.species_generational_stats[generation][specie]['size']]}

                if not self.species_generational_stats[generation][specie]['extinction generation']:
                    pop_size_this_gen -= self.species_generational_stats[generation][specie]['size']

        data = []
        for i in traces:
            data.append(
                dict(
                    x=traces[i]['x-value'],
                    y=traces[i]["y-value"],
                    text=traces[i]['size'],
                    hoverinfo='text',
                    mode='lines',
                    line=dict(width=0.5),
                    fill='tonexty',
                    stackgroup=i
                )
            )
        plotly.offline.plot(data, filename='Species Tracking.html', validate=False)

    def _graph_peak_fitness(self):
        x = sorted(self.overall_generational_stats.keys())
        y = [self.overall_generational_stats[generation]['overall peak fitness'] for generation in x]

        data = [go.Scatter(
            x=x,
            y=y,
            mode='lines+markers'
        )]

        plotly.offline.plot(data, filename='Peak Fitness.html')

    def _graph_genome_stats(self, _stat):
        traces = {}
        generations = sorted(self.species_generational_stats.keys())

        for generation in generations:
            for specie in self.species_generational_stats[generation]:
                try:
                    if self.species_generational_stats[generation][specie]['extinction generation']:
                        pass
                    else:
                        val = self.species_generational_stats[generation][specie][_stat]
                        traces[specie]['y-value'].append(val)
                        traces[specie]['x-value'].append(generation)
                        traces[specie]['id'].append((specie, round(val, 2)))
                except KeyError:
                    val = self.species_generational_stats[generation][specie][_stat]
                    traces[specie] = {'y-value': [val],
                                      'x-value': [generation],
                                      'id': [(specie, round(val, 2))]}
        data = []
        for i in traces:
            data.append(
                go.Bar(
                    x=traces[i]['x-value'],
                    y=traces[i]["y-value"],
                    text=traces[i]['id'],
                    hoverinfo='text',
                    marker=dict(
                        line=dict(width=0.5)
                    )
                )
            )

        layout = go.Layout(
            title=_stat,
            barmode='group',
            bargap=0.12,
            bargroupgap=0.3
        )
        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename='{0}.html'.format(_stat), validate=False)

    def graph_stats(self, winner=None):

        self._graph_num_speices()
        self._graph_species_sizes()
        self._graph_peak_fitness()
        self._graph_genome_stats("average connections")
        self._graph_genome_stats("average nodes")
        if winner:
            self._graph_champion(winner)
