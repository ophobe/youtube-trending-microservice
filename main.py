import requests
import json
import base64
import optparse
import datetime
from os import environ as env
from os.path import join, dirname
from dotenv import load_dotenv

parser = optparse.OptionParser()
parser.add_option('-c', '--country', default='NO')
options, _ = parser.parse_args()

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

endpoint = 'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&chart=mostPopular&regionCode=' + options.country + '&maxResults=50&key='
response = requests.get(endpoint + env.get('YOUTUBE_API_KEY')).text
data = json.loads(response)

videoIds = [video['id'] for video in data['items']]

path = options.country + '/' + datetime.datetime.today().strftime('%d-%m-%Y-%H-%s') + '.txt'

payload = json.dumps({
	'message': path,
	'content': base64.b64encode("\n".join(videoIds))
})

print requests.put(
	'https://api.github.com/repos/ophobe/trending-youtube/contents/' + path,
	data=payload,
	auth=(env.get('GITHUB_USERNAME'), env.get('GITHUB_ACCESS_TOKEN'))
)