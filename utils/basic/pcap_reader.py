import os
import re
import zlib

import cv2
from scapy.layers.inet import TCP
from scapy.utils import rdpcap


class PCAP:
    __images_directory = f"{os.getcwd()}/images"
    pictures_directory = f"{__images_directory}/pictures"
    faces_directory = f"{__images_directory}/faces"
    filename = None

    def __init__(self, filename):
        self.filename = filename

    def __http_assembler(self, filename, picture_directory, faces_directory):
        carved_images = 0
        faces_detected = 0
        a = rdpcap(filename)
        sessions = a.sessions()
        for session in sessions:
            http_payload = ""
            for packet in sessions[session]:
                try:
                    if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                        http_payload += str(packet[TCP].payload)
                except:
                    pass
            headers = self.__get_http_headers(http_payload)
            if headers is None:
                continue
            image, image_type = self.__extract_image(headers, http_payload)

            if image is not None and image_type is not None:
                file_name = f"{filename}-pic_carver_{carved_images}.{image_type}"
                fd = open(f"{picture_directory}/{file_name}")
                fd.write(image)
                fd.close()
                try:
                    result = self.__face_detect(f"{picture_directory}/{file_name}", faces_directory, filename)
                    if result is True:
                        faces_detected += 1
                except:
                    pass
        return carved_images, faces_detected

    def __face_detect(self, path, file_name, faces_directory, filename):
        img = cv2.imread(path)
        cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
        rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20, 20))
        if len(rects) == 0:
            return False
        rects[:, 2:] += rects[:, :2]
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
        cv2.imwrite(f"{faces_directory}/{filename}/{file_name}", img)
        return True

    def __extract_image(self, headers, http_payload):
        image = None
        image_type = None
        try:
            if "image" in headers['Content-Type']:
                image_type = headers["Content-Type"].split("/")[1]
                image = http_payload[http_payload.index("\r\n\r\n") + 4:]
                try:
                    if "Content-Encoding" in headers.keys():
                        if headers['Content-Encoding'] == 'gzip':
                            image = zlib.decompress(image, 16 + zlib.MAX_WBITS)
                        elif headers['Content-Encoding'] == "deflate":
                            image = zlib.decompress(image)
                except:
                    pass
        except:
            return None, None
        return image, image_type

    def __get_http_headers(self, http_payload):
        try:
            headers_raw = http_payload[:http_payload.index("\r\n\r\n") + 2]
            headers = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", headers_raw))
        except:
            return None

        if "Content-Type" not in headers:
            return None

        return headers

    def init_pcap(self, filename):
        print(self.pictures_directory)
        carved_images, faces_detected = self.__http_assembler(filename, self.pictures_directory, self.faces_directory)
        print(f"detect {carved_images} images and {faces_detected} faces")
