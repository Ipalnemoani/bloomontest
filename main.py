# -*- coding: utf-8 -*-
import os
import re
import random
import string

from collections import Counter


class Warehouse(object):
    """
        This class is not used. But it can be used as a test to automatically generate random flowers stream for factory.
    """

    def __init__(self):
        super(Warehouse, self).__init__()
        self.sizes = ['S', 'L']

        # For test I created list oa ascii letters from string module
        # But in real project this must be a DB query of available fl.species
        self.flower_specie = list(string.ascii_lowercase)

    def get_size(self):
        return random.choice(self.sizes)

    def get_flower_specie(self):
        return random.choice(self.flower_specie)

    def start_auto_arrive(self):
        size = self.get_size()
        specie = self.get_flower_specie()
        return f'{specie}{size}'

    def get_arrive_from_file(self, fname='arrive.txt'):
        dirpath = os.path.dirname(os.path.abspath(__file__))
        arrive_file = os.path.join(dirpath, fname)
        with open(fname) as arrive_file:
            text = arrive_file.readlines()
        return text



class FacilityStock():
    """
        The class displays a facility with information on how many total flowers are available, divided by type and size.
    """

    def __init__(self):
        super(FacilityStock, self).__init__()
        # self.stock_items = stock_items

        self.total_flowers = None
        self.flowers = {
                        'S':{'flowers':{}, 'total':0},
                        'L':{'flowers':{}, 'total':0}
                        }

    @staticmethod
    def get_flower_type(flower):
        return flower[0]

    @staticmethod
    def get_flower_size(flower):
        return flower[1]

    def count_total_flowers_in_stock(self) -> int:
        qty = sum([flw['total'] for flw in self.flowers.values()])
        self.total_flowers = qty

    def adding_flower_to_facility(self, fsize: str, ftype: str):
        # Method for adding and calculating flowers in facility by size and type
        if ftype not in self.flowers[fsize]['flowers']:
            self.flowers[fsize]['flowers'][ftype] = 1
        else:
            self.flowers[fsize]['flowers'][ftype] += 1

    def count_qty_flowers_by_size(self, fsize: str) -> int:
        # Method for calculation total flowers in facility by size
        qty = sum(self.flowers[fsize]['flowers'].values())
        self.flowers[fsize]['total'] = qty

    def qty_of_avail_flowers_by_size(self, size: str) -> int:
        return self.flowers[size]['total']

    def qty_of_avail_flowers_by_type_and_size(type, size: str) -> int:
        return self.flowers[size][type]

    def update_stock_from_stream(self, flower: str):

        # When flowers arrive into the facility one-by-one they stored to
        # 'flowers' attribute.
        # Method update information about total qty of flowers in facility
        # And Update information about qty of flowers by size and type

        ftype = self.get_flower_type(flower)
        fsize = self.get_flower_size(flower)
        self.adding_flower_to_facility(fsize, ftype)
        self.count_qty_flowers_by_size(fsize)
        self.count_total_flowers_in_stock()

    def update_stock(self, fsize: str, newstock: dict):
        # Method updates flowers stock if bouquet are created
        self.flowers[fsize]['flowers'] = newstock
        self.count_qty_flowers_by_size(fsize)
        self.count_total_flowers_in_stock()


class BouquetDesign():
    """
        A class describes the bouquet design.

        Attributes:
            bouguet_design (str): is single line of characters with the following format: '<bouquet name><bouquet size><flower 1 quantity><flower 1 specie>...<flower N quantity><flower N specie><total quantity of flowers in the bouquet>'
    """

    def __init__(self, bouguet_design):
        super(BouquetDesign, self).__init__()
        self.bouguet_design = bouguet_design

        self.bd_type = None
        self.bd_size = None
        self.flowers_in_bd = {}
        self.extra_space = 0
        self.bd_total_flowers = 0
        self.qty_flowers_in_bd = 0
        self.flowers_list = re.findall('\d+\w', self.bouguet_design)

    def get_bouquet_design_type(self) -> str:
        return self.bouguet_design[0]

    def get_bouquet_design_size(self) -> str:
        return self.bouguet_design[1]

    def get_total_flowers_in_bd(self) -> int:
        return int(self.flowers_list[-1])

    def get_qty_flowers_in_bd(self) -> int:
        return sum(self.flowers_in_bd.values())

    def get_extra_space(self) -> int:
        return self.bd_total_flowers - self.qty_flowers_in_bd

    def distrib_flowers_by_size_and_type(self):
        for flower in self.flowers_list[:-1]:
            qty = int(flower[:-1])
            ftype = flower[-1]
            self.flowers_in_bd[ftype] = qty
        return

    def get_bouquet_design_components(self):
        self.distrib_flowers_by_size_and_type()
        self.bd_type = self.get_bouquet_design_type()
        self.bd_size = self.get_bouquet_design_size()
        self.bd_total_flowers = self.get_total_flowers_in_bd()
        self.qty_flowers_in_bd = self.get_qty_flowers_in_bd()
        self.extra_space = self.get_extra_space()


class Bouquet(BouquetDesign):
    """
        The Bouquet class is inherited from BouquetDesign and has one attribute 'bqt_flws' (dict): it will be filled as flowers arrive at the facility.

        And has one method for creating a full bouquet.
    """

    def __init__(self, bouguet_design):
        BouquetDesign.__init__(self, bouguet_design)
        self.bqt_flws = {}

    def create_bouquet(self) -> str:

        # Method returns single line of characters with the following format:
        # <bouquet name><bouquet size><flower 1 quantity><flower 1 specie>...<flower N quantity><flower N specie>

        flw = [f'{self.bqt_flws[key]}{key}' for key in sorted(self.bqt_flws)]
        flw = ''.join(flw)
        return f'{self.bd_type}{self.bd_size}{flw}'


def get_input_stream() -> list:
    file_name = 'sample.txt'
    file_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(file_dir, file_name)
    with open(file_path) as input_stream:
        stream_data = input_stream.read()

    split_stream_data = stream_data.split('\n\n')
    return split_stream_data


def main():
    input_stream = get_input_stream()
    bouquet_designs = input_stream[0].strip().split()
    flowers_stream = input_stream[1].strip().split('\n')

    # Creating a facility object
    stock = FacilityStock()
    for flower in flowers_stream:
        # For each flower in stream updating information in facility stock
        # After that checking if it possible to create bouquet from available flowers for each design.
        stock.update_stock_from_stream(flower)
        for design in bouquet_designs:
            # For each bouquet design create Bouquet object with parameters
            bqt = Bouquet(design)
            bqt.get_bouquet_design_components()

            # Flowers are taken from facility only by the size of the design
            stock_flowers_by_size = stock.flowers[bqt.bd_size]['flowers']

            # Creating counter to quickly change the qty of flowers in stock.
            stock_counter = Counter(stock_flowers_by_size)

            # For each type of flower and its quantity in bouquet design, flowers for the bouquet are collected, if their quantity is available in stock.
            for ftype, fqty in bqt.flowers_in_bd.items():
                stock_qty = stock_flowers_by_size.get(ftype)
                if stock_qty and fqty <= stock_qty:
                    bqt.bqt_flws[ftype] = fqty

            # If qty of flowers matches the qty in the design
            if bqt.bqt_flws == bqt.flowers_in_bd:
                # Checking how much qty of flowers are available after bouquet creation
                bouquet_counter = Counter(bqt.bqt_flws)
                new_stock = stock_counter - bouquet_counter
                new_flw_balance = sum(new_stock.values())

                # If there are more or equal flowers in the facility than you can add to the bouquet, flowers of different types and quantities are added to the bouquet. But no more than the total flowers according to the design.
                if bqt.extra_space <= new_flw_balance:
                    felements = list(new_stock.elements())
                    fchoice = random.sample(felements, k=bqt.extra_space)
                    if fchoice:
                        for ftype in new_stock.keys():
                            qty_flw = fchoice.count(ftype)
                            if qty_flw != 0 and ftype in bqt.bqt_flws:
                                bqt.bqt_flws[ftype] += qty_flw
                            elif qty_flw != 0 and ftype not in bqt.bqt_flws:
                                bqt.bqt_flws[ftype] = qty_flw

                    # Create bouquet
                    bouquet = bqt.create_bouquet()

                    # Update qty of flowers by size on stock
                    bouquet_counter = Counter(bqt.bqt_flws)
                    new_stock = dict(stock_counter - bouquet_counter)
                    stock.update_stock(bqt.bd_size, new_stock)

                    print(f"{bouquet}")
                else:
                    continue


if __name__ == '__main__':
    main()
