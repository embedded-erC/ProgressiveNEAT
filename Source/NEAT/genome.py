"""
    Module-level docstring start
"""

from math import exp
from collections import OrderedDict
from Source.constants import *


class Genome(object):
    """
        Class Docstring

        NEAT Responsibilities:
            1. Maintain a list of Connection genes
            2. Maintain a list of Node genes
            3. Have a mechanism to add new Connections
            4. Have a mechanism to add new Nodes
            5. Have a mechanism to convert the linear genome into a network architecture
            6. Maintain a dictionary of Node gene ids, sorted by node_type
            7. Define a method to return the highest innovation number for it's member genes
            8. Define a method to get an ordered list of all gene id's
            9. Define a method to get the size of the genome (connection + node genes)
        Data Reporting/Visualization Responsibilities:
            1. Report the number of Node genes (delineated by in/out/hidden type)
            2, Report the number of Connection genes
    """
    def __init__(self):
        super().__init__()
        self.connection_genes = dict()
        self.node_genes = OrderedDict()

    def mutate_connections(self):
        pass

    def add_node(self):
        pass

    def assemble_topology(self):
        """

        :return:
        """
        self._reset_all_nodes()

        for connection in self.connection_genes.values():
            if connection.enabled:
                input_layer = None
                in_node = self.node_genes[connection.in_node]
                out_node = self.node_genes[connection.out_node]

                if in_node.layer:
                    # Either an input node or we've already had a connection from here
                    input_layer = in_node.layer
                else:
                    input_layer = 2
                    in_node.layer = input_layer

                if out_node.layer and out_node.layer <= input_layer and connection.in_node != connection.out_node:
                    self._propagate_layer_change(out_node.innov_num, input_layer)
                elif not out_node.layer:
                    out_node.layer = input_layer + 1

                in_node.add_outbound_connection(out_node.innov_num, connection.conn_weight)
                out_node.add_inbound_connection(in_node.innov_num)
        self._set_output_layer()
        self._sort_nodes_by_layer()
        self._identify_isolated_nodes()

    def _identify_isolated_nodes(self):
        for node in self.node_genes.values():
            if (not node.inbound_connections or node.inbound_connections == [node.innov_num]) and not \
                    node.node_type == 'input':
                node.is_isolated = True

    def _reset_all_nodes(self):
        [node.reset() for node in self.node_genes.values()]

    def _sort_nodes_by_layer(self):
        self.node_genes = OrderedDict(sorted(self.node_genes.items(), key=lambda node: node[1].layer))

    def _set_output_layer(self):
        """
        Align all output nodes to the highest output node's layer
        :return:
        """
        highest_layer = max([node.layer for node in self.node_genes.values()])
        for node in self.node_genes.values():
            node.layer = highest_layer if node.node_type == "output" else node.layer

    def _propagate_layer_change(self, _start_node_id, _input_layer):
        """
        :param _start_node_id:
        :return:
        """
        next_layer, affected_nodes = self.node_genes[_start_node_id].shift_layer(_input_layer)
        for node in affected_nodes:
            self._propagate_layer_change(node, next_layer)

    def get_greatest_innov(self):
        # Connection genes must have the highest innovation number; the last element in the sorted list is the highest
        return sorted(self.connection_genes)[-1]

    def get_all_gene_ids(self):
        # Return an ordered list of all genes by innovation number
        return sorted(list(self.connection_genes) + list(self.node_genes))

    def get_genome_size(self):
        return len(self.node_genes) + len(self.connection_genes)

    def evaluate(self, inputs):
        """
        *Note: This must only be called after assemble_topology has completed
        *Note: This must also be a fast function...
        :param inputs:
        :return:
        """

        outputs = []

        for ii in range(len(inputs)):
            # Prime the input nodes
            self.node_genes[ii].inbound_activations.append(inputs[ii])
        for node in self.node_genes:
            if node.node_type == 'output':
                # TODO: How to make sure our layer sorting cannot alter the order of output nodes
                outputs.append(node.evaluate())
            else:
                for downstream_node, activation in node.evaluate():
                    self.node_genes[downstream_node].inbound_activations.append(activation)
        return outputs


class Gene(object):
    """
        Class Docstring

        NEAT Responsibilities:
            1. Maintain an innovation number
        Data Reporting/Visualization Responsibilities:
    """
    def __init__(self, innov_num, **kwargs):
        super().__init__(**kwargs)
        self.innov_num = innov_num


class ConnectionGene(Gene):
    """
        Class Docstring

        NEAT Responsibilities:
            1. Define the 'in' node
            2. Define the 'out' node
            3. Define the connection wt. modifier to the 'out' node
            4. Have a mechanism to change the connection wt.
            6. Maintain an enable/disable bit
            7. Have a mechanism to change the enable/disable bit
        Data Reporting/Visualization Responsibilities:
    """
    def __init__(self, in_node, out_node, conn_weight, **kwargs):
        super().__init__(**kwargs)
        self.in_node = in_node
        self.out_node = out_node
        self.conn_weight = conn_weight
        self.enabled = True

    def set_connection_weight(self):
        pass

    def set_enabled(self):
        pass


class NodeGene(Gene):
    """
        Class Docstring

        NEAT Responsibilities:
            1. Maintain a list of candidate input nodes for new inbound connections
            2. Maintain a list of candidate output nodes for new outbound connections
            3. Define a transfer function to be applied to the input signals
            4. Evaluate the transfer function once all signals are received from all input nodes. Return the list of
                all downstream connection IDs when evaluating
            5. Define type as an input, hidden, or output node
            6. Maintain a list of connection gene IDs that signals get propagated down
            7. Maintain a list of inbound connection genes IDs
            8. Maintain a mutable 'layer' number denoting which segment of the hidden layer the node is on.
            9. Define a method to add inbound connections to the inbound_connections list
            10. Define a method to add outbound connections to the outbound_connections list
            11. Define a reset method to clear inbound and outbound connections, layer, and input nad output candidates
            12. Define a method to adjust the Node's layer when building a genome topography
        Data Reporting/Visualization Responsibilities:
            1. Track node evaluations (transfer function firings)
    """
    def __init__(self, node_type='hidden', **kwargs):
        super().__init__(**kwargs)
        self.node_type = node_type
        self.input_candidates = []
        self.output_candidates = []
        self.num_evaluations = 0
        self.outbound_connections = []
        self.outbound_weights = []
        self.inbound_connections = []   # TODO: Can I use this for anything besides testing support?
        self.inbound_activations = []
        self.layer = 1 if self.node_type == 'input' else None
        self.is_isolated = False

    def reset(self):
        self.input_candidates = []
        self.output_candidates = []
        self.inbound_connections = []
        self.inbound_activations = []
        self.outbound_connections = []
        self.outbound_weights = []
        self.num_evaluations = 0
        self.layer = 1 if self.node_type == 'input' else None

    def add_inbound_connection(self, _inbound):
        self.inbound_connections.append(_inbound)

    def add_outbound_connection(self, _outbound, _weight):
        self.outbound_connections.append(_outbound)
        self.outbound_weights.append(_weight)

    def shift_layer(self, _upstream_node_layer):
        """
        Make sure you document this return well, as it's an interface that Genome uses. Namely the tuple mandate
        :param _upstream_node_layer:
        :return:
        """
        if _upstream_node_layer >= self.layer:
            self.layer = _upstream_node_layer + 1
            return self.layer, self.outbound_connections
        return [], []

    def _get_activation(self):
        if self.node_type == 'input':
            return sum(self.inbound_activations)
        elif not self.is_isolated:
            return 1.0 / (1.0 + exp(-kSigmoid_power * sum(self.inbound_activations)))
        else:
            return 0

    def evaluate(self):
        """
        Once all the inputs have been received, Evaluate the transfer function and send the signal to the
        connection genes (or whatever method I have to propagate signals)

        :return:
        - self.outbound_connections and the strength of the signal.
        """
        self.num_evaluations += 1
        activation = self._get_activation()
        downstream_pulses = [activation * weight for weight in self.outbound_weights]

        # Clear in prep for next round of network evaluations. Note the timing of this allows for recursive activations
        self.inbound_activations = []

        return activation if self.node_type == 'output' else zip(self.outbound_connections, downstream_pulses)
