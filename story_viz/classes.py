from pymclevel import  MCSchematic

class StorySchematics:
    """
    This class holds the story schematic objects that will be used by 
    the story schematic placement module. 
    labels:(list:string) The name of the schematic
    schematics:(list:string) A list of filenames pointing to the appropriate schematics
    """
    def __init__(self, labels=None, schematics=None):
        self.schematics = schematics
        self.labels = labels
        self.schematics_dict = {}
        self.__PATH__TO__SCHEMATICS = "stock-schematics/"
        self.__FILE__TYPE = ".schematic"
        print(self.__PATH__TO__SCHEMATICS)


    def get_schematics(self):
        assert self.schematics is not None and self.labels is not None
        for i, filename in enumerate(self.schematics):
            if self.labels[i] not in self.schematics_dict.keys():
                f = filename
                # if self.__PATH__TO__SCHEMATICS not in filename:
                f = self.__PATH__TO__SCHEMATICS + f
                if self.__FILE__TYPE not in filename:
                    f += self.__FILE__TYPE
                f = f.replace('//', '/')
                self.schematics_dict[self.labels[i]] = MCSchematic(filename=f)
        return self.schematics_dict
