import logging
import os
import re
import subprocess
import zipfile


def transcode(file, metadata={'targets': [{"bitrate": 2400, "resolution": 1080}]}):
    targets = metadata['targets']

    logging.info(f"Begining transcode for targets {targets}")
    encoder_command = f"ffmpeg -i {file}"
    for target in targets:
        bitrate = target['bitrate']
        resolution = target['resolution']
        encoder_command += f" -b:v {bitrate}k -vf scale=-1:{resolution} -maxrate {bitrate}k -bufsize 2M {file}_{resolution}_{bitrate}_int.mp4"
    
    logging.info(f"Running encoding command: {encoder_command}")
    subprocess.call(encoder_command, shell=True)

    logging.info("Final packaging")

    final_files = " ".join([f"{file}_{target['resolution']}_{target['bitrate']}_int.mp4#video" for target in targets])
    final_files += f" {file}_{targets[0]['resolution']}_{targets[0]['bitrate']}_int.mp4#audio"
    
    mpd_commad = "MP4Box -dash 2000 -rap -frag-rap -profile onDemand " + final_files
    logging.info(f"Running MPD generation command: {mpd_commad}")
    subprocess.call(mpd_commad, shell=True)

    os.rename(f"{file}_{targets[0]['resolution']}_{targets[0]['bitrate']}_int_dash.mpd", f"{file}_dash.mpd")

    output_files = [f for f in os.listdir('.') if re.match(r'.*dashinit\.mp4', f)]
    output_files.append(f"{file}_dash.mpd")

    logging.info("Copying files to output zip")
    zip_filename = f"{file}.zip"
    zipf = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)

    for output_file in output_files:
        zipf.write(output_file)

    zipf.close()

    logging.info("Cleaning up intermediate files")
    intermediate_files = [f"{file}_{target['resolution']}_{target['bitrate']}_int.mp4" for target in targets]
    intermediate_files.extend(output_files)

    intermediate_files.append(file)

    for intermediate_file in intermediate_files:
        os.remove(intermediate_file)

    return zip_filename
