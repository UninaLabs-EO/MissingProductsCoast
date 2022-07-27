import subprocess
from pathlib import Path

def command_line(cmd:str):
    """ Command line tool """
    print(subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, universal_newlines=True).communicate()[0])

class GPT:

     def __init__(self, product:str, outdir:str, format:str='BEAM-DIMAP'):
          self.prod = product
          self.name = Path(self.prod).stem
          self.format = format
          self.outdir = Path(outdir)

     def blank(self, par=6):
          self.cmd = f'gpt -q {par} -x -Ssource={self.prod} ' # q is the number of threads

     def call(self, suffix:str):
          output = self.outdir.as_posix() + '/' + self.name + '_' + suffix + '.dim'
          print(output)
          self.cmd += f' -t {output} -f {self.format}'
          print(subprocess.Popen(self.cmd.split(' '), stdout=subprocess.PIPE, universal_newlines=True).communicate()[0])
          self.prod = output
          return output

     def LandMask(self, shorExt:int=100):
          """
          Land-Sea Masking Operator
          """
          self.blank()
          self.cmd += f'Land-Sea-Mask -PshorelineExtension={shorExt}'
          self.call(suffix ='LM')

     def Calibration(self, Pols:list=['VH']):
          self.blank()
          for idx, i in enumerate(Pols):
               stringa = f'{i}'
               if idx != len(Pols):
                    stringa += ',' 
          self.cmd += f'Calibration -PoutputImageInComplex=true -PselectedPolarisations={stringa}'
          self.call(suffix='CAL')

     def Deburst(self, Pols:list=['VH']):
          self.blank()
          for idx, i in enumerate(Pols):
               stringa = f'{i}'
               if idx != len(Pols):
                    stringa += ',' 
          self.cmd += f'TOPSAR-Deburst -PselectedPolarisations={stringa}'
          self.call(suffix='DEB')

     def Multilook(self, NRgLooks:int, NAzLooks:int):
          self.blank()
          self.cmd += f'Multilook -PnAzLooks={NRgLooks} -PnRgLooks={NAzLooks}'
          self.call(suffix='ML')

     def AdaptiveThresholding(self, BW=800, GW=500, TW=50, Pfa=6.5):
          self.blank()
          self.cmd += f'AdaptiveThresholding \
               -PbackgroundWindowSizeInMeter={float(BW)} \
               -PguardWindowSizeInMeter={float(GW)} \
               -Ppfa={float(Pfa)} \
               -PtargetWindowSizeInMeter={int(TW)}'
          self.call(suffix='AT')

     def ObjectDiscrimination(self, maxT, minT):
          self.blank()
          self.cmd += f'Object-Discrimination -PmaxTargetSizeInMeter={float(minT)} -PmaxTargetSizeInMeter={float(maxT)}'
          self.call(suffix='OD')
