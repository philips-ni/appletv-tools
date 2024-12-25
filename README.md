# AppleTV Tools

`gen_live_stream_source_list.py` is a script that helps AppleTV APTV users generate live stream source files automatically.

After creating these source files, users can host them on a home PC HTTP server and configure the link in the APTV app, which is an excellent live stream app for Apple TV.

Watch the tutorial: [YouTube Video](https://youtu.be/66rfnh6UplI)

## For Lazy Users

A new feature has been added to upload the live stream source to a GCP bucket.

I occasionally run the script to collect live stream sources and upload them to my own GCP bucket.

Lazy users can use the following links directly:

- Mainland China TV Channels
  - https://storage.googleapis.com/my_iptv_source_list_240723/mcast_1.txt
  - https://storage.googleapis.com/my_iptv_source_list_240723/mcast_2.txt
  - https://storage.googleapis.com/my_iptv_source_list_240723/mcast_3.txt
  - https://storage.googleapis.com/my_iptv_source_list_240723/mcast_4.txt
  - https://storage.googleapis.com/my_iptv_source_list_240723/mcast_5.txt
  - https://storage.googleapis.com/my_iptv_source_list_240723/mcast_6.txt
  - https://storage.googleapis.com/my_iptv_source_list_240723/mcast_7.txt
  - https://storage.googleapis.com/my_iptv_source_list_240723/mcast_8.txt
- Hong Kong and Taiwan TV Channels
  - https://storage.googleapis.com/my_iptv_source_list_240723/tw_HK.txt

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python gen_live_stream_source_list.py mcast
```

Example output:
```
INFO 2024-07-16T21:18:55.269280-0700 - Text with URLs saved to homepage_webpage.txt
INFO 2024-07-16T21:18:55.343555-0700 - ['221.205.167.229', '171.116.226.141', '27.10.76.11', '58.37.91.59', '125.125.180.16', '125.125.180.16', '117.32.84.56', '124.230.56.64']
INFO 2024-07-16T21:19:13.554401-0700 - Text with URLs saved to tmp.txt
INFO 2024-07-16T21:19:13.623630-0700 - url: http://tonkiang.us/hotellist.html?s=221.205.167.229%3A8085&Submit=+
INFO 2024-07-16T21:19:31.280613-0700 - Text with URLs saved to 221.205.167.229_webpage_text.txt
INFO 2024-07-16T21:19:31.367999-0700 - mcast_1.txt created
INFO 2024-07-16T21:19:46.993593-0700 - Text with URLs saved to tmp.txt
INFO 2024-07-16T21:19:47.066451-0700 - url: http://tonkiang.us/hotellist.html?s=171.116.226.141%3A8085&Submit=+
INFO 2024-07-16T21:20:04.062753-0700 - Text with URLs saved to 171.116.226.141_webpage_text.txt
INFO 2024-07-16T21:20:04.150291-0700 - mcast_2.txt created
INFO 2024-07-16T21:20:23.752117-0700 - Text with URLs saved to tmp.txt
INFO 2024-07-16T21:20:23.823214-0700 - url: http://tonkiang.us/hotellist.html?s=27.10.76.11%3A8004&Submit=+
INFO 2024-07-16T21:20:44.060069-0700 - Text with URLs saved to 27.10.76.11_webpage_text.txt
INFO 2024-07-16T21:20:44.142801-0700 - mcast_3.txt created
INFO 2024-07-16T21:21:27.819163-0700 - Text with URLs saved to tmp.txt
INFO 2024-07-16T21:21:27.896241-0700 - url: http://tonkiang.us/hotellist.html?s=58.37.91.59%3A4000&Submit=+
INFO 2024-07-16T21:21:41.861823-0700 - url: http://tonkiang.us/hotellist.html?s=58.37.91.59%3A4000&Submit=+, text:    IPTV Link Search
...
```

The content of `mcast_N.txt` is like:
```
山西黄河HD,http://221.205.167.229:8085/rtp/226.0.2.235:9792
山西经济与科技HD,http://221.205.167.229:8085/rtp/226.0.2.236:9800
山西影视HD,http://221.205.167.229:8085/rtp/226.0.2.237:9808
山西社会与法治HD,http://221.205.167.229:8085/rtp/226.0.2.238:9816
山西文体生活HD,http://221.205.167.229:8085/rtp/226.0.2.16:8040
山西卫视,http://221.205.167.229:8085/rtp/226.0.2.11:8000
山西黄河,http://221.205.167.229:8085/rtp/226.0.2.12:8008
山西经济与科技,http://221.205.167.229:8085/rtp/226.0.2.13:8016
山西影视,http://221.205.167.229:8085/rtp/226.0.2.14:8024
山西社会与法治,http://221.205.167.229:8085/rtp/226.0.2.15:8032
CCTV1-HD,http://221.205.167.229:8085/rtp/226.0.2.153:9136
CCTV2-HD,http://221.205.167.229:8085/rtp/226.0.2.154:9144
CCTV3-HD,http://221.205.167.229:8085/rtp/226.0.2.208:9576
CCTV4-HD,http://221.205.167.229:8085/rtp/226.0.2.156:9160
CCTV5-HD,http://221.205.167.229:8085/rtp/226.0.2.209:9584
CCTV6-HD,http://221.205.167.229:8085/rtp/226.0.2.210:9592
CCTV7-HD,http://221.205.167.229:8085/rtp/226.0.2.159:9184
CCTV8-HD,http://221.205.167.229:8085/rtp/226.0.2.211:9600
CCTV9-HD,http://221.205.167.229:8085/rtp/226.0.2.161:9200
CCTV10-HD,http://221.205.167.229:8085/rtp/226.0.2.162:9208
CCTV12-HD,http://221.205.167.229:8085/rtp/226.0.2.164:9224
CCTV13-HD,http://221.205.167.229:8085/rtp/226.0.2.165:9232
CCTV14-HD,http://221.205.167.229:8085/rtp/226.0.2.166:9240
HD,http://221.205.167.229:8085/rtp/226.0.2.168:9256
CCTV16-HD,http://221.205.167.229:8085/rtp/226.0.2.169:9264
CCTV17-HD,http://221.205.167.229:8085/rtp/226.0.2.170:9272
...
```

## Using the `mcast_N.txt` File in APTV on Apple TV

- Host an HTTP service in the current directory of your PC:
  - Run `python3 -m http.server 8000` in the current directory.
  - The link to `mcast_N.txt` will be like `http://192.168.1.130:8000/mcast_1.txt`.
- Configure this link in the APTV UI.
- If the links in `mcast_N.txt` stop working, run `python gen_live_stream_source_list.py mcast` again to refresh the files.

## Troubleshooting

The default `chromedriver` in this repository is for macOS M1. If you are using a different OS, download the appropriate `chromedriver` from [ChromeDriver Downloads](https://developer.chrome.com/docs/chromedriver/downloads).

If the `chromedriver` version is too low, download the correct version from [ChromeDriver Downloads](https://developer.chrome.com/docs/chromedriver/downloads).


