import network
import os
import urequests
import json
import hashlib
import binascii
import machine
import time
import network
import json
    
#Config_File
config_file = json.load(open('config.json'))

class ugit:
    # ugit
  # micropython OTA update from github
  # Created by TURFPTAx for the openmuscle project
  # Check out https://openmuscle.org for more info
  #
  # Pulls files and folders from open github repository

  global internal_tree

  #### -------------User Variables----------------####
  #### 
  # Default Network to connect using wificonnect()
  ssid = config_file['network']['ssid']
  password = config_file['network']['password']

  # CHANGE TO YOUR REPOSITORY INFO
  # Repository must be public if no personal access token is supplied
  user = 'JoelErni'
  repository = 'ESP32_files'
  token = ''
  # Change this variable to 'master' or any other name matching your default branch
  default_branch = 'main'

  # Don't remove ugit.py from the ignore_files unless you know what you are doing :D
  # Put the files you don't want deleted or updated here use '/filename.ext'
  ignore_files = ['/ugit.py', '/boot.py', '/config.json']
  ignore = ignore_files
  ### -----------END OF USER VARIABLES ----------####

  # Static URLS
  # GitHub uses 'main' instead of master for python repository trees
  giturl = 'https://github.com/{user}/{repository}'
  call_trees_url = f'https://api.github.com/repos/{user}/{repository}/git/trees/{default_branch}?recursive=1'
  raw = f'https://raw.githubusercontent.com/{user}/{repository}/master/'

  def pull(f_path,raw_url):
    print(f'pulling {f_path} from github')
    #files = os.listdir()
    headers = {'User-Agent': 'ugit-turfptax'} 
    # ^^^ Github Requires user-agent header otherwise 403
    if len(ugit.token) > 0:
        headers['authorization'] = "bearer %s" % ugit.token 
    r = urequests.get(raw_url, headers=headers)
    try:
      new_file = open(f_path, 'w')
      new_file.write(r.content.decode('utf-8'))
      new_file.close()
    except:
      print('decode fail try adding non-code files to .gitignore')
      try:
        new_file.close()
      except:
        print('tried to close new_file to save memory durring raw file decode')
    
  def pull_all(tree=call_trees_url,raw = raw,ignore = ignore,isconnected=False):
    if not isconnected:
        wlan = ugit.wificonnect() 
    os.chdir('/')
    tree = ugit.pull_git_tree()
    internal_tree = ugit.build_internal_tree()
    internal_tree = ugit.remove_ignore(internal_tree)
    print(' ignore removed ----------------------')
    print(internal_tree)
    log = []
    # download and save all files
    for i in tree['tree']:
      if i['type'] == 'tree':
        try:
          os.mkdir(i['path'])
        except:
          print(f'failed to {i["path"]} dir may already exist')
      elif i['path'] not in ignore:
        try:
          os.remove(i['path'])
          log.append(f'{i["path"]} file removed from int mem')
          internal_tree = ugit.remove_item(i['path'],internal_tree)
        except:
          log.append(f'{i["path"]} del failed from int mem')
          print('failed to delete old file')
        try:
          ugit.pull(i['path'],raw + i['path'])
          log.append(i['path'] + ' updated')
        except:
          log.append(i['path'] + ' failed to pull')
    # delete files not in Github tree
    if len(internal_tree) > 0:
        print(internal_tree, ' leftover!')
        for i in internal_tree:
            os.remove(i)
            log.append(i + ' removed from int mem')
    logfile = open('ugit_log.py','w')
    logfile.write(str(log))
    logfile.close()
    time.sleep(10)
    #return check instead return with global

  def wificonnect(ssid=ssid,password=password):
      print('Use: like ugit.wificonnect(SSID,Password)')
      print('otherwise uses ssid,password in top of ugit.py code')
      wlan = network.WLAN(network.STA_IF)
      wlan.active(False)
      wlan.active(True)
      wlan.connect(ssid,password)
      while not wlan.isconnected():
          pass
      print('Wifi Connected!!')
      print(f'SSID: {ssid}')
      print('Local Ip Address, Subnet Mask, Default Gateway, Listening on...')
      print(wlan.ifconfig())
      return wlan
    
  def build_internal_tree():
    global internal_tree
    internal_tree = []
    os.chdir('/')
    for i in os.listdir():
      ugit.add_to_tree(i)
    return(internal_tree)

  def add_to_tree(dir_item):
    global internal_tree
    if ugit.is_directory(dir_item) and len(os.listdir(dir_item)) >= 1:
      os.chdir(dir_item)
      for i in os.listdir():
        ugit.add_to_tree(i)
      os.chdir('..')
    else:
      print(dir_item)
      if os.getcwd() != '/':
        subfile_path = os.getcwd() + '/' + dir_item
      else:
        subfile_path = os.getcwd() + dir_item
      try:
        print(f'sub_path: {subfile_path}')
        internal_tree.append([subfile_path,ugit.get_hash(subfile_path)])
      except OSError: # type: ignore # for removing the type error indicator :)
        print(f'{dir_item} could not be added to tree')


  def get_hash(file):
    print(file)
    o_file = open(file)
    r_file = o_file.read()
    sha1obj = hashlib.sha1(r_file)
    hash = sha1obj.digest()
    return(binascii.hexlify(hash))

  def get_data_hash(data):
      sha1obj = hashlib.sha1(data)
      hash = sha1obj.digest()
      return(binascii.hexlify(hash))
    
  def is_directory(file):
    directory = False
    try:
      return (os.stat(file)[8] == 0)
    except:
      return directory
      
  def pull_git_tree(tree_url=call_trees_url,raw = raw):
    headers = {'User-Agent': 'ugit-turfptax'} 
    # ^^^ Github Requires user-agent header otherwise 403
    if len(ugit.token) > 0:
        headers['authorization'] = "bearer %s" % ugit.token 
    r = urequests.get(tree_url,headers=headers)
    data = json.loads(r.content.decode('utf-8'))
    if 'tree' not in data:
        print('\nDefault branch "main" not found. Set "default_branch" variable to your default branch.\n')
        raise Exception(f'Default branch {ugit.default_branch} not found.') 
    tree = json.loads(r.content.decode('utf-8'))
    return(tree)
    
  def parse_git_tree():
    tree = ugit.pull_git_tree()
    dirs = []
    files = []
    for i in tree['tree']:
      if i['type'] == 'tree':
        dirs.append(i['path'])
      if i['type'] == 'blob':
        files.append([i['path'],i['sha'],i['mode']])
    print('dirs:',dirs)
    print('files:',files)
    
    
  def check_ignore(tree=call_trees_url,raw = raw,ignore = ignore):
    os.chdir('/')
    tree = ugit.pull_git_tree()
    check = []
    # download and save all files
    for i in tree['tree']:
      if i['path'] not in ignore:
          print(i['path'] + ' not in ignore')
      if i['path'] in ignore:
          print(i['path']+ ' is in ignore')
          
  def remove_ignore(internal_tree,ignore=ignore):
      clean_tree = []
      int_tree = []
      for i in internal_tree:
          int_tree.append(i[0])
      for i in int_tree:
          if i not in ignore:
              clean_tree.append(i)
      return(clean_tree)
          
  def remove_item(item,tree):
      culled = []
      for i in tree:
          if item not in i:
              culled.append(i)
      return(culled)

  def update():
      print('updates ugit.py to newest version')
      raw_url = 'https://raw.githubusercontent.com/turfptax/ugit/master/'
      ugit.pull('ugit.py',raw_url+'ugit.py')

  def backup():
      int_tree = ugit.build_internal_tree()
      backup_text = "ugit Backup Version 1.0\n\n"
      for i in int_tree:
          data = open(i[0],'r')
          backup_text += f'FN:SHA1{i[0]},{i[1]}\n'
          backup_text += '---'+data.read()+'---\n'
          data.close()
      backup = open('ugit.backup','w')
      backup.write(backup_text)
      backup.close()

def main():
  ugit.wificonnect()
  ugit.pull_all()
  print("pulled done")

  import main as mainScript
  mainScript.main()
    
if __name__ == "__main__":
    main()
