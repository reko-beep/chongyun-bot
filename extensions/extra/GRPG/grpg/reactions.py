import logging

class Reactor:
    def __init__(self, chara):
        self.chara = chara
        self.applied_elements = []


        pass

    def apply(self, element: str):

        if element == 'Physical':
            logging.info('not applying physical - not an element')
        
        elif element not in [
            'Electro', 'Pyro', 'Hydro', 'Cryo', 'Anemo', 'Geo', 'Dendro'
        ]:
            raise Exception("Invalid element applied")
        self.applied_elements.append(element)

    
    

    def react(self, element: str, em):
        """
        performs reactions and outputs 
        """
        self.apply(element)


        # amplifying reactions
        import math

        self.chara.amplification = 1.0

        if self.applied_elements[-2:] == ['Hydro', 'Pyro']:
            # vap
            self.chara.amplification = 1.5 * (1 + 0.00189266831 * em * math.exp(-0.000505 * em))
            pass

        if self.applied_elements[-2:] == ['Pyro', 'Hydro']:
            # reverse vap
            self.chara.amplification = 2.0 * (1 + 0.00189266831 * em * math.exp(-0.000505 * em))
            pass

        if self.applied_elements[-2:] == ['Cryo', 'Pyro']:
            # melt
            self.chara.amplification = 2.0 * (1 + 0.00189266831 * em * math.exp(-0.000505 * em))
            pass

        if self.applied_elements[-2:] == ['Pyro', 'Cryo']:
            # rev melt
            self.chara.amplification = 1.5 * (1 + 0.00189266831 * em * math.exp(-0.000505 * em))
            pass



        if set(self.applied_elements[-2:]) == set(['Hydro', 'Electro']):
            # Electro-charged
            pass

        if set(self.applied_elements[-2:]) == set(['Electro', 'Pyro']):
            # overload
            pass

        if self.applied_elements[-2:] == set(['Cryo', 'Electro']):
            # superconduct
            # reduce res
            pass

        if self.applied_elements[-2:] == set(['Cryo', 'Hydro']):
            # frozen
            # reapply Cryo
            pass
        
        