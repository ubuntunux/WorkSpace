class Unit:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return "%f %s" % (self.value, self.__class__.__name__)
    
class Cm(Unit):pass    
class Mm(Unit):pass    
class Inch(Unit):pass    
class Pt(Unit):pass    
class Px(Unit):pass
class Dxa(Unit):pass    
class Emu(Unit):pass
    
class Conversioner:
    def __init__(self):
        self.conversionMap = {}
    
    def setConversionRatio(self, srcUnit, srcRatio, dstUnit, dstRatio):
        if srcUnit not in self.conversionMap:
            self.conversionMap[srcUnit] = {}
        if dstUnit not in self.conversionMap:
            self.conversionMap[dstUnit] = {}
        self.conversionMap[srcUnit][dstUnit] = dstRatio/srcRatio
        self.conversionMap[dstUnit][srcUnit] = srcRatio/dstRatio
    
    def conversion(self, srcUnitInst, dstUnit):
        dstUnitInst = self.doConversion(srcUnitInst, dstUnit)
        if dstUnitInst is None:
            if type(srcUnitInst) == dstUnit:
                dstUnitInst = srcUnitInst
            else:
                print("%s cannot conversion to %s" % (srcUnitInst.__class__.__name__, dstUnit.__name__))
                return
        print(">> %s => %s" % (srcUnitInst, dstUnitInst))
    
    def doConversion(self, srcUnitInst, dstUnit, searchList=None):        
        if searchList == None:
            searchList = []
        srcUnit = type(srcUnitInst)
        if srcUnit == dstUnit:
            return None
        searchList.append(srcUnit)        
        if srcUnit in self.conversionMap:
            for curUnit in self.conversionMap[srcUnit]:
                if curUnit not in searchList:
                    searchList.append(curUnit)
                    if curUnit == dstUnit:
                        dstUnitInst = dstUnit(srcUnitInst.value * self.conversionMap[srcUnit][dstUnit])
                        return dstUnitInst
                    curUnitInst = curUnit(srcUnitInst.value * self.conversionMap[srcUnit][curUnit])
                    findUnitInst = self.doConversion(curUnitInst, dstUnit, searchList)
                    if findUnitInst:                        
                        return findUnitInst
        return None

# Set unit conversion datas.
conversioner = Conversioner()
conversioner.setConversionRatio(Inch, 1.0, Cm, 2.54)
conversioner.setConversionRatio(Cm, 1.0, Mm, 10.0)
conversioner.setConversionRatio(Inch, 1.0, Pt, 72.0)
conversioner.setConversionRatio(Inch, 1.0, Px, 96.0)
conversioner.setConversionRatio(Pt, 1.0, Dxa, 20.0)
conversioner.setConversionRatio(Dxa, 1.0, Emu, 635.0)

# Run unit conversion test.
conversioner.conversion(Cm(10), Cm)
conversioner.conversion(Inch(10), Mm)
conversioner.conversion(Px(1024), Pt)
conversioner.conversion(Px(768), Inch)
conversioner.conversion(Emu(9144000), Inch)
conversioner.conversion(Dxa(12000), Px)