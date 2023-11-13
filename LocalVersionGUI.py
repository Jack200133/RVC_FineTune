# USAR SOLO PARA VERIFICACIONES O INFERENCIAS NO USARPARA ENTRENAR
# ATT- LA RAM DE MI PC QUE NO AGUANTO
import os
import threading
import time
import tarfile
import requests
import subprocess
import sys
sys.path.append('/home/jack/U/VIII/DeepLearning/RVC_FineTune/content/Retrieval-based-Voice-Conversion-WebUI')
from utils import backups

#@markdown #Click here to run the GUI

#@markdown Keep this option enabled to use the simplified, easy interface.
easy_gui = False #@param{type:"boolean"}

#@markdown Keep this option enabled to use automatic backups feature.
auto_backups = True #@param{type:"boolean"}

#@markdown On this colab, the TensorBoard is automatically loaded. This lets you track advanced training statistics (not relevant for using existing models).
#@markdown <br> The important one being, loss/g/total. To avoid overtraining, watch the value and wait till it starts to rise again. <br>
#@markdown Overtraining is much more likely to happen on v2 weights. This is not necessarily a bad thing, as it means models will be finished sooner. <br>
#@markdown <div style="display:flex; justify-content:center">
#@markdown     <div style="margin-right:10px">
#@markdown         <img src="https://media.discordapp.net/attachments/1089076875999072302/1113732090391969792/image.png" width="700">
#@markdown     </div>
#@markdown </div>

#@markdown Follow the whole training guide here: <br> https://docs.google.com/document/d/13ebnzmeEBc6uzYCMt-QVFQk-whVrK4zw8k7_Lw3Bv_A/edit?usp=sharing

LOGS_FOLDER = '/home/jack/U/VIII/DeepLearning/RVC_FineTune/content/Retrieval-based-Voice-Conversion-WebUI/logs'
if not os.path.exists(LOGS_FOLDER):
    os.makedirs(LOGS_FOLDER)

WEIGHTS_FOLDER = '/home/jack/U/VIII/DeepLearning/RVC_FineTune/content/Retrieval-based-Voice-Conversion-WebUI/weights'
if not os.path.exists(WEIGHTS_FOLDER):
    os.makedirs(WEIGHTS_FOLDER)
def download_file(url, destination):
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination, 'wb') as f:
            f.write(response.content)

def extract_tar_file(tar_path, extract_path):
    with tarfile.open(tar_path, 'r:gz') as tar:
        tar.extractall(extract_path)

def extract_wav2lip_tar_files():
    download_file('https://github.com/777gt/EVC/raw/main/wav2lip-HD.tar.gz', '/home/jack/U/VIII/DeepLearning/RVC_FineTune/content/wav2lip-HD.tar.gz')
    download_file('https://github.com/777gt/EVC/raw/main/wav2lip-cache.tar.gz', '/home/jack/U/VIII/DeepLearning/RVC_FineTune/content/wav2lip-cache.tar.gz')

    extract_tar_file('/home/jack/U/VIII/DeepLearning/RVC_FineTune/content/wav2lip-cache.tar.gz', '/')
    extract_tar_file('/home/jack/U/VIII/DeepLearning/RVC_FineTune/content/wav2lip-HD.tar.gz', '/content')

def start_web_server(easy_gui=False, auto_backups=False):
    os.chdir('/home/jack/U/VIII/DeepLearning/RVC_FineTune/content/Retrieval-based-Voice-Conversion-WebUI')
    subprocess.Popen(['tensorboard', '--logdir', 'logs'])

    os.makedirs('audios', exist_ok=True)

    if easy_gui:
        subprocess.run(['pip', 'install', '-q', 'gTTS'])
        subprocess.run(['pip', 'install', '-q', 'elevenlabs'])
        download_file('https://github.com/777gt/-EVC-/raw/main/audios/someguy.mp3', 'audios/someguy.mp3')
        download_file('https://github.com/777gt/-EVC-/raw/main/audios/somegirl.mp3', 'audios/somegirl.mp3')
        extract_wav2lip_tar_files()
        subprocess.run(['python3', 'EasierGUI.py', '--colab', '--pycmd', 'python3'])
    else:
        subprocess.run(['python3', 'infer-web.py', '--colab', '--pycmd', 'python3'])

# Main execution
if __name__ == '__main__':
    easy_gui = False  # set to True if you want to use the GUI
    auto_backups = False  # set to True if you want to enable auto backups

    web_server_thread = threading.Thread(target=start_web_server, args=(easy_gui, auto_backups))
    web_server_thread.start()

    if auto_backups:
        # Replace 'backups.backup_files()' with the actual function call you have for performing backups
        pass
    else:
        while True:
            time.sleep(10)  # sleep for 10 seconds