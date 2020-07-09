import requests

def update_metadata(video_id, host):
    requests.post(f"{host}/v1/store/video/{video_id}/set_live")