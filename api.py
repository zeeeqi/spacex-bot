import os
import requests
from urllib.parse import urljoin, quote


class SpaceXAPI:
    """
    Utility class to interact with the SpaceX API
    """

    def __init__(self):
        self.base_url = os.getenv("API_BASE_URL", None)
        self.video_name = os.getenv("VIDEO_NAME", None)
        self.video_url = urljoin(self.base_url, f'video/{quote(self.video_name)}/')

    def get_video_info(self):
        """
        Get the video info
        """
        return requests.get(self.video_url).json()

    def get_frame_url(self, frame):
        """
        Get the frame info
        """
        return urljoin(self.video_url, f'frame/{frame}/')
