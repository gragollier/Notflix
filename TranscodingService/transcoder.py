import logging
import os
import re
import subprocess
import zipfile


def transcode(file, metadata={'target-bitrates': [2400]}):
    bitrates = metadata['target-bitrates']

    logging.info("Begining transcode")
    for bitrate in bitrates:
        subprocess.call(
            f"ffmpeg -i {file} -b:v {bitrate}k -maxrate {bitrate}k -bufsize 2M {file}_{bitrate}_int.mp4", shell=True)

    logging.info("Final packaging")

    final_files = " ".join(
        [f"{file}_{bitrate}_int.mp4#video" for bitrate in bitrates])
    final_files += f" {file}_{bitrates[0]}_int.mp4#audio"
    subprocess.call(
        "MP4Box -dash 2000 -rap -frag-rap -profile onDemand " + final_files, shell=True)

    logging.info("Copying files to output zip")
    zip_filename = f"{file}.zip"
    zipf = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)

    output_files = [f for f in os.listdir(
        '.') if re.match(r'.*dashinit\.mp4', f)]
    os.rename(f"{file}_{bitrates[0]}_int_dash.mpd", f"{file}_dash.mpd")
    output_files.append(f"{file}_dash.mpd")

    for output_file in output_files:
        zipf.write(output_file)

    zipf.close()

    logging.info("Cleaning up intermediate files")
    intermediate_files = [f"{file}_{bitrate}_int.mp4" for bitrate in bitrates]
    intermediate_files.extend(output_files)

    intermediate_files.append(file)

    for intermediate_file in intermediate_files:
        os.remove(intermediate_file)

    return zip_filename
