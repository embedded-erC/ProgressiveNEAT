""" Module-level docstring stub """

import os
import pickle
from Source.constants import get_config


class Persistence(object):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.genome_folder = self._get_genome_directory_path()

    def _get_genome_directory_path(self):
        #Make the folder if it doesn't exist
        final_path = self.config['Project Root']
        specified_folder = self.config['kGenome_folder'].split(".")
        while specified_folder:
            final_path = os.path.join(final_path, specified_folder.pop(0))
        return final_path

    def save_genomes(self, genomes):
        # Save out a list of gnomes to that folder with a unique timestamp
        print(self.config['Project Root'])
        pass

    def load_genomes(self):
        # Try to load any genomes from the specified directory
        return "testing"


if __name__ == '__main__':

    config = get_config()
    test_persist = Persistence(config)
    test_persist.save_genomes('test')
