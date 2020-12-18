from  core.colors import yellow,red
from core import VERSION
def banner():
    _ = r'''                      By Ethan~
 ____  ____  __  ____  __  
(_  _)(  __)/  \(  __)/ _\ 
  )(   ) _)(  O )) _)/    \
 (__) (__)  \__/(__) \_/\_/  Version:{version}        
'''

    print(yellow+ _.format(version=VERSION,))



