#!/usr/bin/env python3
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
from lib.fac import FuncAsCmd
from lib.color_print import ColorPrint
from lib.local_shell import run_cmd
import os
from lib.folder import FolderHelper
from lib.log import setup_logger

setup_logger()
pr = ColorPrint()
fac = FuncAsCmd()

def get_response(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses
    return response 


def get_html_page(url):
    response = get_response(url) 
    return response.text

def get_all_img_src(html):
    soup = BeautifulSoup(html, "html.parser")
    image_links = []
    image_tags = soup.find_all("img", src=True)
    image_links.extend([tag['src'] for tag in image_tags])
    return image_links 

def dl_img(img_url, output_folder, filename=None):
    if not filename:
        filename = os.path.basename(urlparse(img_url).path)
        raise ValueError("filename is None")

    img_data = get_response(img_url).content
    with open(os.path.join(output_folder, filename), "wb") as f:
        f.write(img_data)
    print(f"Downloaded: {img_url} {filename}")


#=================================================== 

@fac.as_cmd("download images in a link")
def download_img_src(args):
    output_folder = args.output
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    html = get_html_page(args.link)
    links = get_all_img_src(html)
    i = 0
    for l in links:
        dl_img(l, output_folder, f"{i}") 
        i += 1





@fac.as_cmd("list all img tags in a link")
def list_img_tags(args):
    html = get_html_page(args.link)
    for l in get_all_img_tags(html):
        print(l)


# ==================================================
# must be last 2 functions
# ==================================================
def parse_args():
    parser = argparse.ArgumentParser(
        description="analyze a link and download all images in the link.")
    parser.add_argument("-l", "--link", required=True, help="url to the webpage")
    parser.add_argument("-o", "--output", default="output", help="output folder")
    fac.add_funcs_as_cmds(parser, long_cmd_str="--command", short_cmd_str="-c")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    fac.call_func_by_name(args.command, args)


if __name__ == "__main__":
    main()

